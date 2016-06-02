import glob
import os
dir_list = []
file_names = []
for root, directories, filenames in os.walk(os.getcwd()): #создаем список всех папок нашего корпуса
    for directory in directories:
        dir_list.append(os.path.join(root, directory)) 
for directory in dir_list: #создаем такие же папки, для будущего размеченного корпуса
    os.mkdir(directory.replace('nomarks', 'marked'))
    os.mkdir(directory.replace('nomarks', 'xml'))
os.chdir('nomarks') #Переходим в неразмеченный корпус
for file in glob.glob("**\\**\\*.txt"): #записываем относительный путь каждого файла
    file_names.append(file.replace('.txt', ''))
os.chdir(os.path.dirname(os.getcwd())) #переходим на уровень выше
path = os.getcwd() #записываем абсолютный путь, в котором мы находимся
mystem = '\"D:\mystem.exe -cid '
for file in file_names:
    In = path+'\\nomarks\\'+file+'.txt'+' '
    Out1 = path+'\\marked\\'+file+'.txt'+'\"'
    Out2 = path+'\\xml\\'+file+'.xml'+'\"'
    os.system(mystem+In+Out1)
    os.system(mystem+'--format xml '+In+Out2)