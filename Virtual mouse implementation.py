# # IMPORTING lIBRARIES
import cv2 
import numpy as np

# Setting lower bound and upper bound

#lowerBound=np.array([33,80,40])
#upperBound=np.array([102,255,255])

'''for green
lowerBound=np.array([40,80,40])
upperBound=np.array([65,255,255])

skin color
lowerBound=np.array([0,80,40])
upperBound=np.array([20,255,255])

yelloish
lowerBound=np.array([20, 80, 100])
upperBound=np.array([40,200,300])

for red
lowerBound=np.array([170,120,150])
upperBound=np.array([190,255,255])

for blue
lowerBound=np.array([110,150,100])
upperBound=np.array([120,200,200])'''

#****************

# FOR VIDEO CAPTURE
cam= cv2.VideoCapture(0) 
kernelOpen=np.ones((5,5))
kernelClose=np.ones((20,20))

#font=cv2.InitFont(cv2.FONT_HERSHEY_SIMPLEX,2,0.5,0,3,1)
font = cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255)

#******************

 # IMPORTING lIBRARIES for virtual mouse controller and GUI
import cv2
import numpy as np
from pynput.mouse import Button, Controller
import tkinter as tk
#import wx
mouse=Controller()
#Global variables Setup
#now that we already have all the libraries lets setup all the variables and objects

#app=wx.App(False)
#(sx,sy)=wx.GetDisplaySize()

root = tk.Tk()
sx = root.winfo_screenwidth()
sy = root.winfo_screenheight()
(camx,camy)=(320,240)



lowerBound=np.array([33,80,40])
upperBound=np.array([102,255,255])
# FOR VIDEO CAPTURE
cam= cv2.VideoCapture(0)

#****************

kernelOpen=np.ones((5,5))
kernelClose=np.ones((20,20))
pinchFlag=0

#***************

while True:
    ret, img=cam.read()
    img=cv2.resize(img,(340,220))

    #convert BGR to HSV
    imgHSV= cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    # create the Mask
    mask=cv2.inRange(imgHSV,lowerBound,upperBound)
    #morphology
    maskOpen=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernelOpen)
    maskClose=cv2.morphologyEx(maskOpen,cv2.MORPH_CLOSE,kernelClose)

    maskFinal=maskClose
    conts,h=cv2.findContours(maskFinal.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

    if(len(conts)==2):
        if(pinchFlag==1):
            pinchFlag=0
            mouse.release(Button.left)
        x1,y1,w1,h1=cv2.boundingRect(conts[0])
        x2,y2,w2,h2=cv2.boundingRect(conts[1])
        cv2.rectangle(img,(x1,y1),(x1+w1,y1+h1),(255,0,0),2)
        cv2.rectangle(img,(x2,y2),(x2+w2,y2+h2),(255,0,0),2)
        cx1=x1+w1//2
        cy1=y1+h1//2
        cx2=x2+w2//2
        cy2=y2+h2//2
        cx=(cx1+cx2)//2
        cy=(cy1+cy2)//2
        cv2.line(img, (cx1,cy1),(cx2,cy2),(255,0,0),2)
        cv2.circle(img, (cx,cy),2,(0,0,255),2)
        mouseLoc=int(sx-(cx*sx/camx)), int(cy*sy/camy)
        mouse.position=mouseLoc 
        while mouse.position!=mouseLoc:
            pass
    elif(len(conts)==1):
        x,y,w,h=cv2.boundingRect(conts[0])
        if(pinchFlag==0):
            pinchFlag=1
            mouse.press(Button.left)
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        cx=x+w//2
        cy=y+h//2
        cv2.circle(img,(cx,cy),(w+h)//4,(0,0,255),2)
        mouseLoc=int(sx-(cx*sx/camx)), int(cy*sy/camy)
        mouse.position=mouseLoc 
        while mouse.position!=mouseLoc:
            pass
    cv2.imshow("cam",img)
    cv2.waitKey(2)
