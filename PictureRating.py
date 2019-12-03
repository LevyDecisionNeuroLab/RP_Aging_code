# picture rating
# adapted from Zhihao & Fanning's Reward and Punishment Task

from psychopy import visual, core, event, data, monitors, tools
import random, datetime, time,os,csv

#event.globalKeys.add(key='q',modifiers = ['ctrl'], func = core.quit)

def PicRating(subjectID):
    currentTime=str('%.0f' % time.time())
    currentDirectory=os.path.dirname(os.path.realpath(__file__))
    fileName = currentDirectory + '/data/ETRP_PicRating_' + str(subjectID) +'/ETRP_PicRating_' + str(subjectID)
    if not os.path.isdir('data/ETRP_PicRating_' + str(subjectID)):
        os.makedirs('data/ETRP_PicRating_'+ str(subjectID))
    dataFile = open(fileName+'.csv', 'w')
    dataFile.write('TrialNum,StimuliRefNum,Type,Rating,RT\n')
    
    win = visual.Window(color=[0,0,0], screen = 0, fullscr=True, mouseVisible = False)
    
    # Set up rating scale stimuli
    buttons=[]
    x=-0.8
    for b in range(9):
        buttons.append(visual.TextStim(win, alignHoriz='center',units = 'norm',text=str(b+1),pos=(x,-0.7), height=0.1,font='Courier New',color = 'white'))
        x+=0.2
    labels=[]
    labels.append(visual.TextStim(win, alignHoriz='center',text='Unpleasant',units = 'norm',pos=(-0.8,-0.8),font='Courier New', height=0.08,color='white'))
    labels.append(visual.TextStim(win, alignHoriz='center',text='Pleasant',units = 'norm',pos=(0.8,-0.8), font='Courier New', height=0.08,color='white'))
    # Set up rating marker stimuli
    xpos=0
    xposList = [-0.8,-0.6,-0.4,-0.2,0,0.2,0.4,0.6,0.8]
    rect = visual.Rect(win=win,units="norm",width=0.2,height=0.15,lineWidth = 4,fillColor=None,lineColor='Grey',pos=(xpos,-0.7))
    
    # Fixation dot
    fixationCircle=visual.Circle(win, radius=10, fillColor='black',lineColor='black',units = 'pix')
    
    
    # generate a random list of 1-40
    trialList = list(range(1,41))
    random.shuffle(trialList)
    Pic = visual.ImageStim(win,image = "RewardandPunishment-pic/1.jpg",size = (1,1.2),pos=[0,0.25], units = 'norm')
    
    trial = 0
    while trial< 40:
        # ITI
        Clock = core.Clock()
        while Clock.getTime() < 1:
            fixationCircle.draw()
            win.flip()
            
        
        markStart = random.choice(xposList)
        rect.lineColor = 'White'
        xpos = markStart
        rect.pos=(xpos,-0.7)
        Pic.image = "RewardandPunishment-pic/"+str(trialList[trial])+".jpg"
        # set stimuli autoDraw to True so they would show up on every frame, avoid screen display twinkle:
        for b in buttons:
            b.autoDraw = True
        for l in labels:
            l.autoDraw = True
        Pic.autoDraw = True
        rect.autoDraw = True
        
        
        event.clearEvents()
        Rsp = False 
        Clock= core.Clock() # clock for rating scale
        while Rsp is False:
            win.flip()
            buttonPress=event.getKeys(keyList = ['1','2','3'])
            if len(buttonPress) > 0:
                # Moving the marker to the left with key 1
                if buttonPress == ['1']:
                    xpos-=0.2
                    if xpos < -0.8:
                        xpos = -0.8
                    rect.pos=(xpos,-0.7)
                    rect.lineColor = 'Yellow'
                    win.flip()
                # Moving the marker to the right with key 3
                if buttonPress == ['3']:
                    xpos+=0.2
                    if xpos > 0.8:
                        xpos = 0.8
                    rect.pos=(xpos,-0.7)
                    rect.lineColor = 'Yellow'
                    win.flip()
                # Confirmation key = 2
                if buttonPress == ['2']: 
                    Rating = xposList.index(round(xpos,2))+1
                    RT=Clock.getTime()
                    rect.lineColor = 'Red'
                    win.flip()
                    Rsp=True 
        if Rating > 5:
            Type = 1
        elif Rating < 5:
            Type = 2
        else:
            Type = 0
        # Set all autoDraw back to False, so that you can present new stimuli on the screen
        for b in buttons:
            b.autoDraw = False
        for l in labels:
            l.autoDraw = False
        Pic.autoDraw = False
        rect.autoDraw = False
        
        # write data to save
        dataFile.write('%i,%i,%i,%i,%f\n' %(trial+1,trialList[trial],Type,Rating,RT))
        
        # trial increment
        trial+=1
    