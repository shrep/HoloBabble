# HoloClean
This repo builds on an implementation of SQLNet for predicting SQL constraints for Natural Language descriptions. (https://github.com/xiaojunxu/SQLNet).

These SQL translations are used as constraints for the downstream task of data cleaning and repairing. (https://hazyresearch.github.io/snorkel/blog/holoclean.html)




## Installation
The WikiSQL data is in `data.tar.bz2`. Unzip the code by running
```bash
tar -xjvf data.tar.bz2
```

The code is written using PyTorch in Python 2.7. Check [here](http://pytorch.org/) to install PyTorch. You can install other dependency by running 
```bash
pip install -r requirements.txt
```

## Downloading the glove embedding.
Download the pretrained glove embedding from [here](https://github.com/stanfordnlp/GloVe) using
```bash
bash download_glove.sh
```

## Extract the glove embedding for training.
Run the following command to process the pretrained glove embedding for training the word embedding:
```bash
python extract_vocab.py
```

## Train
The training script is `train.py`. To see the detailed parameters for running:
```bash
python train.py -h
```

Some typical usage are listed as below:
Train a SQLNet model with column attention to predict constraints instead of queries:
```bash
python train.py --ca --constraint
```


Train a SQLNet model on WikiSQL with column attention:
```bash
python train.py --ca
```

Train a SQLNet model with column attention and trainable embedding on WikiSQL (requires pretraining without training embedding, i.e., executing the command above):
```bash
python train.py --ca --train_emb
```

