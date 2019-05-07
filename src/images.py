import numpy as np
import cv2
import glob
import imutils
import scipy as cp

def get_color_masks(img,level=100):#,wb
    
    
    lower_white = np.array([0, 0, 210])
    upper_white = np.array([255,45,255])
    white = cv2.inRange(img, lower_white, upper_white)
	
    
    #green
    lower_green = np.array([35, 20, 20],np.uint8)
    upper_green = np.array([72, 255, 255],np.uint8)
    green=cv2.inRange(img,lower_green,upper_green)
    
    
    #red
    #red has to be done twice because the revolving ends and starts by red
    lower_red1 = np.array([0,60,60])
    upper_red1 = np.array([10,255,255])
    lower_red2 = np.array([160,60,60])
    upper_red2 = np.array([179,255,255])
    mask0 = cv2.inRange(img, lower_red1, upper_red1)
    mask1 = cv2.inRange(img, lower_red2, upper_red2)
    red = mask0+mask1
    return white,red,green
    

	
def detect_stop(img):

    contours= cv2.findContours(img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    if len(contours)!=0:
        c = max(contours, key = cv2.contourArea)

        peri = cv2.arcLength(c, True)

        approx = cv2.approxPolyDP(c, 0.015 * peri, True)
        x,y,w,h = cv2.boundingRect(approx)
        if ((abs(w-h)<15) and (w>10)):
            if (7<=len(approx)<=10):
                distance=1500/w
                return 1,int(distance)
            else:
                return 0,0
        else:
            return 0,0
    return 0,0
def detect_lights(grey,img_red,img_green):
    a=0
	
    contours= cv2.findContours(img_green,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    if len(contours)!=0:
        c1 = max(contours, key = cv2.contourArea)
        M = cv2.moments(c1)
        if M['m00']!=0:
            a=a+1
            cxg = int(M['m10']/M['m00'])
            cyg = int(M['m01']/M['m00'])
            green=int(cv2.contourArea(c1))
            

    contours= cv2.findContours(img_red,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    if len(contours)!=0:

        c2 = max(contours, key = cv2.contourArea)
        M = cv2.moments(c2)
        if M['m00']!=0:
            a=a+1
            cxr = int(M['m10']/M['m00'])
            cyr = int(M['m01']/M['m00'])
            red=int(cv2.contourArea(c2))
            
			
    
    
    if (a==2):
        green_image = np.zeros((240,320,3), np.uint8)
        cv2.drawContours(green_image, c1, 0, (0,255,0), -1)
        mask_grey=cv2.cvtColor(green_image,cv2.COLOR_BGR2GRAY)
        mean_green= cv2.mean(grey,mask = mask_grey)
		
        red_image = np.zeros((240,320,3), np.uint8)
        cv2.drawContours(red_image, c2, 0, (0,255,0), -1)
        mask_grey=cv2.cvtColor(red_image,cv2.COLOR_BGR2GRAY)
        mean_red= cv2.mean(grey,mask = mask_grey)
        if((green>200) and (red>200)):
            if(abs(cyr-cyg)<=30):
                if (mean_green>mean_red):
                    return 1
                else:
                    return 2
    return 0

def detect_line(white):

  
    contours=cv2.findContours(white, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    contours= imutils.grab_contours(contours)
    if len(contours)!=0:
        c = max(contours, key = cv2.contourArea)
        peri = cv2.arcLength(c, True)
        c = cv2.approxPolyDP(c, 0.02 * peri, True)
        M = cv2.moments(c)
        if M['m00']!=0:
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            return cx
        else:
            return 0
    else:
        return 0