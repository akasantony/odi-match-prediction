import pymysql
from core.classifier.player_Dict import player_dict


__authors__ = "Gududuru Abhilasha"
__email__ = "abhilashagududuru@gmail.com"
__date__ = "1st, April 2016"

conn = pymysql.connect("localhost","root","root","cricketcommentaryanalysis")

cursor = conn.cursor()

query = """select bowling_style,player_name from player_card"""

player_role_dict={}
playerVec=[]

try:
    cursor.execute(query)
    results = cursor.fetchall()
    #print(results)
    for row in results:
       #print(row)
       flag=0
       vec=[]
       vec.append(row[-1])
       if row[0]:
           if 'orthodox' in row[0] or 'offbreak' in row[0] or 'Legbreak' in row[0]:
               vec.append('spin')
           if 'fast' in row[0]:
               vec.append('fast')
               flag=1
           if 'medium' in row[0] and flag==0:
               vec.append('medium')
           if 'slow' in row[0]:
               vec.append('slow')
       else:
           vec.append(' ')
           
       playerVec.append(vec)

except:
    print("Error: Unable to Fetch Data")

player_role_dict=dict(playerVec)


for key in player_dict:
    if key in player_role_dict:
        player_role_dict[player_dict[key]] = player_role_dict.pop(key)
