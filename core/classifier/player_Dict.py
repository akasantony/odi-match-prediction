import pymysql


__authors__ = "Gududuru Abhilasha"
__email__ = "abhilashagududuru@gmail.com"
__date__ = "28th, February 2016"

conn = pymysql.connect("localhost","root","root","cricketcommentaryanalysis")

cursor = conn.cursor()

query = """select player_id,player_name from player_card"""

player_dict={}
playerVec=[]
try:
    cursor.execute(query)
    results = cursor.fetchall()
    for row in results:
       vec=[]
       vec.append(row[-1])
       vec.append(row[0])
       playerVec.append(vec)

except:
    print("Error: Unable to Fetch Data")
print(playerVec[21])
player_dict=dict(playerVec)
