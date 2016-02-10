import json
import os
dicts = []
months = []
Dict = {}
years = os.listdir('D:\\HSE\Python\\rep\\mystem\\marked')
for year in years:
    for root, dirs, filenames in os.walk(os.getcwd()+'\\'+year):
        if len(dirs) != 0:
            months.extend(dirs)
        if len(dirs) == 0:
            for month in set(months):
                if month in root:
                    if year not in Dict:
                        Dict.update({year:{'month':{month:filenames}}})
                    else:
                        Dict[year]['month'].update({month:filenames})
    dicts.append(Dict)
    Dict={}
f = open('D:\\tree.json','w')
json.dump(dicts,f, ensure_ascii = False, indent = 2)
f.close()