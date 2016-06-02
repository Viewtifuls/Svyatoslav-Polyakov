import vk
from time import sleep
import pandas as pd

session = vk.AuthSession(app_id='', user_login='', user_password='')
api = vk.API(session)
ids = []
meta = 'ID\tfirst_name\tlast_name\tbdate\tsex\tcity\thome_town\tlangs\n'

def get_ids():
    query = api.users.search(hometown = 'Сольвычегодск', count = 1000)
    query.remove(query[0])
    for f in query:
        ids.append(f['uid'])
        
def get_texts():
    for i in ids:
        texts = ''
        data = api.wall.get(owner_id = i, filter = 'owner', count = 100)
        data.remove(data[0])
        for dct in data:
            if dct['post_type'] == 'post':
                texts = texts+dct['text']+'\n'*2
            if 'copy_text' in dct:
                texts = texts+dct['text']+'\n'*2
        f = open('id'+str(i)+'.txt', 'w', encoding = 'utf-8')
        f.write(texts)
        f.close
        sleep(0.20)

def get_meta():
    global meta
    for i in ids:
        check = api.users.get(user_id=i, fields = 'sex, bdate, city, home_town, personal')
        uid = str(check[0]['uid'])
        first_name = check[0]['first_name']
        last_name = check[0]['last_name']
        if 'bdate' in check[0]:
            bdate = check[0]['bdate']
        else: bdate = ' '
        sex = str(check[0]['sex'])
        city = str(check[0]['city'])
        if 'home_town' in check[0]:
            home_town = check[0]['home_town']
        else: home_town = ' '
        if 'personal' in check[0]:
            if 'langs' in check[0]['personal']:
                if len(check[0]['personal']['langs']) == 1:
                    langs = check[0]['personal']['langs'][0]
                else: langs = ', '.join(check[0]['personal']['langs'])
        else: langs = ' '
        meta = meta + uid + '\t' + first_name + '\t' + last_name + '\t' + bdate + '\t' + sex + '\t' + city + '\t' + home_town + '\t' + langs + '\n'
        sleep(0.30)
 
def meta_to_tsv():
    f = open('meta.tsv', 'w', encoding = 'utf-8')     
    f.write(meta)
    f.close

def sort_meta():
    df = pd.read_csv('meta.tsv', sep = '\t')
    df = df.sort(['ID'], ascending=True)
    df.to_csv('D:\\test.csv', index = False, sep = '\t', encoding = 'UTF-8')
    
          
get_ids()
get_texts()
get_meta()
meta_to_tsv()
sort_meta()
