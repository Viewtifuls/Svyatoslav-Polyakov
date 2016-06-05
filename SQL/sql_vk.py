import pymysql
import pandas as pd
conn = pymysql.connect(host = 'localhost', user = 'guest1', passwd = '', db = 'guest1_polyakov_hw_sql', charset = 'utf8')
cur = conn.cursor()
df = pd.read_csv('meta.tsv', sep = '\t')
df['ID'] = df['ID'].replace({'id': ''}, regex=True)

def create_tables():
    cur.execute('CREATE TABLE main(`vk_ID` INT(10), `name_ID` INT(10), `surname` VARCHAR(255), `bdate` VARCHAR(255), `sex_ID` INT(10), `city_ID` INT(10), PRIMARY KEY(`vk_ID`)) DEFAULT CHARSET = utf8;')
    cur.execute('CREATE TABLE name(`name_ID` INT(10), `name` VARCHAR(255),  PRIMARY KEY(`name_ID`)) DEFAULT CHARSET = utf8;')
    cur.execute('CREATE TABLE sex(`sex_ID` INT(10), `sex` VARCHAR(255), PRIMARY KEY(`sex_ID`)) DEFAULT CHARSET = utf8;')
    cur.execute('CREATE TABLE city(`city_ID` INT(10), `city` VARCHAR(255), PRIMARY KEY(`city_ID`)) DEFAULT CHARSET = utf8;')
    
def related_tables(col_name):
    """
    Принимает на вход имя колонки датафрейма,
    
    проверяет какие значения являются уникальными,
    
    возвращает часть запроса для вставки новых строк в таблицу[1]
    
    в виде (ID, unique value), а также массив уникальных значений[2]

    :param col_name: имя колонки датафрейма(строка)
    :return:
    """
    unique_data = df[col_name].unique().tolist()
    query = ''
    cntr = 0
    while cntr < len(unique_data):
        query = query + '(' + str(cntr+1) + ', ' + '\'' + str(unique_data[cntr]) + '\'' + ')' + ', '
        cntr += 1    
    return(query[:-2]+';', unique_data)

def main_table():
    """
    Возвращает часть запроса для вставки новых строк в таблицу main
    :return:
    """
    query = ''
    cntr = 0
    name = related_tables('first_name')[1]
    city = related_tables('city')[1]
    sex = related_tables('sex')[1]
    while cntr < len(df):
        query = query + '(' + str(df.ID[cntr]) + ', ' + str(name.index(df.first_name[cntr])+1) + ', ' + '\'' + str(df.last_name[cntr]) + '\'' + ', ' + '\'' + str(df.bdate[cntr]) + '\'' + ', ' + str(sex.index(df.sex[cntr])+1) + ', ' + str(city.index(df.city[cntr])+1) + ')' + ', '
        cntr += 1
    return(query[:-2]+';')

def main():
    '''
    Вставляет новые строки в таблицы main, name, sex, city
    
    '''
    insert_main = 'INSERT INTO main(`vk_ID`, `name_ID`, `surname`, `bdate`, `sex_ID`, `city_ID`) VALUES ' + main_table()
    insert_name = 'INSERT INTO name(`name_ID`, `name`) VALUES ' + related_tables('first_name')[0]
    insert_sex = 'INSERT INTO sex(`sex_ID`, `sex`) VALUES ' + related_tables('sex')[0]
    insert_city = 'INSERT INTO city(`city_ID`, `city`) VALUES ' + related_tables('city')[0]
    cur.execute(insert_main)
    cur.execute(insert_name)
    cur.execute(insert_sex)
    cur.execute(insert_city)
    
if __name__ == "__main__":
    create_tables()
    main()
    conn.commit()