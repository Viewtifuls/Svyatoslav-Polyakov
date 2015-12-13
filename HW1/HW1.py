replacements = {'ბ':'b', 'დ':'d', 'ძ':'dz', 'ჯ':'dʒ', 'გ':'ɡ', 'ღ':'ɣ', 'ჰ':'h', 'კ':'kʼ', 'ქ':'kʰ', 'ლ':'l', 'მ':'m', 'ნ':'n', 'პ':'pʼ', 'ფ':'pʰ', 'ყ':'qʼ', 'რ':'r', 'ს':'s', 'შ':'ʃ', 'ტ':'tʼ', 'თ':'tʰ', 'წ':'tsʼ', 'ც':'tsʰ', 'ჭ':'tʃʼ', 'ჩ':'tʃʰ', 'ვ':'v', 'ხ':'x', 'ზ':'z', 'ჟ':'ʒ', 'ა':'ɑ',  'ე':'ɛ', 'ი':'i', 'ო':'ɔ', 'უ':'u',}

with open('georgian.txt', encoding ='utf-8') as infile, open('result.txt', 'w', encoding ='utf-8') as outfile:
    for line in infile:
        for src, target in replacements.items():
            line = line.replace(src, target)
        outfile.write(line)
		
	

    
