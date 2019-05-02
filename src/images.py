 import numpy as np
import cv2
import glob
import imutils
import scipy as cp

def get_color_masks(img,level=100):#,wb
    
    kernel_erode = np.ones((4,4),np.uint8)
    kernel_dilate = np.ones((6,6),np.uint8)
    
    b = np.mean(img[:,:,2])
    if b!=0:
        r = level / b
        img[:,:,2]=img[:,:,2]*r
    #mg=white_balance(img)
   #img=wb.balanceWhite(img)
    lower_white = np.array([0, 0, 180])
    upper_white = np.array([255,255,255])
    white = cv2.inRange(img, lower_white, upper_white)
    
    #green
    lower_green = np.array([40, 30, 30],np.uint8)
    upper_green = np.array([70, 255, 255],np.uint8)
    green=cv2.inRange(img,lower_green,upper_green)
    
    #yellow
    lower_yellow = np.array([20, 30, 30],np.uint8)
    upper_yellow = np.array([33, 255, 255],np.uint8)
    yellow=cv2.inRange(img,lower_yellow,upper_yellow)
    
    #red
    #red has to be done twice because the revolving ends and starts by red
    lower_red1 = np.array([0,30,30])
    upper_red1 = np.array([9,255,255])
    lower_red2 = np.array([170,30,30])
    upper_red2 = np.array([180,255,255])
    mask0 = cv2.inRange(img, lower_red1, upper_red1)
    mask1 = cv2.inRange(img, lower_red2, upper_red2)
    red = mask0+mask1
    return white,red,yellow,green
    
def undistort_img():
    # Prepare object points 0,0,0 ... 8,5,0
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    
    obj_pts = np.zeros((6*9,3), np.float32)
    obj_pts[:,:2] = np.mgrid[0:9, 0:6].T.reshape(-1,2)
    # Stores all object points & img points from all images
    objpoints = []
    imgpoints = []
    # Get directory for all calibration images
    images = glob.glob('camera_cal/*.png')
    for indx, fname in enumerate(images):
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, (9,6), flags=cv2.CALIB_CB_ADAPTIVE_THRESH)
        if ret == True:
            objpoints.append(obj_pts)
            corners2 = cv2.cornerSubPix(gray,corners,(5,5),(-1,-1),criteria)
            imgpoints.append(corners2)
    # Test undistortion on img
    img_size = (img.shape[1], img.shape[0])
    # Calibrate camera
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, img_size, None,None)
    map1,map2=cv2.initUndistortRectifyMap(mtx,dist,None,mtx,(img.shape[1],img.shape[0]), cv2.CV_32FC1)
    
    return map1,map2
	
def distance_to_camera(knownWidth, focalLength, perWidth):
    # compute and return the distance from the maker to the camera
    return (knownWidth * focalLength) / perWidth
	
def detect_stop(img):

    contours= cv2.findContours(opening,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    c = max(contours, key = cv2.contourArea)

    peri = cv2.arcLength(c, True)

    approx = cv2.approxPolyDP(c, 0.02 * peri, True)
    
    if (7<=len(approx)<=9):
        return 1
    return 0
	
def detect_lights(img_red,img_yellow,img_green):
    
    contours= cv2.findContours(img_red,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    c = max(contours, key = cv2.contourArea)
    M = cv2.moments(c)
    cxr = int(M['m10']/M['m00'])
    cyr = int(M['m01']/M['m00'])
    red=int(cv2.contourArea(c))
    
    contours= cv2.findContours(img_yellow,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    c = max(contours, key = cv2.contourArea)
    M = cv2.moments(c)
    cxy = int(M['m10']/M['m00'])
    cyy = int(M['m01']/M['m00'])
    yellow=int(cv2.contourArea(c))
    
    contours= cv2.findContours(img_green,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    c = max(contours, key = cv2.contourArea)
    M = cv2.moments(c)
    cxg = int(M['m10']/M['m00'])
    cyg = int(M['m01']/M['m00'])
    green=int(cv2.contourArea(c))

    if((np.diff((cyr,cyy,cyg))>=0).all()):
        if(cxr-cxg<=40):
            if (red>yellow):
                if (red>green):
                    return 0
                else:
                    return 1
            elif (yellow>green):
                return 1
            else:
                return 2
    return 3

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