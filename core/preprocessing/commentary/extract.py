import os
import io
import nltk

__author__ = 'Akas Antony'
__email__ = 'antony.akas@gmail.com'
__date__ = '28th January, 2016'


class Extract(object):

    def __init__(self):
        self.ball_no = 0
        self.bowler_name = ''
        self.batsman_name = ''
        self.prev_val = ''
        self.ball_details = {}
        self.no_run = ["no run"]
        self.one_run = ["1 run", " wide called"]
        self.two_run = ["2 run"]
        self.three_run = ["3 run"]
        self.four_run = ["four"]
        self.six_run = ["six"]
        self.out = ["OUT"]
        self.match_types = ["super eights", "semi final", "group", "final"]
        self.runs = 0
        self.match_details = {}
        self.metadat = []

    def parse(self, file):
        text = ""
        with io.open(file, 'r', encoding='iso-8859-15') as file_handle:
            for line in file_handle:
                if line == '\n':
                    continue
                else:
                    text += line
        text = text.split('\n')
        return text

    def extract_runs(self, data):
        run = 0
        if any(ext in data for ext in self.no_run):
            run = 0
        elif any(ext in data for ext in self.one_run):
            run = 1
        elif any(ext in data for ext in self.two_run):
            run = 2
        elif any(ext in data for ext in self.four_run):
            run = 4
        elif any(ext in data for ext in self.six_run):
            run = 6
        elif any(ext in data for ext in self.out):
            run = "OUT"
        return run

    def extract_ballno(self, data):
        if data[0][1] == 'CD':
            try:
                float(data[0][0])
                return data[0][0]
            except ValueError:
                return 0

    def extract_bowler_batsman(self, data):
        i = 0
        self.bowler_name = ''
        self.batsman_name = ''
        for word in data:
            if word[1] == 'NNP' or word[1] == 'NNS' or word[1] == 'NN' and ('TO' in data):
                self.bowler_name += ' '+word[0]
            if word[1] == 'TO':
                ind = data[1].index('TO')
                # print(data[ind+1][0])
                while 1:
                    if data[ind+1][1] == 'NNP' or data[ind+1][1] == 'NNS' or word[1] == 'NN':
                        self.batsman_name += ' '+data[ind+1][0]
                        ind += 1
                    else:
                        break
                break
        return self.batsman_name.strip(), self.bowler_name.strip()
        # print(self.ball_details)

    def process(self, data):
        match_details = {}
        ball_details = []
        f = open('out.txt', 'a')
        for index, line in enumerate(data):
            if data:
                flag = 1
                tokenized_text = nltk.word_tokenize(line)
                pos_tagged = nltk.pos_tag(tokenized_text)
                if index == 0:
                    if any(types in line.lower() for self.ind, types in enumerate(self.match_types)):
                        self.match_type = self.match_types[self.ind]
                        match_details['category'] = self.match_type
                if index == 5:
                    self.year = line.split()[2]
                    match_details['year'] = self.year
                if index == 1:
                    self.countries = line.split('v')
                    self.countries = [i.strip() for i in self.countries]
                if index == 6:
                    self.first_innings = line.split('Innings:')[0].strip()
                    self.second_innings = self.countries[0] if self.countries[1] == self.first_innings else self.countries[1]
                    match_details['first_innings'] = self.first_innings
                    match_details['second_innings'] = self.second_innings
                if index > 6:
                    if(pos_tagged):
                        if self.extract_ballno(pos_tagged):
                            self.ball_no = self.extract_ballno(pos_tagged)
                            self.ball_no = self.ball_no.replace('.', '/')
                            flag = 0
                            prev_ball = True
                    if flag and prev_ball:
                        # print(pos_tagged)
                        self.batsman_name, self.bowler_name = self.extract_bowler_batsman(pos_tagged)
                        self.runs = self.extract_runs(line.lower())
                        lis = [self.year, self.match_type, self.first_innings, self.second_innings, self.ball_no, self.
                            batsman_name, self.bowler_name, self.runs]
                        ball_details.append([self.ball_no, self.batsman_name, self.bowler_name, self.runs])
                        prev_ball = False
                        if index == 9:
                            break
        # match_details['ball_details'] = ball_details
        # print(match_details)
        # return match_details

        return ball_details
