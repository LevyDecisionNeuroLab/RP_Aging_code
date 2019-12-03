# Image picking function for Reward and Punishment
# Adapted from Zhang&Fanning's

import csv,os
from shutil import copyfile
import pandas as pd

def sortRankPic(subjectID):
    currentDirectory=os.path.dirname(os.path.realpath(__file__))
    fileName = currentDirectory + '/data/ETRP_PicRating_' + str(subjectID) +'/ETRP_PicRef_' + str(subjectID)
    if not os.path.isdir('data/ETRP_PicRating_' + str(subjectID)):
        os.makedirs('data/ETRP_PicRating_'+ str(subjectID))
    dataFile = open(fileName+'.csv', 'w')
    dataFile.write('Type, Level,PicLabel\n')
    src = "C:\\Users\\levylab\Documents\\Reward_and_Punishment\\RewardandPunishment-pic\\"
    dst = "C:\\Users\\levylab\Documents\\Reward_and_Punishment\\data\\ETRP_PicRating_"+str(subjectID)
    # generate an external level list that goes from level 4 to 1, as how pictures are arranged in the dataframe
    lvlList = list(range(4,0,-1))
    
    RankList = pd.read_csv(os.path.abspath(os.path.join('data/ETRP_PicRating_'+str(subjectID) +'/ETRP_PicRanking_'+str(subjectID)+'.csv')), delimiter = ',')
    
    PicList = RankList[RankList["RatingNum"] > 5 ]
    rankLen = len(PicList["PicLabel"])
    if rankLen< 4:
        print('Error: Not enough pictures for task')
    elif 3<rankLen<7:
        PicLabel = [PicList["PicLabel"][0],PicList["PicLabel"][1],PicList["PicLabel"][2],PicList["PicLabel"][3]]
    elif 6<rankLen<10:
        PicLabel = [PicList["PicLabel"][0],PicList["PicLabel"][2],PicList["PicLabel"][4],PicList["PicLabel"][6]]
    elif 9<rankLen<13:
        PicLabel = [PicList["PicLabel"][0],PicList["PicLabel"][3],PicList["PicLabel"][6],PicList["PicLabel"][9]]
    elif 12<rankLen<16:
        PicLabel = [PicList["PicLabel"][0],PicList["PicLabel"][4],PicList["PicLabel"][8],PicList["PicLabel"][12]]
    elif 15<rankLen<19:
        PicLabel = [PicList["PicLabel"][0],PicList["PicLabel"][5],PicList["PicLabel"][10],PicList["PicLabel"][15]]
    elif 18<rankLen<21:
        PicLabel = [PicList["PicLabel"][0],PicList["PicLabel"][6],PicList["PicLabel"][12],PicList["PicLabel"][18]]
    else:
        print('There was an error selecting the pictures from the rank list.')
    
    # locate the picture file and copy to subject's folder
    for p in PicLabel:
        dataFile.write('%i,%i,%i\n' %(1, lvlList[PicLabel.index(p)], p))
        copyfile(os.path.join(src+str(p)+'.jpg'),os.path.join(dst+"\\typ1lv"+str(lvlList[PicLabel.index(p)])+"o.jpg"))
    
    PicList = []
    PicList = RankList[RankList["RatingNum"] < 5].reset_index(drop=True)
    rankLen = len(PicList["PicLabel"])
    
    if rankLen< 4:
        print('Error: Not enough pictures for task')
    elif 3<rankLen<7:
        PicLabel = [PicList["PicLabel"][0],PicList["PicLabel"][1],PicList["PicLabel"][2],PicList["PicLabel"][3]]
    elif 6<rankLen<10:
        PicLabel = [PicList["PicLabel"][0],PicList["PicLabel"][2],PicList["PicLabel"][4],PicList["PicLabel"][6]]
    elif 9<rankLen<13:
        PicLabel = [PicList["PicLabel"][0],PicList["PicLabel"][3],PicList["PicLabel"][6],PicList["PicLabel"][9]]
    elif 12<rankLen<16:
        PicLabel = [PicList["PicLabel"][0],PicList["PicLabel"][4],PicList["PicLabel"][8],PicList["PicLabel"][12]]
    elif 15<rankLen<19:
        PicLabel = [PicList["PicLabel"][0],PicList["PicLabel"][5],PicList["PicLabel"][10],PicList["PicLabel"][15]]
    elif 18<rankLen<21:
        PicLabel = [PicList["PicLabel"][0],PicList["PicLabel"][6],PicList["PicLabel"][12],PicList["PicLabel"][18]]
    else:
        print('There was an error selecting the pictures from the rank list.')
    
    for q in PicLabel:
        dataFile.write('%i,%i,%i\n' %(2, lvlList[PicLabel.index(q)], q))
        copyfile(os.path.join(src+str(q)+'.jpg'),os.path.join(dst+"\\typ2lv"+str(lvlList[PicLabel.index(q)])+"o.jpg"))
    