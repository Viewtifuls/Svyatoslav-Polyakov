import lxml.html
import re

def create_dict(path):
    f1 = open(path, encoding = 'utf-8').readlines()
    f1 = f1[30:]
    for i in f1:
        temp_list = i.split(' ', 2)
        trans = re.search('\[.*?\]', temp_list[2]).group(0)[1:-1]
        sem = re.search('(?<=/).*(?=/)', temp_list[2]).group(0)
        temp_list[0], temp_list[1] = temp_list[1], temp_list[0]
        temp_list[1] = trans
        temp_list[2] = sem
        temp_list[2] = temp_list[2].replace('/', ', ')
        if temp_list[0] in dct:
            dct[temp_list[0]].append(temp_list[1:])
        else:
            dct[temp_list[0]] = [temp_list[1:]]

def parse(path, out):
    f = open(path, encoding = 'utf-8')
    tree = lxml.html.fromstring(f.read())
    text = '<?xml version=\"1.0\" encoding="utf-8"?>\n<html>\n<head>\n</head>\n<body>'
    for se in tree.xpath(".//se/text()"):
        cntr = 1
        text = text + '\n<se>'
        while len(se)>0:
            if len(se) == 1:
                word = se
            else:
                word = se[:-cntr]
            if word in dct:
                if len(dct[word]) == 1:
                    text = text + '\n<w><ana lex=\"'+word+'\" transcr=\"'+dct[word][0][0]+'\" sem=\"'+dct[word][0][1]+'\"/>'+word+'</w>'
                else: 
                    text = text + '\n<w>'
                    for i in range(0, len(dct[word])):
                        text = text + '<ana lex=\"'+word+'\" transcr=\"'+dct[word][i][0]+'\" sem=\"'+dct[word][i][1]+'\"/>'
                    text = text + word +'</w>'
                se = se[len(word):]
                cntr = 1               
            else:
                if len(word) == 1:
                    text = text+word
                    se = se[len(word):]
                    cntr = 1
                else:
                    cntr += 1
        text = text + '</se>'
    f.close()
    text = text + '\n</body>\n</html>'
    f2 = open(out ,'w', encoding = 'utf-8')
    f2.write(text)
    f2.close()

if __name__ == "__main__":
    dct = {}
    create_dict('cedict_ts.u8')
    parse('stal.xml', 'out.xml')    