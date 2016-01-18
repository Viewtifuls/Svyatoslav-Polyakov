table = open('table.tsv', 'r', encoding = 'utf-8')
lines = [line.split() for line in table]#что-то вроде матрицы m x n
dct = {}
for i in range(1,len(lines)):
        for j in range(1, len(lines[i])):
            vowel = lines[0][j]
            consonant = lines[i][0]
            dct[lines[i][j]] = consonant+vowel
table.close()
with open('amh.txt', encoding ='utf-8') as infile, open('result.txt', 'w', encoding ='utf-8') as outfile:
    for line in infile:
        for src, target in dct.items():
            line = line.replace(src, target)
        outfile.write(line)
