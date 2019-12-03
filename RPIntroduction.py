# RP introduction
from psychopy import visual, core, event, data, tools, monitors
from psychopy.iohub import launchHubServer
import scipy.io as sio
import numpy as np
import time, os, sys,csv, random
from practiceTrials import pracTrials_untimed
from practiceTrials import pracTrials


#event.globalKeys.add(key='q',modifiers = ['ctrl'], func = core.quit)
def Intro(subjectID):
    win = visual.Window(color=[0,0,0],screen=0, fullscr=True, mouseVisible = False)
    event.Mouse(visible=False)
    mov1 = visual.MovieStim3(win, filename = 'IntroVideo\R&P instruction_1.mp4', size=(1920, 1080),
        flipVert=False, flipHoriz=False, loop=False, autoLog = False)
    mov2 = visual.MovieStim3(win, filename = 'IntroVideo\R&P instruction_2.mp4', size=(1920, 1080),
        flipVert=False, flipHoriz=False, loop=False, autoLog = False)
    mov3 = visual.MovieStim3(win, filename = 'IntroVideo\R&P instruction_3.mp4', size=(1920, 1080),
        flipVert=False, flipHoriz=False, loop=False, autoLog = False)
    mov4 = visual.MovieStim3(win, filename = 'IntroVideo\R&P instruction_4.mp4', size=(1920, 1080),
        flipVert=False, flipHoriz=False, loop=False, autoLog = False)
    mov5 = visual.MovieStim3(win, filename = 'IntroVideo\R&P instruction_5.mp4', size=(1920, 1080),
        flipVert=False, flipHoriz=False, loop=False, autoLog = False)
    mov6 = visual.MovieStim3(win, filename = 'IntroVideo\R&P instruction_6.mp4', size=(1920, 1080),
        flipVert=False, flipHoriz=False, loop=False, autoLog = False)
     
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
    Cue = visual.ImageStim(win,image = 'images/Intro1.png', size = (1,1), units = 'norm')
    Text = visual.TextStim(win,text=u"+", height = 0.08, wrapWidth = 1,font='Courier New',
                alignHoriz = 'center', alignVert = 'center', color = 'white',units = 'norm')
    for n in range(1,6):
        if n == 1:
            while mov1.status != visual.FINISHED:
                mov1.draw()
                win.flip()
        
            markStart = random.choice(xposList)
            rect.lineColor = 'White'
            xpos = markStart
            rect.pos=(xpos,-0.7)
            
            # set stimuli autoDraw to True so they would show up on every frame, avoid screen display twinkle:
            for b in buttons:
                b.autoDraw = True
            for l in labels:
                l.autoDraw = True
            Cue.autoDraw = True
            rect.autoDraw = True
            # Cue rating
            event.clearEvents()
            Rsp = False
            #Clock= core.Clock() # clock for rating scale
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
        
        if n == 2: 
            while mov2.status != visual.FINISHED:
                mov2.draw()
                win.flip()
            markStart = random.choice(xposList)
            Rsp = False
            rect.lineColor = 'White'
            xpos = markStart
            rect.pos=(xpos,-0.7)
            
            # set stimuli autoDraw to True so they would show up on every frame, avoid screen display twinkle:
            for b in buttons:
                b.autoDraw = True
            for l in labels:
                l.autoDraw = True
            Cue.autoDraw = False
            rect.autoDraw = True
            # Cue rating
            event.clearEvents()
            #Clock= core.Clock() # clock for rating scale
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
                        rect.lineColor = 'Red'
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
        
        if n == 3: 
            while mov3.status != visual.FINISHED:
                mov3.draw()
                win.flip()
        
            markStart = random.choice(xposList)
            Rsp = False
            rect.lineColor = 'White'
            xpos = markStart
            rect.pos=(xpos,-0.7)
            Cue.image = 'images\\typ3lv3.png'
            # set stimuli autoDraw to True so they would show up on every frame, avoid screen display twinkle:
            for b in buttons:
                b.autoDraw = True
            for l in labels:
                l.autoDraw = True
            Cue.autoDraw = True
            rect.autoDraw = True
            # Cue rating
            event.clearEvents()
            #Clock= core.Clock() # clock for rating scale
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
                        rect.lineColor = 'Red'
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
            
        if n == 4: 
            while mov4.status != visual.FINISHED:
                mov4.draw()
                win.flip()
            markStart = random.choice(xposList)
            Rsp = False
            rect.lineColor = 'White'
            xpos = markStart
            rect.pos=(xpos,-0.7)
            
            # set stimuli autoDraw to True so they would show up on every frame, avoid screen display twinkle:
            for b in buttons:
                b.autoDraw = True
            for l in labels:
                l.autoDraw = True
            Cue.autoDraw = False
            rect.autoDraw = True
            # Cue rating
            event.clearEvents()
            #Clock= core.Clock() # clock for rating scale
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
                        rect.lineColor = 'Red'
                        #CueRemainDur = CueDur - RT
                        win.flip()
                        #core.wait(CueRemainDur)
                        Rsp=True
                    
            # Set all autoDraw back to False, so that you can present new stimuli on the screen
            for b in buttons:
                b.autoDraw = False
            for l in labels:
                l.autoDraw = False
            Cue.autoDraw = False
            rect.autoDraw = False
            
        if n == 5:
            while mov5.status != visual.FINISHED:
                mov5.draw()
                win.flip()
        
            AnsList = ['4','2','3','1','2','2','4','1']
            Text.text = 'To make sure that you remember these things,\nwe’ll ask you a few questions about what you’ve just learned.\nTo choose your answer, press the corresponding number on the keyboard.\n\n[Press 5 to start]'
            
            event.clearEvents()
            Rsp = False
            while Rsp is False:
                Text.draw()
                win.flip()
                buttonPress=event.getKeys(keyList = ['5'])
                if len(buttonPress)>0:
                        Rsp = True
            
            for PracNum in range(1,9):
                PracProb = visual.ImageStim(win,image = 'C:\\Users\\levylab\\Documents\\Reward_and_Punishment\\images\\PracProb'+str(PracNum)+'.png', size = (1.5,1), units = 'norm')
                event.clearEvents()
                Rsp = False
                while Rsp is False:
                    PracProb.draw()
                    win.flip()
                    buttonPress = event.getKeys(keyList = ['1','2','3','4'])
                    if len(buttonPress) > 0:
                        if buttonPress[0] == AnsList[PracNum-1]:
                            Text.text = 'Correct!'
                            Text.draw()
                            win.flip()
                            core.wait(1)
                            Rsp = True
                        else:
                            Text.text = 'Try again.'
                            Text.draw()
                            win.flip()
                            core.wait(1)
                            Rsp = False
        
            Text.text = 'Next, we will do two practice trials. For these trials, you will have as much time as you want to make your ratings and view the shapes. Let the experimenter know if you have any questions during the practice trials.\n\nNote: "Outcome information" will be replaced with actual outcomes in experiment.\n\n[Press 5 to start]'
            event.clearEvents()
            Rsp = False
            while Rsp is False:
                Text.draw()
                win.flip()
                buttonPress=event.getKeys(keyList = ['5'])
                if len(buttonPress)>0:
                    Rsp = True
                    core.wait(0.5)
            #win.close()
            pracTrials_untimed()
        
            Text.text = 'In the actual experiment, the trials will go by very  quickly. You will only have about 6 seconds to make the first rating, and 4 seconds to make the second rating.\nNext, we’ll do some practice trials in real time, so you can see what the trials will actually be like.\n\n[Press 5 to start]'
            Rsp = False
            while Rsp is False:
                Text.draw()
                win.flip()
                buttonPress=event.getKeys(keyList = ['5'])
                if len(buttonPress)>0:
                        Rsp = True
            #win.close()
            pracTrials()
                
            while mov6.status != visual.FINISHED:
                mov6.draw()
                win.flip()