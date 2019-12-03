# practice trials
from psychopy.iohub import *
import gc
from psychopy import visual, core, event, data, monitors, tools
from randomizer import randomizeOrder
import random, datetime, time,itertools,math,sys, os
from copy import deepcopy
import numpy as np
import scipy.io as sio

def pracTrials():
# window setup
    win = visual.Window(color=[0,0,0], screen = 0, fullscr=True, mouseVisible = False)
    mon = monitors.Monitor('testMonitor')
    winSize = mon.getSizePix()
    event.Mouse(visible=False)
    
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
    
    # Trial randomizer for the whole 96 trials; trials will be further randomized to follow designated rules in each block
    trialList = list(range(1,25))
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
    
    
    # shuffle by 
    for s in range(len(NOList)):
        random.shuffle(NOList[s])
        random.shuffle(OList[s])
    
    # Order randomization using "randomizeOrder" function:
    Index = randomizeOrder(24)
    idxList = Index['typeA']+Index['typeB']+Index['typeC']+Index['typeD']
    idxListO = Index['outcomeA']+Index['outcomeB']+Index['outcomeC']+Index['outcomeD']
    #print(idxList)
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
    Delay = list(itertools.repeat(1,8))+list(itertools.repeat(2,8))+list(itertools.repeat(3,8))
    random.shuffle(Delay)
    ITI = list(itertools.repeat(4,8))+list(itertools.repeat(6,8))+list(itertools.repeat(8,8))
    random.shuffle(ITI)
    CueDur = 6 # for the task, 6  # for pupil diameter - min = 4
    OutcomeDur = 4 # for the task, 4
    
        
    n = 0 # n = 0 for indexing purposes
    while n < 5:
        # experiment
        trialNum = n+1 # for the purpose of indcating the correct trial
        # the Grey box will start at a random number for each trial
        markStart = random.choice(xposList)
        rect.lineColor = 'White'
        xpos = markStart
        rect.pos=(xpos,-0.7)
        typ=[]
        lvl=[]
        # if trial number is not in reward list
        if orderList[n] not in outcomeList:
        # Determine type
            for c in refNOList:
                if orderList[n] in c:
                    typ = refNOList.index(c)+1
                    lvl = math.ceil((c.index(orderList[n])+1)/4)
                    # Cue setup
                    Cue = visual.ImageStim(win,image='images/typ'+str(typ)+'lv'+str(lvl)+'.png', size = (0.8,0.9), units = 'norm')
                    OutcomeStim = visual.TextStim(win,text=u"No Outcome", height = 0.1, wrapWidth = 1,font='Courier New', alignHoriz = 'center', 
                        alignVert = 'center', color = 'yellow',units = 'norm',pos=(0,-0.6))
    
        else:
            for c in refOList:
                if orderList[n] in c:
                    typ = refOList.index(c)+1
                    lvl = math.ceil((c.index(orderList[n])+1)/4)
                    Cue = visual.ImageStim(win,image='images/typ'+str(typ)+'lv'+str(lvl)+'.png', size = (0.8,0.9), units = 'norm')
                    OutcomeStim = visual.ImageStim(win,image = 'images/PracticeOutcome.png',size = (0.5,0.6),units = 'norm')
    
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
        Rsp = False
        event.clearEvents()
        Clock= core.Clock() # clock for rating scale
        # indicator for eyetracking data
        startedPressing=False
        gotFinalPress=False
        
        while Rsp is False:
            win.flip()
            buttonPress=event.getKeys(keyList = ['1','2','3'])
            if len(buttonPress) > 0 and Clock.getTime() < CueDur:
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
                # Confirmation key = 2, the subject has to move the marker in order to confirm
                # (in other words, the marker has to be Green in order to accept the choice)
                if buttonPress == ['2'] and Clock.getTime(): # rect.lineColor is 'Yellow' and 
                    Rating = xposList.index(round(xpos,2))+1
                    RT=Clock.getTime()
                    rect.lineColor = 'Red'
                    CueRemainDur = CueDur - RT
                    win.flip()
                    core.wait(CueRemainDur)
                    Rsp=True
            elif buttonPress != ['2'] and Clock.getTime() > CueDur: # (rect.lineColor is 'Grey' and Clock.getTime() > CueDur) or ()
                Rating = 0
                RT = -1
                Rsp = True
                
        # Set all autoDraw back to False, so that you can present new stimuli on the screen
        for b in buttons:
            b.autoDraw = False
        for l in labels:
            l.autoDraw = False
        Cue.autoDraw = False
        rect.autoDraw = False
        
        if RT == -1:
            # "Hurry Up!"
            Clock = core.Clock()
            while Clock.getTime() < 1:
                Text.text = 'Hurry Up!'
                Text.draw()
                win.flip()
        
        # Delay period - fixation point
        Clock = core.Clock()
        while Clock.getTime() < Delayjit:
            fixationCircle.draw()
            win.flip()
            
        # Outcome display - camera image and outcome image
        Clock = core.Clock()
        while Clock.getTime() < 2:
            Cue.draw()
            OutcomeStim.draw()
            win.flip()
            
        # Reward rating
        for b in buttons:
            b.autoDraw = True
        for l in labels:
            l.autoDraw = True
        rect.autoDraw = True
        Rsp = False
        RewardMarkStart = random.choice(xposList)
        rect.lineColor = 'White'
        xpos = RewardMarkStart
        rect.pos=(xpos,-0.7)
        event.clearEvents()
        Clock= core.Clock() # clock for rating scale
        
        #tracker indicator
        startedPressing=False
        gotFinalPress=False
        while Rsp is False:
            win.flip()
            
            buttonPress=event.getKeys(keyList = ['1','2','3'])
            if len(buttonPress) > 0 and Clock.getTime() < OutcomeDur:
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
                # Confirmation key = 2
                if buttonPress == ['2'] and Clock.getTime() < OutcomeDur: #rect.lineColor is 'Yellow' and 
                    RewardRating = xposList.index(round(xpos,2))+1
                    RewardRT=Clock.getTime()
                    rect.lineColor = 'Red'
                    CueRemainDur = OutcomeDur - RewardRT
                    win.flip()
                    core.wait(CueRemainDur)
                    Rsp=True
                    
            elif buttonPress != ['2'] and Clock.getTime() > OutcomeDur: # (rect.lineColor is 'Grey' and Clock.getTime() > OutcomeDur) or ()
                RewardRating = 0
                RewardRT = -1
                Rsp = True
        for b in buttons:
            b.autoDraw = False
        for l in labels:
            l.autoDraw = False
        rect.autoDraw = False
        
        if RewardRT == -1:
            # "Hurry Up!"
            Clock = core.Clock()
            while Clock.getTime() < 1:
                Text.text = 'Hurry Up!'
                Text.draw()
                win.flip()
                
        # ITI - fixation point
        Clock = core.Clock()
        while Clock.getTime() < ITIjit:
            fixationCircle.draw()
            win.flip()
            
        n+=1
    win.close()
        
        
        
def pracTrials_untimed():
# window setup
    win = visual.Window(color=[0,0,0], screen = 0, fullscr=True, mouseVisible = False)
    mon = monitors.Monitor('testMonitor')
    #winSize = mon.getSizePix()
    event.Mouse(visible=False)
    
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
    
    # Trial randomizer for the whole 96 trials; trials will be further randomized to follow designated rules in each block
    trialList = list(range(1,25))
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
    
    
    # shuffle by 
    for s in range(len(NOList)):
        random.shuffle(NOList[s])
        random.shuffle(OList[s])
    
    # Order randomization using "randomizeOrder" function:
    Index = randomizeOrder(24)
    idxList = Index['typeA']+Index['typeB']+Index['typeC']+Index['typeD']
    idxListO = Index['outcomeA']+Index['outcomeB']+Index['outcomeC']+Index['outcomeD']
    #print(idxList)
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
    Delay = list(itertools.repeat(1,8))+list(itertools.repeat(1,8))+list(itertools.repeat(1,8))
    random.shuffle(Delay)
    ITI = list(itertools.repeat(1,8))+list(itertools.repeat(1,8))+list(itertools.repeat(1,8))
    random.shuffle(ITI)
    CueDur = 6 # for the task, 6  # for pupil diameter - min = 4
    OutcomeDur = 4 # for the task, 4
    
        
    n = 0 # n = 0 for indexing purposes
    while n < 2:
        # experiment
        trialNum = n+1 # for the purpose of indcating the correct trial
        # the Grey box will start at a random number for each trial
        markStart = random.choice(xposList)
        rect.lineColor = 'White'
        xpos = markStart
        rect.pos=(xpos,-0.7)
        typ=[]
        lvl=[]
        # if trial number is not in reward list
        if orderList[n] not in outcomeList:
        # Determine type
            for c in refNOList:
                if orderList[n] in c:
                    typ = refNOList.index(c)+1
                    lvl = math.ceil((c.index(orderList[n])+1)/4)
                    # Cue setup
                    Cue = visual.ImageStim(win,image='images/typ'+str(typ)+'lv'+str(lvl)+'.png', size = (0.8,0.9), units = 'norm')
                    OutcomeStim = visual.TextStim(win,text=u"No Outcome", height = 0.1, wrapWidth = 1,font='Courier New', alignHoriz = 'center', 
                        alignVert = 'center', color = 'yellow',units = 'norm',pos=(0,-0.6))
    
        else:
            for c in refOList:
                if orderList[n] in c:
                    typ = refOList.index(c)+1
                    lvl = math.ceil((c.index(orderList[n])+1)/4)
                    Cue = visual.ImageStim(win,image='images/typ'+str(typ)+'lv'+str(lvl)+'.png', size = (0.8,0.9), units = 'norm')
                    OutcomeStim = visual.ImageStim(win,image = 'images/PracticeOutcome.png',size = (0.5,0.6),units = 'norm')
    
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
        Rsp = False
        event.clearEvents()
        #Clock= core.Clock() # clock for rating scale
        # indicator for eyetracking data
        startedPressing=False
        gotFinalPress=False
        event.clearEvents()
        while Rsp is False:
            win.flip()
            buttonPress=event.getKeys(keyList = ['1','2','3'])
            if len(buttonPress) > 0 :
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
                # Confirmation key = 2, the subject has to move the marker in order to confirm
                # (in other words, the marker has to be Green in order to accept the choice)
                if buttonPress == ['2']: # rect.lineColor is 'Yellow' and 
                    Rating = xposList.index(round(xpos,2))+1
                    #RT=Clock.getTime()
                    rect.lineColor = 'Red'
                    #CueRemainDur = CueDur - RT
                    win.flip()
                    core.wait(2)
                    Rsp=True
                
        # Set all autoDraw back to False, so that you can present new stimuli on the screen
        for b in buttons:
            b.autoDraw = False
        for l in labels:
            l.autoDraw = False
        Cue.autoDraw = False
        rect.autoDraw = False
        
        # Delay period - fixation point
        Clock = core.Clock()
        while Clock.getTime() < Delayjit:
            fixationCircle.draw()
            win.flip()
            
        # Outcome display - camera image and outcome image
        Clock = core.Clock()
        while Clock.getTime() < 2:
            Cue.draw()
            OutcomeStim.draw()
            win.flip()
            
        # Reward rating
        for b in buttons:
            b.autoDraw = True
        for l in labels:
            l.autoDraw = True
        rect.autoDraw = True
        Rsp = False
        RewardMarkStart = random.choice(xposList)
        rect.lineColor = 'White'
        xpos = RewardMarkStart
        rect.pos=(xpos,-0.7)
        event.clearEvents()
        #Clock= core.Clock() # clock for rating scale
        
        #tracker indicator
        startedPressing=False
        gotFinalPress=False
        event.clearEvents()
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
                # Confirmation key = 2
                if buttonPress == ['2']: #rect.lineColor is 'Yellow' and 
                    RewardRating = xposList.index(round(xpos,2))+1
                    #RewardRT=Clock.getTime()
                    rect.lineColor = 'Red'
                    #CueRemainDur = OutcomeDur - RewardRT
                    win.flip()
                    core.wait(2)
                    Rsp=True
                    
        for b in buttons:
            b.autoDraw = False
        for l in labels:
            l.autoDraw = False
        rect.autoDraw = False
    
        # ITI - fixation point
        Clock = core.Clock()
        while Clock.getTime() < ITIjit:
            fixationCircle.draw()
            win.flip()
        n+=1
    win.close()