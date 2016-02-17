import pandas as pd
import numpy as np
df = pd.read_table('table.tsv')
years = []
for i in df['created']:
    year = i[-4:]
    years.append(year)
df['sex'] = np.nan
df['birthday'] = np.nan
df['sphere'] = 'публицистика'
df['genre_fi'] = np.nan
df['type'] = np.nan
df['chronotop'] = np.nan
df['style'] = 'нейральный'
df['audience_age'] = 'н-возраст'
df['audience_level'] = 'н-уровень'
df['audience_size'] = 'районная'
df['publication'] = 'Деснянская правда'
df['publisher'] = np.nan
df['publ_year'] = years
df['medium'] = 'газета'
df['country'] = 'Россия'
df['region'] = 'Брянская область'
df['language'] = 'ru'
df = df[['path', 'author', 'sex', 'birthday', 'header', 'created', 'sphere',
         'genre_fi', 'type', 'topic', 'chronotop', 'style', 'audience_age',
         'audience_level', 'audience_size', 'source', 'publication', 'publisher',
         'publ_year', 'medium', 'country', 'region','language']]
df.to_csv('table.csv', sep = '\t', index=False, encoding = 'utf-8')