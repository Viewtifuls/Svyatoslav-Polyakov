import re
from urllib.request import urlopen
page = urlopen("http://desnyanka.ru/").read().decode()
regexp = '(?<=href=[\"\'])http://desnyanka.ru(?:[^\'\"\.а-я-]-?)*?(?:\.html|/+)(?=[\'\"])'
visited = list(set(re.findall(regexp, page)))
page_list = []
not_visited = []
for url in visited:
    page = urlopen(url).read().decode()
    f=open("file_" + str(visited.index(url)) + ".txt", 'w', encoding='utf-8')
    f.write(page)
    page_list.append(page)
for page in page_list:
    not_visited.extend(re.findall(regexp,page))
    page_list.remove(page)
not_visited = list(set(not_visited))
for url in not_visited:
    if url in visited:
        not_visited.remove(url)
while not_visited is not []:
    for url in not_visited:
        page = urlopen(url).read().decode()
        page_list.append(page)
        visited.append(url)
        f=open("file_" + str(visited.index(url)) + ".txt", 'w', encoding='utf-8')
        f.write(page)
        for page in page_list: 
            not_visited.extend(re.findall(regexp,page))
            page_list.remove(page)
            not_visited = list(set(not_visited))
            for url in not_visited:
                if url in visited:
                    not_visited.remove(url)
  
            



