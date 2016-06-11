from difflib import SequenceMatcher
from lxml import etree
import re
import os

def similar(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()
    
def merge(path):
    os.chdir(path)
    para_list = []
    cntr = 0
    for file in os.listdir(path):
        f1 = open(file, 'r', encoding = 'utf-8' )
        ftree = etree.fromstring(f1.read())
        for para in ftree.iter('para'):
            para.set('id', str(cntr))
            para_list.append(para)
            cntr += 1
            f1.close
    tree = etree.Element('html')
    head = etree.SubElement(tree, 'head')
    body = etree.SubElement(tree, 'body')
    for para in para_list:
        body.append(para)
    return tree
        
        
def correct(gstandard, output):
    f1 = open(gstandard, 'r', encoding = 'utf-8')
    gtree = etree.fromstring(f1.read())
    gse_list = gtree.xpath('.//se[@lang="en"]')
    for se in tree.xpath('.//se[@lang="uk"]'):
        i = tree.xpath('.//se[@lang="uk"]').index(se)
        for gse in gse_list:
            if se.text is not None:
                if gse.text is not None:
                    if se.text == gse.text:
                        print(i)
                        gse_list.remove(gse)
                        break
                    else:
                        if similar(se.text, gse.text) > 0.89:
                            tree.xpath('.//se[@lang="uk"]')[i].text = gse.text
                            gi = gse_list.index(gse)
                            if gi != 0:
                                gse_list = gse_list[gi:]
                            gse_list.remove(gse)
                            break
                        if similar(se.text, gse.text) > 0.4:
                            fullstop = gse.text.count('. ')
                            if fullstop > 0:
                                gsents = gse.text.split('. ')
                                if similar(se.text, gsents[0]) > 0.85:
                                    tree.xpath('.//se[@lang="uk"]')[i].text = gsents[0]+'.'
                                    break
                                if similar(se.text, gsents[1]) > 0.85:
                                    tree.xpath('.//se[@lang="uk"]')[i].text = gsents[1]
                                    break
                            if ('(' or ')' or ']' or '[' or '*' or '\\' or '\'' or '\"') in se.text:
                                break
                            else:
                                if len(se.text) > 15 and len(gse.text) > 20:
                                    regexp = se.text[0:2]+'.*'+se.text[-4:]
                                    if re.search(regexp, gse.text) is not None:
                                        check = re.search(regexp, gse.text).group(0)
                                        if se.text != check:
                                            tree.xpath('.//se[@lang="uk"]')[i].text = gse.text
                                            break
    f2 = open(output, 'w', encoding = 'utf-8')
    f2.write(etree.tostring(tree, pretty_print=True, encoding="utf-8").decode())
    f2.close()
        
if __name__=='__main__':
    tree = merge(path)
    correct(gstandard, output)
    