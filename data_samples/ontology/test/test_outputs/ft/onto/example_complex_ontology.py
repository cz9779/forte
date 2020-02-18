# ***automatically_generated***
# flake8: noqa
# mypy: ignore-errors
# pylint: skip-file
"""


Automatically generated ontology . Do not change manually.
"""

from forte.data.base_pack import PackType
from forte.data.ontology.core import Entry
from forte.data.ontology.top import Annotation
from forte.data.ontology.top import Link
from typing import List
from typing import Optional


__all__ = [
    "Token",
    "Sentence",
    "Document",
    "Dependency",
]


class Token(Annotation):
    """

    Attributes:
        _lemma (Optional[str])
        _is_verb (Optional[bool])
        _num_chars (Optional[int])
        _score (Optional[float])

    """

    def __init__(self, pack: PackType, begin: int, end: int):
        super().__init__(pack, begin, end)
        self._lemma: Optional[str] = None
        self._is_verb: Optional[bool] = None
        self._num_chars: Optional[int] = None
        self._score: Optional[float] = None

    def __getstate__(self): 
        state = super().__getstate__()
        state['lemma'] = self._lemma
        state['is_verb'] = self._is_verb
        state['num_chars'] = self._num_chars
        state['score'] = self._score
        return state

    def __setstate__(self, state): 
        state = super().__setstate__(state)
        self._lemma = state.get('lemma', None) 
        self._is_verb = state.get('is_verb', None) 
        self._num_chars = state.get('num_chars', None) 
        self._score = state.get('score', None) 

    @property
    def lemma(self):
        return self._lemma

    @lemma.setter
    def lemma(self, lemma: Optional[str]):
        self.set_fields(_lemma=lemma)

    @property
    def is_verb(self):
        return self._is_verb

    @is_verb.setter
    def is_verb(self, is_verb: Optional[bool]):
        self.set_fields(_is_verb=is_verb)

    @property
    def num_chars(self):
        return self._num_chars

    @num_chars.setter
    def num_chars(self, num_chars: Optional[int]):
        self.set_fields(_num_chars=num_chars)

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, score: Optional[float]):
        self.set_fields(_score=score)


class Sentence(Annotation):
    """

    Attributes:
        _key_tokens (Optional[List[int]])

    """

    def __init__(self, pack: PackType, begin: int, end: int):
        super().__init__(pack, begin, end)
        self._key_tokens: Optional[List[int]] = []

    def __getstate__(self): 
        state = super().__getstate__()
        state['key_tokens'] = self._key_tokens
        return state

    def __setstate__(self, state): 
        state = super().__setstate__(state)
        self._key_tokens = state.get('key_tokens', None) 

    @property
    def key_tokens(self):
        return self._key_tokens

    @key_tokens.setter
    def key_tokens(self, key_tokens: Optional[List[Token]]):
        self.set_fields(_key_tokens=[self.__pack.add_entry_(obj) for obj in key_tokens])

    def num_key_tokens(self):
        return len(self._key_tokens)

    def clear_key_tokens(self):
        [self.__pack.delete_entry(self.__pack.get_entry(tid)) for tid in self._key_tokens]
        self._key_tokens.clear()

    def add_key_tokens(self, a_key_tokens: Token):
        self._key_tokens.append(self.__pack.add_entry_(a_key_tokens))


class Document(Annotation):
    """


    """

    def __init__(self, pack: PackType, begin: int, end: int):
        super().__init__(pack, begin, end)

    def __getstate__(self): 
        state = super().__getstate__()
        return state

    def __setstate__(self, state): 
        state = super().__setstate__(state)


class Dependency(Link):
    """

    Attributes:
        _rel_type (Optional[str])

    """

    def __init__(self, pack: PackType, parent: Optional[Entry] = None, child: Optional[Entry] = None):
        super().__init__(pack, parent, child)
        self._rel_type: Optional[str] = None

    def __getstate__(self): 
        state = super().__getstate__()
        state['rel_type'] = self._rel_type
        return state

    def __setstate__(self, state): 
        state = super().__setstate__(state)
        self._rel_type = state.get('rel_type', None) 

    @property
    def rel_type(self):
        return self._rel_type

    @rel_type.setter
    def rel_type(self, rel_type: Optional[str]):
        self.set_fields(_rel_type=rel_type)
