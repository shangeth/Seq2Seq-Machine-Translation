from io import open
import unicodedata
import string
import re
import random


class Language:
    def __init__(self, name):
        '''
        class to get index2word, word2index, wordcount of a language
        '''
        self.name = name
        self.word2index = {}
        self.word2count = {}
        self.index2word = {0: "SOS", 1: "EOS"}
        self.n_words = 2 
    def addSentence(self, sentence):
        for word in sentence.split(' '):
            self.addWord(word)
    def addWord(self, word):
        if word not in self.word2index:
            self.word2index[word] = self.n_words
            self.word2count[word] = 1
            self.index2word[self.n_words] = word
            self.n_words += 1
        else:
            self.word2count[word] += 1


def unicodeToAscii(s):
    '''
    to remove all unicodes and foreign language's accent characters
    '''
    return ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn'
    )


def process_sentence(s):
    '''
    remove other chars and lowecase the sentence.
    '''
    s = unicodeToAscii(s.lower().strip())
    s = re.sub(r"([.!?])", r" \1", s)
    s = re.sub(r"[^a-zA-Z.!?]+", r" ", s)
    return s


def readLangs(lang1, lang2, reverse=False):
    '''
    read data file and get pairs of english-french translation
    '''
    lines = open('data/%s-%s.txt' % (lang1, lang2), encoding='utf-8').\
        read().strip().split('\n')
    pairs = [[process_sentence(s) for s in l.split('\t')] for l in lines]
    if reverse:
        pairs = [list(reversed(p)) for p in pairs]
        input_lang = Language(lang2)
        output_lang = Language(lang1)
    else:
        input_lang = Language(lang1)
        output_lang = Language(lang2)
    return input_lang, output_lang, pairs


def filterPair(p):
    '''drop data if len of words are more than MAX_LENGTH'''
    MAX_LENGTH = 25
    return len(p[0].split(' ')) < MAX_LENGTH and len(p[1].split(' ')) < MAX_LENGTH

    
def filterPairs(pairs):
    '''drop data if len of words are more than MAX_LENGTH'''
    return [pair for pair in pairs if filterPair(pair)]


def prepareData(lang1, lang2, reverse=False):
    input_lang, output_lang, pairs = readLangs(lang1, lang2, reverse)
    print("%s translation pairs found in dataset." % len(pairs))
    pairs = filterPairs(pairs)
    print("Reduced dataset to %s translation pairs." % len(pairs))
    for pair in pairs:
        input_lang.addSentence(pair[0])
        output_lang.addSentence(pair[1])
    print("No of words in each language:")
    print(input_lang.name, input_lang.n_words)
    print(output_lang.name, output_lang.n_words)
    return input_lang, output_lang, pairs



def main():
    input_lang, output_lang, pairs = prepareData('eng', 'fra')

if __name__ == '__main__':
    main()