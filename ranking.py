# Picture ranking for Reward and Punishment

from psychopy import visual, core, event, data, monitors, tools
import random, datetime, time,os,csv, itertools
import pandas as pd

# event.globalKeys.add(key='q',modifiers = ['ctrl'], func = core.quit)

def PicRanking(subjectID):
    win = visual.Window(color=[0,0,0], screen = 0, fullscr=True, mouseVisible = False)
    
    currentTime=str('%.0f' % time.time())
    currentDirectory=os.path.dirname(os.path.realpath(__file__))
    fileName = currentDirectory + '/data/ETRP_PicRating_' + str(subjectID) +'/ETRP_PicRanking_' + str(subjectID)
    if not os.path.isdir('data/ETRP_PicRating_' + str(subjectID)):
        os.makedirs('data/ETRP_PicRating_'+ str(subjectID))
    dataFile = open(fileName+'.csv', 'w')
    dataFile.write('RatingNum,PicLabel,Rank,RT\n')
    
    # import result from pic rating
    PicRefList = pd.read_csv(os.path.abspath(os.path.join('data/ETRP_PicRating_'+str(subjectID) +'/ETRP_PicRating_'+str(subjectID)+'.csv')), delimiter = ',')
    
    # sorting with respect to Rating column
    PicRefList.sort_values("Rating",inplace = True, ascending = False)
    # find the maximum rating
    maxRating = PicRefList['Rating'].max()
    # find the minimum rating
    minRating = PicRefList['Rating'].min()
    # rank present in order of rating 9->6, 1->4:
    rankOrder = list(range(maxRating,5,-1))+list(range(minRating,5,1))
    #print(rankOrder)
    
    Text = visual.TextStim(win,text=u"+", height = 0.08, wrapWidth = 1,font='Courier New',
            alignHoriz = 'center', alignVert = 'center', color = 'white',units = 'norm')
    
    for s in rankOrder:
        print(s)
        Segment = PicRefList[PicRefList["Rating"] == s]
        
        # from 1(MOST (un)pleasant to the LEAST (un)pleasant):
        if s == minRating:
            Text.text = "Rank from the Most Unpleasant to Little Unpleasant\n[Press 5 to start]"
            Rank = 0
        elif s == maxRating:
            Text.text = "Rank from the Most Pleasant to Little Pleasant\n[Press 5 to start]"
            Rank = 0
        
        event.clearEvents()
        Rsp = False
        while Rsp is False:
            Text.draw()
            win.flip()
            buttonPress=event.getKeys(keyList = ['5'])
            if len(buttonPress)>0:
                Rsp = True
        RefNumList = Segment['StimuliRefNum'].values.tolist()
        # shuffle the list
        random.shuffle(RefNumList)
        
        #Set up rating marker stimuli
        xpos=0
        rect = visual.Rect(
            win=win,units="norm",width=0.4,height=0.55,lineWidth = 5,fillColor=None,lineColor='Grey',pos=(xpos,0.6))
        # if more than 9 pictures, take the first 9 pictures after shuffling the whole list(shuffled in lines above)
        if len(RefNumList) > 9:
            RefNumList = RefNumList[0:8]
        xposList = [-0.65,0,0.65]
        yposList = [0.6,0,-0.6]
        picDim = (0.4,0.55)
        refList = list(itertools.product(xposList,yposList))
        
        trial = 0
        pic=[]
        while trial < len(RefNumList):
            pic.append(visual.ImageStim(win, image = "RewardandPunishment-pic/"+str(RefNumList[trial])+".jpg",pos=refList[trial],size=picDim,units="norm"))
            trial+=1
        
        # sum of picList is 0 when subject has ranked all of the pictures in this rating
        picList = list(itertools.repeat(1,len(RefNumList)))
        
        trial = 0
        while sum(picList) > 0:
            markStartX = random.choice(xposList)
            markStartY = random.choice(yposList)
            rect.lineColor = 'White'
            xpos = markStartX
            ypos = markStartY
            rect.pos=(xpos,ypos)
            for p in pic:
                p.autoDraw=True
            rect.autoDraw=True
            event.clearEvents()
            Rsp = False
            Clock= core.Clock()
            while Rsp is False:
                win.flip()
                buttonPress=event.getKeys(keyList = ['1','2','3'])
                if len(buttonPress) > 0:
                    # Moving the marker to the left with key 1
                    if buttonPress == ['1']:
                        xpos-=xposList[2] # to move horizontally
                        # if mark is on the second or third row, allow to move up
                        if xpos < xposList[0] and (ypos < yposList[0]):
                            xpos = xposList[2] # locate on the right
                            ypos += yposList[0] # move up one row
                        elif xpos < xposList[0] and (ypos == yposList[0]):
                            xpos = xposList[0] # freez at the left
                            ypos = yposList[0] # freez at the top row
                            
                        rect.pos=(xpos,ypos)
                        rect.lineColor = 'Yellow'
                        win.flip()
                    # Moving the marker to the right with key 3
                    if buttonPress == ['3']:
                        xpos+=xposList[2]
                        # if mark is on the first or second row, allow to move down
                        if xpos > xposList[2] and (ypos > yposList[2]):
                            xpos = xposList[0] # locate on the left
                            ypos += yposList[2] # move down one row
                        elif xpos > xposList[2] and (ypos == yposList[2]):
                            xpos = xposList[2] # freez at the right
                            ypox = yposList[2] # freez at the bottom row
                        rect.pos=(xpos,ypos)
                        rect.lineColor = 'Yellow'
                        win.flip()
                    # Confirmation key = 2
                    if buttonPress == ['2']:
                        RankChoice = refList.index((xpos,ypos))
                        #ChoiceHistory = 
    #                    print(RankChoice)
                        RT=Clock.getTime()
                        rect.lineColor = 'Red'
                        #CueRemainDur = CueDur - RT
                        win.flip()
                        core.wait(0.5)
                        Rsp = True 
            for p in pic:
                p.autoDraw=False
            rect.autoDraw=False
            if RankChoice < len(RefNumList) and picList[RankChoice] == 1:
                pic[RankChoice] = visual.ImageStim(win, image = "RewardandPunishment-pic/snip2.png",pos=refList[RankChoice],size=(0.4,0.55),units="norm")
                picList[RankChoice] = 0
                Rank += 1
                dataFile.write('%i,%i,%i,%f\n' %(s,RefNumList[RankChoice],Rank,RT))
                trial += 1