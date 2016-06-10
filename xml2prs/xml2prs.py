from sys import argv
import re
import pandas as pd
from io import StringIO
from lxml import etree

def prs2xml(inpt, outpt):
    f1 = open(inpt, 'r', encoding = 'utf-8').readlines()
    temp = f1[10:] #таблица без лишней метаинформации
    f1 = f1[:1] #заголовки таблицы
    f1.extend(temp)
    f1 = ''.join(f1)
    f1 = StringIO(f1)
    df = pd.read_csv(f1, sep="\t")
    root = etree.Element("body")
    for i in range(0, len(df)):
        if df.ix[i]['#wordno'] == 1 and df.ix[i]['#nvar'] == 1:
            sent = etree.SubElement(root, 'se')
        if df.ix[i]['#nvar'] == 1:
            word = etree.SubElement(sent, 'word')
            ana = etree.SubElement(word, 'ana')
            ana.set('lex',  df.ix[i]['#lem'])
            morph = re.search('[^A-Z_0-9 ].*', df.ix[i]['#gram']).group()
            morph = re.sub('^ +(?=[^\s])', '', morph)
            morph = re.sub(' syll.', '', morph) #убрав эту строку можно при необходимости сохранить syll8 и тд
            if len(morph) != 0:
                ana.set('morph', morph)
            gr = re.search('[A-Z_0-9 ]*', df.ix[i]['#gram']).group().lower()
            if gr[-1] == ' ':
                gr = gr[:-1]
            gr = df.ix[i]['#lex'] + ' ' + gr
            ana.set('gr', gr)
        if df.ix[i]['#nvars'] == df.ix[i]['#nvar']:
            ana.tail = df.ix[i]["#word"]
            if type(df.ix[i]['#punctr']) is not float: #чтобы исключить nan
                word.tail = df.ix[i]['#punctr']
            else:
                word.tail = ''
    f2 = open(outpt, 'w', encoding = 'utf-8')
    text = etree.tostring(root, pretty_print=True, encoding="utf-8").decode()
    f2.write(text)
    f2.close()
    

def xml2prs(inpt, outpt):
    text = '#sentno	#wordno	#lang	#graph	#word	#indexword	#nvars	#nlems	#nvar	#lem	#trans	#trans_ru	#lex	#gram	#flex	#punctl	#punctr	#sent_pos'
    f1 = open(inpt, 'r', encoding = 'utf-8')
    tree = etree.fromstring(f1.read())
    sentno = 0
    for sent in tree.iter('se'):
        sentno += 1
        wordno = 0
        for wordxml in sent.iter('w'):
            word = wordxml.xpath("string()").strip()
            if word[0].isupper():
                graph = 'cap'
            else:
                graph = ''
            wordno += 1
            lang = ''
            nvar = 0
            lem_list = []
            for ana in wordxml.iter('ana'):
                if ana.get('lex') not in lem_list:
                    lem_list.append(ana.get('lex'))
            nlem = len(lem_list) 
            for ana in wordxml.iter('ana'):
                indexword = ''
                nvars = len(list(wordxml.iter('ana')))
                nvar += 1
                lem = ana.get('lex')
                trans = ana.get('trans')
                trans_ru = ''
                gram = ana.get('gr')
                if ',' in gram:
                    lex, gram = gram.split(',', 1)
                else:
                    lex = gram
                    gram = ''
                gram = gram.upper()
                gram = re.sub('[^A-Z|0-9]', ' ', gram)
                if ana.get('morph'):
                    gram = gram + ' ' + ana.get('morph')
                flex = ''
                punctl = ''
                if wordxml.tail:
                    punctr = wordxml.tail.strip()
                else:
                    punctr = ''
                if wordno == 1:
                    sent_pos = 'bos'
                else:
                    if wordno == len(list(sent)):
                        sent_pos = 'eos'
                    else:
                        sent_pos = ''
                line = str(sentno), str(wordno), lang, graph, word, indexword, str(nvars), str(nlem), str(nvar), lem, trans, trans_ru, lex, gram, flex, punctl, punctr, sent_pos
                line = '\t'.join(line)
                text = text + '\n' + line
    f1.close()
    f2 = open(outpt, 'w', encoding = 'utf-8')
    f2.write(text)
    f2.close

def main(argv):
    '''Usage
    python xml2prs.py infile outfile
    '''
    if len(argv) == 3:
        if '.xml' in argv[2]:
            prs2xml(argv[1], argv[2])  
        if '.prs' in argv[2]:
            xml2prs(argv[1], argv[2])
    else: 
        print(main.__doc__)   
		
if __name__=='__main__':
    main(argv)