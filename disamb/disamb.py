import re
class Info(object):
    def __init__(self, path):
        with open(path,'r', encoding = 'utf-8') as f:
            text = f.readlines()
        self.lines = text
        self.path = path
        self.case = {} #ключ - предлог, значение - падеж без числа
        self.case2 = {} #ключ - предлог, значение - падеж с числом
        self.prs = []
    def parse(self):
        for line in self.lines:
            if '=PR=' in line:
                pr = re.search('(?<=\{).*(?==PR=)', line).group(0)
                if pr not in self.prs:
                    self.prs.append(pr)
        for pr in self.prs:
            case_list = []
            for i in range(0, len(self.lines)):
                if pr+'=PR=' in self.lines[i]:
                    if '=S,' in self.lines[i+1]:
                        temp = re.search('(?<=од=\().*(?=\))', self.lines[i+1])
                        if temp is not None:
                            temp_list = temp.group(0).split('|')
                            case_list.extend(temp_list)
                        else:
                            temp = re.search('(?<=од=).*(?=\})', self.lines[i+1])
                            if temp is not None:
                                case_list.append(temp.group(0))
                    else:
                        if '=SPRO' not in self.lines[i+1]:
                            if '=S,' in self.lines[i+2]:
                                temp = re.search('(?<=од=\().*(?=\))', self.lines[i+2])
                                if temp is not None:
                                    temp_list = temp.group(0).split('|')
                                    case_list.extend(temp_list)
                                else:
                                    temp = re.search('(?<=од=).*(?=\})', self.lines[i+2])
                                    if temp is not None:
                                        case_list.append(temp.group(0))                            
            if len(case_list) > 0:
                self.case2[pr] = max(set(case_list), key=case_list.count)
                for i in range(0, len(case_list)):
                    if ',' in case_list[i]:
                        case_list[i] = case_list[i].split(',')[0]
                self.case[pr] = max(set(case_list), key=case_list.count)

class Disamb(Info):
    def __init__(self, path):
        super().__init__(path)
    def disamb(self):
        for i in range(0, len(self.lines)):
            if '=PR=' in self.lines[i]:
                pr = re.search('(?<=\{).*(?==PR=)', self.lines[i]).group(0)
                if pr in self.case:
                    if '=S,' in self.lines[i+1]:
                        temp = re.search('(?<=од=)\(.*\)', self.lines[i+1])
                        if temp is not None:
                            if self.case[pr] in temp.group(0):                                      
                                count = temp.group(0).count(pr)
                                if count == 2:
                                    self.lines[i+1] = self.lines[i+1].replace(temp.group(0), self.case2[pr])
                                else:
                                    case = re.search(self.case[pr]+',[а-я]*', temp.group(0))
                                    if case is not None:
                                        case = case.group(0)
                                    else:
                                        case = self.case[pr]
                                    self.lines[i+1] = self.lines[i+1].replace(temp.group(0), case)
                    else:
                        if '=SPRO' not in self.lines[i+1]:
                            if '=S,' in self.lines[i+2]:
                                temp = re.search('(?<=од=)\(.*\)', self.lines[i+2])
                                if temp is not None:
                                    if self.case[pr] in temp.group(0):                                      
                                        count = temp.group(0).count(pr)
                                        if count == 2:
                                            self.lines[i+2] = self.lines[i+2].replace(temp.group(0), self.case2[pr])
                                        else:
                                            case = re.search(self.case[pr]+',[а-я]*', temp.group(0))
                                            if case is not None:
                                                case = case.group(0)
                                            else:
                                                case = self.case[pr]
                                            self.lines[i+2] = self.lines[i+2].replace(temp.group(0), case)
                        
    def save(self, output):
        out = open(output, 'w', encoding = 'utf-8')
        out.write(''.join(self.lines))
        out.close()

if __name__=='__main__':
    D = Disamb(path)
    D.parse()
    D.disamb()
    D.save(output)