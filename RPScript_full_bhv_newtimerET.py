# Reward and Punishment Psychopy version
# adapted from Zhihao & Jennifer's e-prime script
from psychopy import visual, core, event, data, monitors, tools
from randomizer import randomizeOrder
import random, datetime, time,itertools,math
from copy import deepcopy
import sys, datetime
import os
import numpy as np
from psychopy.iohub import launchHubServer
import scipy.io as sio
from pylink import *

def RPET(subjectID):
    currentTime=str('%.0f' % time.time())
    currentDirectory=os.path.dirname(os.path.realpath(__file__))
    fileName = currentDirectory + '/data/ETRP_' + str(subjectID) +'/ETRP_' + currentTime + '_' + str(subjectID)
    if not os.path.isdir('data/ETRP_' + str(subjectID)):
        os.makedirs('data/ETRP_'+ str(subjectID))
    dataFile = open(fileName+'.csv', 'w')
    dataFile.write('subjID,Block,TrialNum,StimuliRefNum,Type,Level,Actualization,CueRating,OutcomeRating,CueMarkerStartPos,OutcomeMarkerStartPos,CueRT,RewardRT,TrialDur,Delay,ITIjitter\n')
    
    win = visual.Window(color=[0,0,0], screen = 1, fullscr=True, mouseVisible = False)
    mon = monitors.Monitor('testMonitor')
    winSize = mon.getSizePix()
    startKey = '5'
    
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    #Set up eyelinktracker
    eyelinktracker = EyeLink()
    RIGHT_EYE = 1
    LEFT_EYE = 0
    BINOCULAR = 2
    
    # need to change background color here:
    foreground = (250,250,250) #???
    background = (int(254/2),int(254/2),int(254/2))# check background color on testing date, change if color doesn't match
    screenColor = (192,192,192) #???
    
    
    edfFileName = "ETRP" + str(subjectID)
    if len(edfFileName) > 8:
        edfFileName = edfFileName[0:8]
    getEYELINK().openDataFile(edfFileName)
    
    #Eyelink - set idle mode
    getEYELINK().setOfflineMode();
    
    #Eyelink - Gets the display surface and sends a mesage to EDF file;
    getEYELINK().sendCommand("screen_pixel_coords =  0 0 %d %d"%(winSize[0]-1, winSize[1]-1))
    getEYELINK().sendMessage("Resolution %d %d" %((winSize[0]-1, winSize[1]-1)))
    getEYELINK().sendMessage("EyeToScreen %d" %(mon.getDistance()))
    getEYELINK().sendMessage("MonitorWidth %d" %(mon.getWidth()))
    
    #EyeLink - Set data file contents
    getEYELINK().sendCommand("file_sample_data  = LEFT,RIGHT,GAZE,AREA,GAZERES,STATUS,HTARGET,INPUT")
    getEYELINK().sendCommand("link_sample_data  = LEFT,RIGHT,GAZE,GAZERES,AREA,STATUS,HTARGET,INPUT")
    
    #EyeLink - Set Filter contents
    getEYELINK().sendCommand("file_event_filter = LEFT,RIGHT,FIXATION,SACCADE,BLINK,MESSAGE,BUTTON,INPUT")
    getEYELINK().sendCommand("link_event_filter = LEFT,RIGHT,FIXATION,SACCADE,BLINK,BUTTON,INPUT")
    
    #EyeLink - Set Calibration Environment
    #getEYELINK().sendCommand("button_function 5 'accept_target_fixation'");
    setCalibrationColors(foreground, background);  	#Sets the calibration target and background color  - background color should match testing background
    #setTargetSize(int(win.size[0]/20), int(win.size[0]/100));	#select best size for calibration target
    
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    
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
    rect = visual.Rect(
        win=win,units="norm",width=0.2,height=0.15,lineWidth = 4,fillColor=None,lineColor='Grey',pos=(xpos,-0.7))
    
    # Text stimuli setup, default as a + mark
    Text = visual.TextStim(win,text=u"+", height = 0.08, wrapWidth = 1,font='Courier New',
            alignHoriz = 'center', alignVert = 'center', color = 'white',units = 'norm')
            
    # Fixation dot
    fixationCircle=visual.Circle(win, radius=10, fillColor='black',lineColor='black',units = 'pix')
    
    # Ready screen
    Ready = visual.ImageStim(win,image = "images/Ready.png",size = (1.25,1), units = 'norm')
    
    # Trial randomizer for the whole 96 trials; trials will be further randomized to follow designated rules in each block
    trialList = list(range(1,97))
    oList1 = list(range(1,len(trialList)-4,6))
    oList2 = list(range(2,len(trialList)-3,6))
    outcomeList = oList1+oList2
    outcomeList.sort()
    NonOutcome = list(set(outcomeList) ^ set(trialList))
    
    
    x = 0
    NOList = []
    OList = []
    while x < 1:
        NOList.append(sorted(set(NonOutcome[int(x*len(NonOutcome)):int((x+0.25)*len(NonOutcome))])))
        OList.append(sorted(set(outcomeList[int(x*len(outcomeList)):int((x+0.25)*len(outcomeList))])))
        x += 0.25
    refNOList = deepcopy(NOList)
    refOList = deepcopy(OList)
    
    #shuffle within each type
    for s in range(len(NOList)):
        random.shuffle(NOList[s])
        random.shuffle(OList[s])
        
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    # eyetracker setup
    flushGetkeyQueue()
    getEYELINK().setOfflineMode()
    winX = int(winSize[0])
    winY = int(winSize[1])
    openGraphics((winX,winY),32)
    #openGraphicsEx(genv)
    getEYELINK().doTrackerSetup()
    closeGraphics()
    setCalibrationSounds("", "", "");
    setDriftCorrectSounds("", "off", "off");
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    
    # Block counter:
    for block in range(1,5):
        # Order randomization using "randomizeOrder" function:
        Index = randomizeOrder(24)
        # a list of index number (1-24), shuffled so that there is no more than two trials from the same category
        idxList = Index['typeA']+Index['typeB']+Index['typeC']+Index['typeD']
        # a list of index number [1,2,7,8,13,14,19,20] for outcome trials, shuffled; 
        idxListO = Index['outcomeA']+Index['outcomeB']+Index['outcomeC']+Index['outcomeD']
        # create a trial list of randomized reference number (24 out of 1~96) based on randomization 
        trialList = []
        for t in range(4):
            olist=[]
            tlist=[]
            olist= OList[t][0:2]
            for p in range(2):
                OList[t].pop(0)
            tlist=NOList[t][0:4]
            for q in range(4):
                NOList[t].pop(0)
            trialList += olist+tlist
    
        orderList = []
        for i in idxList:
            orderList.append(trialList[i-1])
    
        # Set up time components, shuffle delay and ITI jitter within block
        Delay = list(itertools.repeat(1,8))+list(itertools.repeat(2,8))+list(itertools.repeat(3,8)) # 1,2,3
        random.shuffle(Delay)
        ITI = list(itertools.repeat(4,8))+list(itertools.repeat(6,8))+list(itertools.repeat(8,8)) # change back to int if getting rid of 100 wait at the end of each trial; 4,6,8
        random.shuffle(ITI)
        CueDur = 6 # for the task, 6
        OutcomeDur = 4 # for the task, 4
        
        if block is 4:
            MonetaryOutcome = refOList[2]+refOList[3]
            random.shuffle(MonetaryOutcome)
            orderList.append(MonetaryOutcome[0])
            MonOutcomeTime = [2,6]
            Delay.append(MonOutcomeTime[0])
            ITI.append(MonOutcomeTime[1])
            
        # Block start
        event.clearEvents()
        Rsp = False
        while Rsp == False:
            Text.height= 0.08
            Text.text = 'Start of block.'
            Text.draw()
            # # # # # # # # # # # # # # # # # # 
            getEYELINK().sendMessage('WaitForExptrStart')
            # # # # # # # # # # # # # # # # # # 
            win.flip()
            buttonPress=event.getKeys(keyList = ['7'])
            if len(buttonPress)>0:
                Rsp = True
        
        event.clearEvents()
        Rsp = False
        while Rsp == False:
            Text.height= 0.08
            Text.text = 'Waiting for the scanner to start...'
            Text.draw()
            # # # # # # # # # # # # # # # # # # 
            getEYELINK().sendMessage('WaitForScanner')
            # # # # # # # # # # # # # # # # # # 
            win.flip()
            buttonPress=event.getKeys(keyList = ['5'])
            if len(buttonPress)>0:
                Rsp = True
                
        # Ready screen
        Clock = core.Clock()
        Clock.add(5)
        while Clock.getTime()<0:
            Ready.draw()
            # # # # # # # # # # # # # # # # # # 
            getEYELINK().sendMessage('ReadyScreen')
            # # # # # # # # # # # # # # # # # # 
            win.flip()
        
        # ITI
        #Clock.reset()
        Clock.add(2)
        while Clock.getTime() < 0:
            fixationCircle.draw()
            # # # # # # # # # # # # # # # # # # 
            getEYELINK().sendMessage('ReadyITI')
            # # # # # # # # # # # # # # # # # # 
            win.flip()
        
        n = 0 # n = 0 for indexing purposes
        while n < len(orderList): #len(orderList)
            trialClock = core.MonotonicClock()
            # eyetracker
            error = getEYELINK().startRecording(1,1,1,1) # flags = (samples in edf, events in edf, samples over link, events over link)
            getEYELINK().sendMessage('TRIALID %d'%(n))
            
            #Clock.reset()
            trialNum = n+1 # for the purpose of indcating the correct trial
            # the Grey box will start at a random number for each trial
            markStart = random.choice(xposList)
            rect.lineColor = 'White'
            xpos = markStart
            rect.pos=(xpos,-0.7)
            typ=[]
            lvl=[]
            #print('trial',n,'orderList[n]',orderList[n])
            if orderList[n] not in outcomeList:
                Act = 0
            # Determine type and level
                for c in refNOList:
                    if orderList[n] in c:
                        typ = refNOList.index(c)+1
                        # from a list of 16 numbers, divided by 4 and ceil, to find level
                        lvl = math.ceil((c.index(orderList[n])+1)/4)
                        # Cue setup
                        Cue = visual.ImageStim(win,image='images/typ'+str(typ)+'lv'+str(lvl)+'.png', size = (1.25,1), units = 'norm')
                        OutcomeStim = visual.TextStim(win,text=u"No Outcome", height = 0.1, wrapWidth = 1,font='Courier New', alignHoriz = 'center', 
                            alignVert = 'center', color = 'yellow',units = 'norm',pos=(0,-0.6))
            else:
                Act = 1
                for c in refOList:
                    if orderList[n] in c:
                        typ = refOList.index(c)+1
                        # from a list of 8 numbers, divided by 2 and ceil, to find level
                        lvl = math.ceil((c.index(orderList[n])+1)/2)
                        Cue = visual.ImageStim(win,image='images/typ'+str(typ)+'lv'+str(lvl)+'.png', size = (1.3,1), units = 'norm')
                        if typ < 3:
                            OutcomeStim = visual.ImageStim(win,image = os.path.join('data//ETRP_PicRating_'+str(subjectID)+'//typ'+str(typ)+'lv'+str(lvl)+'o.jpg'),size = (1,0.85),units = 'norm') # size = (0.4,0.5)
                        else:
                            OutcomeStim = visual.ImageStim(win,image = 'images/typ'+str(typ)+'lv'+str(lvl)+'o.png',size = (0.65,0.78), units = 'norm')
    
            Delayjit = Delay[n]
            ITIjit = ITI[n]
            # set stimuli autoDraw to True so they would show up on every frame, avoid screen display twinkle:
            for b in buttons:
                b.autoDraw = True
            for l in labels:
                l.autoDraw = True
            Cue.autoDraw = True
            rect.autoDraw = True
            # Cue rating
            event.clearEvents()
            Clock.add(CueDur)
            # indicator for eyetracking data
            startedPressing=False
            gotFinalPress=False
            Rsp = False
            while Rsp is False:
                # # # # # # # # # # # # # # # # # # # # # 
                # eyetracking labels
                if startedPressing == False:
                    getEYELINK().sendMessage('cueRating1')
                elif startedPressing==True and gotFinalPress==False:
                    getEYELINK().sendMessage('cueRating2')
                elif gotFinalPress==True:
                    getEYELINK().sendMessage('cueRating3')
                # # # # # # # # # # # # # # # # # # # # # 
                win.flip()
                buttonPress=event.getKeys(keyList = ['1','2','3'])
                if len(buttonPress) > 0 and Clock.getTime() < 0:
                    startedPressing = True
                    # Moving the marker to the left with key 1
                    if buttonPress == ['1']:
                        #startedPressing = True
                        xpos-=0.2
                        if xpos < -0.8:
                            xpos = -0.8
                        rect.pos=(xpos,-0.7)
                        rect.lineColor = 'Yellow'
                        win.flip()
                    # Moving the marker to the right with key 3
                    if buttonPress == ['3']:
                        #startedPressing = True
                        xpos+=0.2
                        if xpos > 0.8:
                            xpos = 0.8
                        rect.pos=(xpos,-0.7)
                        rect.lineColor = 'Yellow'
                        win.flip()
                    # Confirmation key = 2
                    if buttonPress == ['2']:
                        gotFinalPress= True
                        Rating = xposList.index(round(xpos,2))+1
                        RT= CueDur + Clock.getTime() #Clock.getTime()
                        rect.lineColor = 'Red'
                        CueRemainDur = CueDur - RT # 0 - RT
                        win.flip()
                        core.wait(CueRemainDur)
                        Rsp = True
                elif buttonPress != ['2'] and Clock.getTime() > 0: 
                    #buttonPress != ['2'] and Clock.getTime() > 0:
                    Rating = 0
                    RT = Clock.getTime() #-1
                    Rsp = True
                    
            # Set all autoDraw back to False, so that you can present new stimuli on the screen
            for b in buttons:
                b.autoDraw = False
            for l in labels:
                l.autoDraw = False
            Cue.autoDraw = False
            rect.autoDraw = False
            
            # Delay period - fixation point
            #Clock.reset()
            Clock.add(Delayjit)
            while Clock.getTime() < 0:
                fixationCircle.draw()
                win.flip()
                # # # # # # # # # # # # # # # # # # 
                getEYELINK().sendMessage('delay')
                # # # # # # # # # # # # # # # # # # 
            
            # Outcome display - camera image and outcome image
            #Clock.reset()
            Clock.add(2)
            while Clock.getTime() < 0:
                Cue.draw()
                OutcomeStim.draw()
                win.flip()
                # # # # # # # # # # # # # # # # # # 
                getEYELINK().sendMessage('outcome')
                # # # # # # # # # # # # # # # # # # 
            
            # Reward rating
            for b in buttons:
                b.autoDraw = True
            for l in labels:
                l.autoDraw = True
            rect.autoDraw = True
            
            
            RewardMarkStart = random.choice(xposList)
            rect.lineColor = 'White'
            xpos = RewardMarkStart
            rect.pos=(xpos,-0.7)
            event.clearEvents()
            Rsp = False
            Clock.add(OutcomeDur)
            #tracker indicator
            startedPressing=False
            gotFinalPress=False
            while Rsp is False:
                # # # # # # # # # # # # # # # # # # # # # # # # 
                if startedPressing == False:
                    getEYELINK().sendMessage('rewardRating1')
                elif startedPressing==True and gotFinalPress==False:
                    getEYELINK().sendMessage('rewardRating2')
                elif gotFinalPress==True:
                    getEYELINK().sendMessage('rewardRating3')
                # # # # # # # # # # # # # # # # # # # # # # # # 
                win.flip()
                buttonPress=event.getKeys(keyList = ['1','2','3'])
                if len(buttonPress) > 0 and Clock.getTime() < 0:
                    startedPressing = True
                    # Moving the marker to the left with key 1
                    if buttonPress == ['1']:
                        
                        xpos-=0.2
                        if xpos < -0.8:
                            xpos = -0.8
                        rect.pos=(xpos,-0.7)
                        rect.lineColor = 'Yellow'
                        rect.autoDraw = True
                        win.flip()
                    # Moving the marker to the right with key 3
                    if buttonPress == ['3']:
                        
                        xpos+=0.2
                        if xpos > 0.8:
                            xpos = 0.8
                        rect.pos=(xpos,-0.7)
                        rect.lineColor = 'Yellow'
                        rect.autoDraw=True
                        win.flip()
                    # Confirmation key = 2, the subject has to move the marker in order to confirm
                    # (in other words, the marker does not have to be Yellow in order to accept the choice)
                    if buttonPress == ['2'] and Clock.getTime() < 0: #rect.lineColor is 'Yellow' and 
                        gotFinalPress=True
                        RewardRating = xposList.index(round(xpos,2))+1
                        RewardRT= OutcomeDur + Clock.getTime() # Clock.getTime()
                        rect.lineColor = 'Red'
                        CueRemainDur = OutcomeDur - RewardRT # 0 - RewardRT
                        win.flip()
                        core.wait(CueRemainDur)
                        Rsp=True
                        
                elif buttonPress != ['2'] and Clock.getTime() > 0: # (rect.lineColor is 'Grey' and Clock.getTime() > OutcomeDur) or ()
                    RewardRating = 0
                    RewardRT = Clock.getTime()#-1
                    Rsp = True
                    
            for b in buttons:
                b.autoDraw = False
            for l in labels:
                l.autoDraw = False
            rect.autoDraw = False
        
            # ITI - fixation point
            Clock.add(ITIjit)
            while Clock.getTime() < 0:
                fixationCircle.draw()
                # # # # # # # # # # # # # # # # # # 
                getEYELINK().sendMessage('ITI')
                # # # # # # # # # # # # # # # # # # 
                win.flip()
            TrialDur = trialClock.getTime()
            dataFile.write('%i,%i,%i,%i,%i,%i,%i,%i,%i,%i,%i,%f,%f,%f,%f,%f\n' %(subjectID,block,trialNum,orderList[n],typ,lvl,Act,Rating,RewardRating,xposList.index(markStart)+1,xposList.index(RewardMarkStart)+1,RT,RewardRT,TrialDur,Delayjit,ITIjit))
            
            n+=1
            # Log data
            
        block += 1
        
        event.clearEvents()
        Rsp = False
        while Rsp == False:
            Text.height= 0.08
            Text.text = 'End of block.'
            Text.draw()
            # # # # # # # # # # # # # # # # # # 
            getEYELINK().sendMessage('WaitForExptrEnd')
            # # # # # # # # # # # # # # # # # # 
            win.flip()
            buttonPress=event.getKeys(keyList = ['9'])
            if len(buttonPress)>0:
                Rsp = True

    dataFile.close()
    
    Text.text='Thank you for participating!'
    for frame in range(60):
        Text.draw()
        win.flip()
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    if getEYELINK() != None:
    # File transfer and cleanup!
        getEYELINK().setOfflineMode()
        pumpDelay(500)
    
    #Close the file and transfer it to Display PC
        getEYELINK().closeDataFile()
        transferFileName = fileName + '.edf' # fileName
        getEYELINK().receiveDataFile(edfFileName, transferFileName)
        getEYELINK().close()
        #matFileName = fileName + '.mat'
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        #check matlab on the experiment computer
        #os.system('DYLD_LIBRARY_PATH=C:/Users/levylab/Documents/Reward and Punishment/edfmat_mac64 %s %s'%(transferFileName,matFileName))
    win.close()
    core.quit()
    