from PictureRating import PicRating
from ranking import PicRanking
from sortRankPic import sortRankPic
from RPIntroduction import Intro
from practiceTrials import pracTrials
from RPScript_full_bhv_newtimer import RPbhv
from RPScript_full_bhv_newtimerET import RPET
from restingState import restingState
from psychopy import core, event

event.globalKeys.add(key='q',modifiers = ['ctrl'], func = core.quit)
# what is the subject ID?
subjectID = 13

whichTask = 5

#Run 1 and 2 in behavior room
if whichTask == 1:
    PicRating(subjectID)
    PicRanking(subjectID)
    sortRankPic(subjectID)

if whichTask == 2:
    Intro(subjectID)

# If not automatically set when connected to the display at MRRC, change display setting to 400*800
#Run 3 and 4 when subject is in the scanner

# 3 ==> runs 5 practice trials
if whichTask == 3:
    pracTrials()
    
# 4 ==> runs the full task
if whichTask == 4:
    #RPbhv(subjectID)
    RPET(subjectID)  # eyetracking version

# 5 ==> runs resting state
if whichTask == 5:
    restingState(subjectID)
