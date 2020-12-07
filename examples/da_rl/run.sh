# under examples/da_rl dir
# prepare data
python download_imdb.py
python utils/imdb_format.py --raw_data_dir=data/IMDB_raw/aclImdb --train_id_path=data/IMDB_raw/train_id_list.txt --output_dir=data/IMDB
python prepare_dataset.py
# run model
python main.py --do-train --do-eval --do-test