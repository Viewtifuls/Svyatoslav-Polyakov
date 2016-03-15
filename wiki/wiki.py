import os
import nltk
from bs4 import BeautifulSoup
import pandas as pd
import re

def extract(inpt, out):
    #
    # принимает на вход путь к дампу и куда мы хотим положить результат
    python = '\"C:\\Python27\\python.exe '
    wiki = 'D:\\WikiExtractor.py '
    out = '-o '+out
    inpt = '\t'+inpt+'\"'
    os.system(python+wiki+out+inpt)

def clean(path):
    #
    #чистит файлы от оставшегося мусора, токенизирует
    texts = []
    for filename in os.listdir(path):
        f = open(path+'\\'+ filename, encoding = 'utf-8').read()
        texts.append(BeautifulSoup(f).get_text())
    text = '\n'.join(texts)
    text = text.lower()
    text = re.sub('[\W0-9]', ' ', text)
    tokens = nltk.word_tokenize(text)
    return tokens

def freq(tokens):
    #
    #строит частотный список и создает таблицу tsv
    freq_list = []
    for token in set(tokens):
        freq_list.append((token, tokens.count(token)))
    df = pd.DataFrame(freq_list, columns=['Word', 'Frequency'])
    df = df.sort(['Frequency'], ascending=False)
    df.to_csv('table.tsv', sep = '\t', index=False, encoding = 'utf-8')
    
extract('D:\\ruwikibooks.xml', 'D:\\out')
tokens = clean('D:\\out\\AA')
freq(tokens)