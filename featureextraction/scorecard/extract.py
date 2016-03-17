from config import paths

__author__ = 'Akas Antony'
__email__ = 'antony.akas@gmail.com'
__date__ = '04th February, 2016'


class Extract(object):

    def parse(self, file):
        text = ""
        file_handle = open(file, 'r')
        for line in file_handle:
            line.replace('\t', '\n')
            if line == '\n' or line == '':
                continue
            else:
                text += line
        return text.split('\n')

    def batting_card(self, data):
        index = 8
        x = []
        y = []
        for pos, i in enumerate(range(index, index+11)):
            k = []
            lis = data[i].split('\t')
            k.append(lis[0])
            if 'lbw b ' in lis[1]:
                k.append(lis[1].split('lbw b ')[1])
            if 'st ' in lis[1]:
                k.append(lis[1].split(' b ')[-1])
            if lis[1] == ' ':
                break
            if lis[1].split(' ')[0] == 'b':
                k.append(lis[1][2:])
            if lis[1].split(' ')[0] == 'c':
                k.append(lis[1].split(' b ')[1])
            if not lis[2] == ' ':
                k.append(lis[2])
                k.append(lis[3])
                k.append(lis[4])
                k.append(lis[5])
            if 'not out' in data[i]:
                k.insert(1, 'N/O')
            if 'run out' in data[i]:
                k.insert(1, 'R/0')
            k.append(1)
            k.append(pos+1)
            x.append(k)
        for i in range(index+10, len(data)):
            if '(target ' in data[i]:
                for pos, a in enumerate(range(i, i+11)):
                    k = []
                    lis = data[a+1].split('\t')
                    k.append(lis[0])
                    if 'lbw b ' in lis[1]:
                        k.append(lis[1].split('lbw b ')[1])
                    if 'st ' in lis[1]:
                        k.append(lis[1].split(' b ')[-1])
                    if lis[1].split(' ')[0] == 'b':
                        k.append(lis[1][2:])
                    if lis[1].split(' ')[0] == 'c':
                        k.append(lis[1].split(' b ')[1])
                    if not lis[2] == ' ':
                        k.append(lis[2])
                        k.append(lis[3])
                        k.append(lis[4])
                        k.append(lis[5])
                    if 'not out' in data[a+1]:
                        k.insert(1, 'N/O')
                    if 'run out' in data[a+1]:
                        k.insert(1, 'R/0')
                    if lis[2] == ' ':
                        break
                    k.append(2)
                    k.append(pos+1)
                    y.append(k)
        return x, y

    def bowling_card(self, data):
        x = []
        y = []
        flag = True
        for index, i in enumerate(data):
            if 'Bowling' in i:
                ind = index
                while 1:
                    if flag:
                        ind += 1
                        if not data[ind] == ' ':
                            x.append(data[ind].split('\t'))
                        if data[ind] == ' ':
                            flag = False
                            break
                    if not flag:
                        ind += 1
                        if not data[ind] == ' ':
                            y.append(data[ind].split('\t'))
                        if data[ind] == ' ':
                            flag = False
                            break
        for i in x:
            for ind, j in enumerate(i):
                if j == ' ':
                    i[ind] = 0
                if not i[2] == ' ':
                    i[1] = float(int(i[1]) + float(i[2]))
            i[1] = int(str(i[1]).split('.')[0])*6 + int(str(i[1]).split('.')[1])
            del i[2]
            del i[-1]
            del i[-1]
            i.append(1)
        for i in y:
            for ind, j in enumerate(i):
                if j == ' ':
                    i[ind] = 0
                if not i[2] == ' ':
                    i[1] = float(int(i[1]) + float(i[2]))
            i[1] = int(str(i[1]).split('.')[0])*6 + int(str(i[1]).split('.')[1])
            del i[2]
            del i[-1]
            del i[-1]
            i.append(2)
        return x, y

    def country_extract(self, data):
        countries = data[0].split('-')[-1].strip().split(' v ')
        first_inng = data[7].split('\t')[0]
        second_inng = countries[0] if first_inng == countries[1] else countries[1]
        return first_inng, second_inng

if __name__ == '__main__':
    batting_file = open(paths.__SCORECARD__+'batting_card.txt', 'w')
    bowling_file = open(paths.__SCORECARD__+'bowling_card.txt', 'w')
    ex = Extract()
    for m in range(1, 50):
        batting_vec = []
        bowling_vec = []
        parsed_text = ex.parse(paths.__SCORECARD__+str(m))
        bowling_card = ex.bowling_card(parsed_text)
        batting_card = ex.batting_card(parsed_text)
        first_inng, second_inng = ex.country_extract(parsed_text)
        for j in batting_card[0]:
            batting_vec = batting_vec + [[m] + [first_inng] + j]
            bowl_cnt_first = second_inng
        for j in batting_card[1]:
            batting_vec.append([m] + [second_inng] + j)
            bowl_cnt_second = first_inng
        for i in batting_vec:
            for j in i:
                batting_file.write(str(j)+'\t')
            batting_file.write('\n')
        for j in bowling_card[0]:
            bowling_vec = bowling_vec + [[m] + [bowl_cnt_first] +j]
        for j in bowling_card[1]:
            bowling_vec.append([m] + [bowl_cnt_second] + j)
        for i in bowling_vec:
            for j in i:
                bowling_file.write(str(j)+'\t')
            bowling_file.write('\n')

