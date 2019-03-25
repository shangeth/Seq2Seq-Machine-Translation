# Seq2Seq-Machine-Translation

![](https://smerity.com/media/images/articles/2016/gnmt_arch_1_enc_dec.svg)

```
git clone https://github.com/shangeth/Seq2Seq-Machine-Translation.git
cd Seq2Seq-Machine-Translation
mkdir trained_model
```

Check [DEMO Notebook](./DEMO.ipynb)

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
```
135842 translation pairs found in dataset.
Reduced dataset to 135690 translation pairs.
No of words in each language:
eng 12996
fra 21267

Starting Training Loop...
3m 44s (- 0m 0s) (5000 100%) 5.0887
```
## Translationg English sentence to French with the trained model.
make sure the saved model exists in trained_model/ directory/

```
python translate.py -h
```
```
usage: translate.py [-h] [--translate_sentence TRANSLATE_SENTENCE]

optional arguments:
  -h, --help            show this help message and exit
  --translate_sentence TRANSLATE_SENTENCE
                        sentence to translate

```

```
!python translate.py --translate_sentence='This is my sister!'
```
```
135842 translation pairs found in dataset.
Reduced dataset to 135690 translation pairs.
No of words in each language:
eng 12996
fra 21267
input = this is my sister !
output = je ne que vous vous pas <EOS>
```
