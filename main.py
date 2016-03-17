from featureextraction.commentary.extract import Extract
import os
from config import paths
from pymongo import MongoClient

if __name__ == '__main__':
    # client = MongoClient()
    # client = MongoClient('localhost', 27017)
    # db = client.cricket_data
    # db_data = db.data
    ex = Extract()
    data = {}
    for file in os.listdir(paths.__CW2007__):
        text = ex.parse(paths.__CW2007__+file)
        print(paths.__CW2007__+file)
        ball_details = ex.process(text)
        # year = match_details['year']
        # first_innings = match_details['first_innings']
        # second_innings = match_details['second_innings']
        # category = match_details['category']
        # ball_details = match_details['ball_details']
        # print(match_details)
        print (ball_details)
        break
