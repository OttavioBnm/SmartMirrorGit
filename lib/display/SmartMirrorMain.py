import P3picam
import subprocess

motionState = False
oldMotion = False

while True: 
    oldMotion = motionState
    motionState = P3picam.motion()
    
    if(motionState and oldMotion == False):
        print("mouvement")
        
    elif(motionState == False and oldMotion):
        print("----")