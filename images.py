import numpy as np
import cv2
import glob
import imutils
import scipy as cp

#function to get the masks of white, red and green color
#img is an hsv image
def get_color_masks(img,level=100):#,wb
    
    
    lower_white = np.array([0, 0, 130])#lower point of the white rectangle
    upper_white = np.array([255,10,255])#upper point of the white rectnagle
    white = cv2.inRange(img, lower_white, upper_white)#only the pixel in the white rectangle are kept, the others are black (binary image)
	
    white = cv2.erode(white,(5,5),iterations = 2)#used to erase the small enough noise
    white = cv2.dilate(white,(9,9),iterations = 1)#increase the main contours back after the erode
    
	
    
    #green
    lower_green = np.array([35, 20, 20],np.uint8)#lower point of the green rectangle
    upper_green = np.array([72, 255, 255],np.uint8)#upper point of the green rectangle
    green=cv2.inRange(img,lower_green,upper_green)#only the pixel in the green rectangle are kept, the others are black (binary image)
    
    
    #red
    #red has to be done twice because the revolving ends and starts by red
    lower_red1 = np.array([0,70,10])#lower point of the first red rectangle
    upper_red1 = np.array([10,255,255])#upper point of the first red rectangle
    lower_red2 = np.array([170,70,10])#lower point of the second red rectangle
    upper_red2 = np.array([180,255,255])#upper point of the second red rectangle
    mask0 = cv2.inRange(img, lower_red1, upper_red1)#only the pixel in the first red rectangle are kept, the others are black (binary image)
    mask1 = cv2.inRange(img, lower_red2, upper_red2)#only the pixel in the second red rectangle are kept, the others are black (binary image)
    red = mask0+mask1#both masks are added
    red = cv2.morphologyEx(red, cv2.MORPH_OPEN, (5,5,),iterations=2)#remove noise 
    red = cv2.dilate(red,(5,5),iterations = 2)#incread main objects to fill up and connect different parts 
    red = cv2.morphologyEx(red, cv2.MORPH_CLOSE, (5,5),iterations=2)#remove holes in main objects detected
    white=white[100:240,20:300]#resize white so we only keep the part with the line
    return white,red,green
    

#used to detect a stop in the red mask	
def detect_stop(img):

    contours= cv2.findContours(img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)#search for contours in the red mask
    contours = imutils.grab_contours(contours)#only keep the contours from the findContours return
    if len(contours)!=0:#check that at least one contour was detected
        c = max(contours, key = cv2.contourArea)#keep the one with the biggest area

        peri = cv2.arcLength(c, True)#compute the perimeter of this contour

        approx = cv2.approxPolyDP(c, 0.025 * peri, True)#create an approximation contour of the previous so we can check if it is an octogone
		#0.03*peri is how much the length of the approx contour can be different of the detected one
        x,y,w,h = cv2.boundingRect(approx)#return the bottom-left point of the rectangle enclosing the contour, it's width and heigth
        if ((abs(w-h)<30) and (w>20)):#check that the contour is big enough and that width is similar to heigth
            if (7<=len(approx)<=9):#check that is has a correct amount of vertices
                distance=3750/w#compute the distance from the camera(value was computed before hand by the rule of three
                return 1,int(distance)
            else:
                return 0,0
        else:
            return 0,0
    return 0,0

#used to detect the traffic ligth
def detect_lights(grey,img_red,img_green):
    a=0#flag used to check at the end that both red and green was detected
	
    contours= cv2.findContours(img_green,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)#detect contours in the green mask
    contours = imutils.grab_contours(contours)
    if len(contours)!=0:#check that at least one was detected
        c1 = max(contours, key = cv2.contourArea)#keep the biggest one
        M = cv2.moments(c1)#compute the moments of the contour
        if M['m00']!=0:#check that 'm00' is not null to avoid division by zero
            a=a+1
            cxg = int(M['m10']/M['m00'])
            cyg = int(M['m01']/M['m00'])
            green=int(cv2.contourArea(c1))#keep the area of this contour as we detect the biggest contours as the brigthess one because the ligth
			#makes it look bigger in hsv
            
    #the same is done for the red mask as fot the green
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
            
			
    
    
    if (a==2):#check that both were detected
    #the two 4-line blocks below are used to draw the filled contours on a black image and get the average brightness whit cv2.mean
        green_image = np.zeros((240,320,3), np.uint8)
        cv2.drawContours(green_image, c1, 0, (0,255,0), -1)
        mask_grey=cv2.cvtColor(green_image,cv2.COLOR_BGR2GRAY)
        mean_green= cv2.mean(grey,mask = mask_grey)
		
        red_image = np.zeros((240,320,3), np.uint8)
        cv2.drawContours(red_image, c2, 0, (0,255,0), -1)
        mask_grey=cv2.cvtColor(red_image,cv2.COLOR_BGR2GRAY)
        mean_red= cv2.mean(grey,mask = mask_grey)
        if((green>200) and (red>200)):#check the area are big enough(to prevent false positive)
            if(abs(cyr-cyg)<=30):#check that there are vertically aligned
                if (mean_green>mean_red):#if green is bigger it is the one brigth, if not red is brigth
                    return 1
                else:
                    return 2
    return 0

#used to detect the centoid of the line
def detect_line(white):

  
    contours=cv2.findContours(white, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)#detect contours in the white mask
    contours= imutils.grab_contours(contours)
    if len(contours)!=0:#check that at least one was detected
        c=contours[0]#set up the maximum with the first one in the list of contours
        for contour in contours:#if the currently checked contour has a greater perimeter it becomes the temporary biggest contour until all are checked
            if(cv2.arcLength(c,True)<=cv2.arcLength(contour,True)):
                c=contour
        peri = cv2.arcLength(c, True)#compute the perimeter of the greatest contour
        c = cv2.approxPolyDP(c, 0.02 * peri, True)#compute an approximation of the gretest contoru
        M = cv2.moments(c)#compute the moments of this contour
        if M['m00']!=0:#if m00 not null
            cx = int(M['m10']/M['m00'])#compute the x of centroid
            cy = int(M['m01']/M['m00'])#compute the y of centroid
            return cx
        else:
            return 0
    else:
        return 0