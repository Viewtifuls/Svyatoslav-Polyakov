import lxml.html
import os
import re
from urllib.request import urlopen
page = urlopen("http://desnyanka.ru/").read().decode()
tree = lxml.html.fromstring(page)
months = {'Январь': 'January', 'Февраль': 'February',
          'Март': 'March', 'Апрель': 'April', 'Май': 'May',
          'Июнь': 'June', 'Июль': 'July', 'Август': 'August',
          'Сентябрь': 'September', 'Октябрь': 'October',
          'Ноябрь': 'November','Декабрь': 'December'}
visited = []
html_list = []
not_visited = []
for a in tree.iter("a"):
    if a.get("href") not in not_visited:
        if 'http://desnyanka.ru/2' in a.get("href"):
            not_visited.append(a.get("href"))
        if 'http://desnyanka.ru' in a.get("href") and '.html' in a.get("href") and '..' and '--' and '#' not in a.get("href"):
            if a.get("href") not in html_list:
                html_list.append(a.get("href"))
while len(not_visited) >0:
    for url in not_visited:
        page = urlopen(url).read().decode()
        visited.append(url) 
        tree = lxml.html.fromstring(page)
        for a in tree.iter("a"):
            if a.get("href") is not None:
                if a.get("href") not in not_visited:
                    if 'http://desnyanka.ru/2' in a.get("href"):
                        not_visited.append(a.get("href"))
                    if 'http://desnyanka.ru' in a.get("href") and '.html' in a.get("href") and '..' not in a.get("href") and '--' and '#' not in a.get("href") and 'а' not in a.get("href") and  'ы' not in a.get("href") and 'у' not in a.get("href"):
                        if a.get("href") not in html_list:
                            html_list.append(a.get("href"))
                    for url in not_visited:
                        if url in visited:
                            not_visited.remove(url)
for url in html_list:
    if '--' in url:
        html_list.remove(url)
for url in html_list:
    if '--' in url:
        html_list.remove(url)
for url in html_list:
    if '.P' in url:
        html_list.remove(url)
for url in html_list:
    if '.k' in url:
        html_list.remove(url)
tsv = '"Название статьи"\t"Дата публикации"\t"Автор статьи"\t"Рубрика"\t"Путь к файлу"\n'
for url in html_list:
    page = urlopen(url).read().decode()
    tree = lxml.html.fromstring(page) 
    date = (re.search('(?<=\s-\s).*П', tree.xpath('.//span[@class="post-date"]/text()')[0])).group(0)
    year = (re.search('2[0-9]{3}', date)).group(0)
    month = (re.search('.*?(?=\s)', date)).group(0)
    month = months[month]
    title = re.search('.*(?=\s\|)', tree.findtext('.//title')).group(0)
    name = re.sub('[:*?"/<>|»]', '', title)
    if len(tree.xpath('.//p[@style="text-align: right"]')) != 0:
        author = tree.xpath('.//p[@style="text-align: right"]')[0].text_content()
    else: author = '-'
    if tree.findtext('.//a[@rel="category tag"]') is not None:
        topic = tree.findtext('.//a[@rel="category tag"]')
    else: topic = '-'
    text = []
    for i in tree.xpath('.//p'):
        if '\r' not in i.text_content():
            text.append(i.text_content())
    text = '\n'.join(text)
    filename = year+'/'+month+'/'+ str(html_list.index(url)) + '.txt'
    tsv = tsv + '"' + title + '"' + '\t' + '"' + date + '"' + '\t'+ '"' + author + '"' + '\t' + '"' + topic + '"' + '\t' + '"' + filename + '"''\n'
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding = 'utf-8') as f:
        f.write(text)
        f.close
f=open('table.tsv', 'w', encoding ='utf-8')
f.write(tsv)
f.close()