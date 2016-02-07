import glob
import os
import pandas
from pymystem3 import Mystem
df = pandas.read_table('table.tsv')
df['Название статьи (lemma)'] = df['Название статьи']
m = Mystem()
lemma = df['Название статьи (lemma)']
for index in range(0, len(lemma)):
    lemma[index] = ''.join(m.lemmatize(lemma[index])).replace('\n', '')
df.to_csv('new_table.tsv', sep = '\t', encoding = 'utf-8', index = False)
dir_list = []
for root, directories, filenames in os.walk(os.getcwd()): #создаем список всех папок нашего корпуса
    for directory in directories:
        dir_list.append(os.path.join(root, directory)) 
for directory in dir_list: #создаем такие же папки, для будущего размеченного корпуса
    os.mkdir(directory.replace('nomarks', 'marked'))
os.chdir('nomarks') #Переходим в неразмеченный корпус
file_names = glob.glob("**\\**\\*.txt") #записываем относительный путь каждого файла
os.chdir(os.path.dirname(os.getcwd())) #переходим на уровень выше
path = os.getcwd() #записываем абсолютный путь, в котором мы находимся
mystem = '\"D:\mystem.exe -ni '
for file in file_names:
    In = path+'\\nomarks\\'+file+' ' 
    Out = path+'\\marked\\'+file+'\"'
    os.system(mystem+In+Out)