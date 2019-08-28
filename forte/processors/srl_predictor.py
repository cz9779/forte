import os
import logging
from typing import Dict, List, Tuple

import texar.torch as tx
from texar.torch.hyperparams import HParams
import torch

from forte.common.resources import Resources
from forte.data import DataPack
from forte.data.ontology import ontonotes_ontology
from forte.models.srl.model import LabeledSpanGraphNetwork
from forte.processors.base import BatchProcessor, ProcessInfo

logger = logging.getLogger(__name__)

__all__ = [
    "SRLPredictor",
]

Prediction = Dict[
    ontonotes_ontology.PredicateMention,
    List[Tuple[ontonotes_ontology.PredicateArgument, str]]]


class SRLPredictor(BatchProcessor):
    word_vocab: tx.data.Vocab
    char_vocab: tx.data.Vocab
    model: LabeledSpanGraphNetwork

    def __init__(self):
        super().__init__()

        self._ontology = ontonotes_ontology
        self.define_context()

        self.batch_size = 4
        self.batcher = self.initialize_batcher()

        self.device = torch.device(
            torch.cuda.current_device() if torch.cuda.is_available() else 'cpu')

    def initialize(self, configs: HParams, resource: Resources):  # pylint: disable=unused-argument

        model_dir = configs.storage_path
        logger.info("restoring SRL model from %s", model_dir)

        self.word_vocab = tx.data.Vocab(
            os.path.join(model_dir, "embeddings/word_vocab.english.txt"))
        self.char_vocab = tx.data.Vocab(
            os.path.join(model_dir, "embeddings/char_vocab.english.txt"))
        model_hparams = LabeledSpanGraphNetwork.default_hparams()
        model_hparams["context_embeddings"]["path"] = os.path.join(
            model_dir, model_hparams["context_embeddings"]["path"])
        model_hparams["head_embeddings"]["path"] = os.path.join(
            model_dir, model_hparams["head_embeddings"]["path"])
        self.model = LabeledSpanGraphNetwork(
            self.word_vocab, self.char_vocab, model_hparams)
        self.model.load_state_dict(torch.load(
            os.path.join(model_dir, "pretrained/model.pt"),
            map_location=self.device))
        self.model.eval()

    def define_context(self):
        self.context_type = self._ontology.Sentence

    def _define_input_info(self) -> ProcessInfo:
        input_info: ProcessInfo = {
            self._ontology.Token: []
        }
        return input_info

    def _define_output_info(self) -> ProcessInfo:
        output_info: ProcessInfo = {
            self._ontology.PredicateMention:
                ["pred_type", "span"],
            self._ontology.PredicateArgument: ["span"],
            self._ontology.PredicateLink:
                ["parent", "child", "arg_type"]
        }
        return output_info

    def predict(self, data_batch: Dict) -> Dict[str, List[Prediction]]:
        text: List[List[str]] = [
            sentence.tolist() for sentence in data_batch["Token"]["text"]]
        text_ids, length = tx.data.padded_batch([
            self.word_vocab.map_tokens_to_ids_py(sentence)
            for sentence in text])
        text_ids = torch.from_numpy(text_ids).to(device=self.device)
        length = torch.tensor(length, dtype=torch.long, device=self.device)
        batch_size = len(text)
        batch = tx.data.Batch(batch_size, text=text, text_ids=text_ids,
                              length=length, srl=[[]] * batch_size)
        self.model = self.model.cuda()
        batch_srl_spans = self.model.decode(batch)

        # Convert predictions into annotations.
        batch_predictions: List[Prediction] = []
        for idx, srl_spans in enumerate(batch_srl_spans):
            word_spans = data_batch["Token"]["span"][idx]
            predictions: Prediction = {}
            for pred_idx, pred_args in srl_spans.items():
                begin, end = word_spans[pred_idx]
                pred_annotation = self._ontology.PredicateMention(begin, end)
                arguments = []
                for arg in pred_args:
                    begin = word_spans[arg.start][0]
                    end = word_spans[arg.end][1]
                    arg_annotation = self._ontology.PredicateArgument(begin,
                                                                      end)
                    arguments.append((arg_annotation, arg.label))
                predictions[pred_annotation] = arguments
            batch_predictions.append(predictions)
        return {"predictions": batch_predictions}

    def pack(self, data_pack: DataPack,
             inputs: Dict[str, List[Prediction]]) -> None:
        batch_predictions = inputs["predictions"]
        for predictions in batch_predictions:
            for pred, args in predictions.items():
                pred = data_pack.add_or_get_entry(pred)
                for arg, label in args:
                    arg = data_pack.add_or_get_entry(arg)
                    link = self._ontology.PredicateLink(pred, arg)
                    link.set_fields(arg_type=label)
                    data_pack.add_or_get_entry(link)

    @staticmethod
    def default_hparams():
        """
        This defines a basic Hparams structure
        :return:
        """
        hparams_dict = {
            'storage_path': None,
        }
        return hparams_dict