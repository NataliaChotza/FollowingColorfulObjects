import cv2 as cv
import numpy as np
import argparse
import sys
import colorsys

frame = None
hsv_frame = None
res = None
w=0
he=0
xi=0
yi=0
cnts=[]
lower_limit = None
upper_limit = None

h=0
s=0
v=0

'''
This is a method where as an argument its given frame and which 
gives back frame after dilatations and erosions

'''
def ero_di(res):
    res_de= cv.dilate(res,np.ones((7,7)),iterations=6)
    res_er = cv.erode(res_de,np.ones((7,7)),iterations=2)
    return res_er

'''
This is a method called while left button being down and up. 
In this method the lower and upper limit of colors is saved 
for each pressed pixel

'''

def mouse_click(event, x, y, flags, param):
    global lower_limit, upper_limit,hsv_frame,res,frame,h,s,v
    lower_limit = None
    upper_limit = None
    
    
    if event == cv.EVENT_LBUTTONDOWN:

        h = hsv_frame[y,x,0]
        s = hsv_frame[y,x,1]
        v = hsv_frame[y,x,2]

    
        if lower_limit is None:

             lower_limit = np.array([h-20,s-50,v-40])
        if upper_limit is None:

             upper_limit = np.array([h+20,s+50,v+40])
                
    elif event == cv.EVENT_LBUTTONUP: 
        h = hsv_frame[y,x,0]
        s = hsv_frame[y,x,1]
        v = hsv_frame[y,x,2]
            

        if lower_limit is None:

            lower_limit = np.array([h-20,s-50,v-40])
        if upper_limit is None:

            upper_limit = np.array([h+20,s+50,v+40])
                 
'''
This is the main method of a program where each frame in a video 
is changed according to colors. BY default until nothing is pressed the 
upper and lower array is filled with data for color red. Later when 
mousecallback is on the arrays are changed to values of pixels.
* 
cnts is an array filled for each frame separatedly which saves 
contours for eroded and delated frame and based on this later are 
created rectangles


'''                  
        
def main(args):
    global frame,hsv_frame,res,w,he,xi,yi,cnts,lower_limit,upper_limit,h,s,v
    
    if args.input_video == None:
        video = cv.VideoCapture(1)#---camera
        vi=True
    else:
        video = cv.VideoCapture(args.input_video)
        vi=False
        if video.isOpened() == False:
            print('Error to open')
            sys.exit()

    cv.namedWindow('window')
    cv.setMouseCallback('window',mouse_click)
  
    while True:
       if vi ==True: 
           video = cv.VideoCapture(0)#---camera
           _,frame=video.read()
    
       else:         
           _, frame = video.read() 
       
       hsv_frame = cv.cvtColor(frame,cv.COLOR_BGR2HSV)
       
       key = cv.waitKey(1)
       if key == ord('q'):
            break
       if key == ord('p'):
           cv.waitKey(-1)  
       
       if lower_limit is None:
            lower_limit = np.array([10,30,255])
       if upper_limit is None:
            upper_limit = np.array([10,30,255])
       
       
       mask = cv.inRange(hsv_frame,lower_limit,upper_limit)
       res=cv.bitwise_and(hsv_frame,hsv_frame,mask=mask)
       
       hsv_IMG = cv.cvtColor(res,cv.COLOR_HSV2BGR)
       hsv_IMG= cv.cvtColor(hsv_IMG,cv.COLOR_BGR2GRAY)
     
       ret,tframe = cv.threshold(hsv_IMG,0,255,cv.THRESH_BINARY)
       erodedDilatedFrame = ero_di(tframe)
       
       cnts.clear()
       (cnts,_) = cv.findContours(erodedDilatedFrame.copy(),cv.RETR_EXTERNAL,
                        cv.CHAIN_APPROX_SIMPLE) 
       
       color=hsv2rgb(h,s,v)
       
       for cnt in cnts:
            print(cnt)
            xi,yi,w,he = cv.boundingRect(cnt)
            cv.rectangle(frame,(xi,yi),(xi+w,yi+he),color,2)   

       cv.imshow('window',frame)
       cv.setMouseCallback('window',mouse_click)
           
 
    video.release()
    cv.destroyAllWindows()
    
'''
This is the method which makes tuple of color which in main method 
is used to make rectangle around pressed object with the same color
as an object.
'''    
def hsv2rgb(h,s,v):   
    color = tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h*100/360,s*100/360,v*100/360))
    return color
'''
This is a simple method which is responsible for creating the 
parsed arguments
'''                  

def parse_args():
   parser = argparse.ArgumentParser()
   parser.add_argument('-i','--input_video',required=False,default=None)
   return parser.parse_args()

if __name__== '__main__':
    main(parse_args())