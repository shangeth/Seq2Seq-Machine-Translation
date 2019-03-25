# Seq2Seq-Machine-Translation

![](https://smerity.com/media/images/articles/2016/gnmt_arch_1_enc_dec.svg)

```
git clone https://github.com/shangeth/Seq2Seq-Machine-Translation.git
cd Seq2Seq-Machine-Translation
mkdir trained_model
```

## Training the model
Place the data in data/ directory.

```
python train.py -h
```
```
usage: train.py [-h] [--epochs EPOCHS] [--lr LR]

optional arguments:
  -h, --help       show this help message and exit
  --epochs EPOCHS  no of epochs to train
  --lr LR          learning rate
```

Change the hyperparameters as needed and optimizer in the train.py file and train the model. Data preprocessing will be done before training.
```
python train.py --epoch=5000 --lr=0.0001
```
