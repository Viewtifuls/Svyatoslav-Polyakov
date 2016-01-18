import re
dct = {}
page = open('irish.htm', encoding = 'utf-8').read()
page = page.replace('\n', '').replace('\t','')
forms = re.findall('(?<=Forms:).*?(?=<)', page)
forms = forms[0].replace(' ','')
forms = forms.split(',')
lemma = re.findall('headword_id=".*?">.*?<', page)
lemma = re.findall('(?<=>).*?(?=<)', lemma[0])
headid = re.findall('(?<=headword_)id=".*?"(?=>)', page)
for i in range(0, len(forms)):
    dct[forms[i]] = lemma
print('Лемма - '+lemma[0])
print(headid[0])
print('Формы: '+', '.join(forms))
print('Словарь:')
print(dct)
