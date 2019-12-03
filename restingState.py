# resting state
# opens a grey window for two five-minutes session
from psychopy import visual, core, event, monitors, data, tools
import random, datetime, time,itertools, sys, os
from pylink import *

def restingState(subjectID):
    #event.globalKeys.add(key='q',modifiers = ['ctrl'], func = core.quit)
    currentTime=str('%.0f' % time.time())
    currentDirectory=os.path.dirname(os.path.realpath(__file__))
    fileName = currentDirectory + '/data/ETRP_' + str(subjectID) +'/ETRP_' + currentTime + '_' + str(subjectID)
    if not os.path.isdir('data/ETRP_' + str(subjectID)):
        os.makedirs('data/ETRP_'+ str(subjectID))
        print('Error: subject data folder not found.Making a new one.')
        #core.quit()
        
    win = visual.Window(monitor = "testMonitor", fullscr=True, mouseVisible = False)
    mon = monitors.Monitor('testMonitor')
    winSize = mon.getSizePix()
    
    event.Mouse(visible=False)
    
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    # Set up eyelinktracker
    
    eyelinktracker = EyeLink()  #was EyeLink
    RIGHT_EYE = 1
    LEFT_EYE = 0
    BINOCULAR = 2
    
    foreground = (250,250,250) #???
    background = (int(254/2),int(254/2),int(254/2))# check background color on testing date, change if color doesn't match
    screenColor = (192,192,192) #???
    
    edfFileName = "RPRS" + str(subjectID)
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
    
    message = visual.TextStim(win,text=u"Ready", height = 0.2, wrapWidth = 1,font='Courier New',
                alignHoriz = 'center', alignVert = 'center', color = 'Green',units = 'norm')
    for n in range (1,3):
        Rsp = False
        event.clearEvents()
        while Rsp == False:
            message.text = 'Ready'
            message.color = 'green'
            message.draw()
            win.flip()
            buttonPress=event.getKeys(keyList = ['5'])
            if len(buttonPress)>0:
                Rsp = True 
        
        Clock = core.Clock()
        while Clock.getTime() < 300: #300
            # # # # # # # # # # # # # # # # # # 
            getEYELINK().sendMessage('RestingState'+str(n))
            # # # # # # # # # # # # # # # # # # 
            win.flip()
            
        Rsp = False
        event.clearEvents()
        while Rsp == False:
            message.text = 'End of part' + str(n)
            message. color = 'white'
            message.draw()
            win.flip()
            buttonPress=event.getKeys(keyList = ['9'])
            if len(buttonPress)>0:
                Rsp = True
                
    #dataFile.close()
    
    message.text='Thank you for participating!'
    for frame in range(60):
        message.draw()
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