import os
import glob
import cv2
#Change Folder, example: "D:/IT Majors/Thesis Outline/testLabel/"
import argparse
import cv2
import numpy as np
import copy

nameWindow = "Plase select ROI"
class selectROI():

    def __init__(self):
    
        self.refPt = []
        self.currPt = 0
        self.nextPt = 1
        self.clickEventsEnabled = False
        self.drawingRectangle = False
        self.rectangleDrawn = False
        self.drawingPolygonLine = False
        self.polygonLineDrawn = False
        self.ix = -1
        self.iy = -1
        
        self.refImage = None
    
    def clickPolygonPoints(self, event, x, y, flags, param):

        image_temp = self.refImage.copy()
        
        if(self.clickEventsEnabled == True):
            if event == cv2.EVENT_LBUTTONDOWN:
                if((self.drawingRectangle == False) & (self.rectangleDrawn == False)):
                    self.drawingPolygonLine = True
                    self.refPt.append((x,y))
                if(len(self.refPt) > 1):
                    cv2.line(self.refImage, self.refPt[self.currPt], self.refPt[self.nextPt], (0,0,255), 1)
                    cv2.imshow(nameWindow, self.refImage)
                    self.currPt += 1
                    self.nextPt += 1  
            elif event == cv2.EVENT_LBUTTONUP:
                if((self.drawingRectangle == False) &(self.drawingPolygonLine == True)):
                    self.polygonLineDrawn == True
            elif event == cv2.EVENT_RBUTTONDOWN:
                if((self.drawingPolygonLine == False) & (self.polygonLineDrawn == False) & (self.rectangleDrawn == False)):
                    self.drawingRectangle = True
                    self.ix,self.iy = x,y
                    self.refPt.append((x,y))
            elif event == cv2.EVENT_RBUTTONUP:
                if((self.drawingPolygonLine == False) & (self.polygonLineDrawn == False) & (self.rectangleDrawn == False)):
                    self.drawingRectangle = False
                    self.rectangleDrawn = True
                    cv2.rectangle(self.refImage, (self.ix,self.iy), (x,y), (0,0,255), 1)
                    self.refPt.append((self.ix,self.iy))
                    self.refPt.append((x,self.iy))
                    self.refPt.append((x,y))
                    self.refPt.append((self.ix,y))
                    cv2.imshow(nameWindow, self.refImage)
            elif event ==  cv2.EVENT_MOUSEMOVE:
                if(self.drawingRectangle == True):
                    cv2.rectangle(image_temp, (self.ix,self.iy), (x,y), (0,0,255), 1)
                    cv2.imshow(nameWindow, image_temp)
                    image_temp = self.refImage
                elif((self.drawingPolygonLine == True)):
                    cv2.line(image_temp, self.refPt[self.currPt], (x,y), (0,0,255), 1)
                    cv2.imshow(nameWindow, image_temp)
                    image_temp = self.refImage

    def maskImgWithROI(self, aImage, aROIPointsList):
        pointsArray = np.array(aROIPointsList)
        mask = np.zeros(aImage.shape, dtype=np.uint8)
        white = (255,255,255)
        cv2.fillPoly(mask, np.int32([pointsArray]), white)
        maskedImage = cv2.bitwise_and(aImage, mask)
        return maskedImage  
        
    def outputROIMask(self, aImage, aROIPointsList):
        pointsArray = np.array(aROIPointsList)
        pointsArray = pointsArray.reshape((-1,1,2))
        mask = np.zeros(aImage.shape, dtype=np.uint8)
        white = (255,255,255)
        cv2.fillPoly(mask, np.int32([pointsArray]), white)
        return mask  
        
    def runInterface(self, refImage):
        self.refImage = cv2.imread(refImage)
        originalRefImage = self.refImage.copy()
        
        cv2.namedWindow(nameWindow)
        self.clickEventsEnabled = True
        cv2.setMouseCallback(nameWindow, self.clickPolygonPoints)

        while True:
            cv2.imshow(nameWindow, self.refImage)
            key = cv2.waitKey(0)
           
            if key == ord("r"):
                self.refImage = originalRefImage.copy()
                self.refPt = []
                self.currPt, self.nextPt = 0, 1
                self.drawingRectangle = False
                self.rectangleDrawn = False
                self.drawingPolygonLine = False
                self.polygonLineDrawn = False
                self.ix, self.iy = -1,-1
            
            if key == ord("p"):
                self.clickEventsEnabled = False
                self.refImage = originalRefImage.copy()
                self.drawingRectangle = False
                self.rectangleDrawn = False
                self.drawingPolygonLine = False
                self.polygonLineDrawn = False
                break

        self.refImage = self.maskImgWithROI(self.refImage, self.refPt)
        #cv2.imshow("refImage", self.refImage)
	
        savename=str(refImage).replace(".jpg","Roi.jpg")
        print("Saving",savename)
        cv2.imwrite(savename, self.refImage)
        print("Done.")
        #cv2.waitKey(0)
        cv2.destroyAllWindows()
        return self.refImage

#roiMask = self.outputROIMask(self.refImage, self.refPt) #Ve ROI Mask
#cv2.imwrite("ROI.jpg", roiMask) #save ROI mask

#selROI = selectROI()
#selROI.runInterface(refImage='image-1.jpg')
unlabeled = True #False ís browse through all images
direc = os.getcwd()
os.chdir(direc)
paths = [item for item in os.listdir() if ".jpg" in os.path.basename(item) and "Roi.jpg" not in os.path.basename(item)]
print(paths)
def apply_roi(img, roi):
    # resize ROI to match the original image size
    roi = cv2.resize(src=roi, dsize=(img.shape[1], img.shape[0]))
    
    assert img.shape[:2] == roi.shape[:2]
    
    # scale ROI to [0, 1] => binary mask
    thresh, roi = cv2.threshold(roi, thresh=128, maxval=1, type=cv2.THRESH_BINARY)
    
    # apply ROI on the original image
    new_img = img * roi
    return new_img

def AnnotateImage(Image):
    # Select ROI
    showCrosshair = False
    fromCenter = False
    r = cv2.selectROI("Click or Select Bounding Box to Annotate a Vehicle", Image, fromCenter, showCrosshair)
    #Get centroid
    x = int((int(r[0])+int(r[0] + r[2]))/2)
    y = int((int(r[1])+int(r[1] + r[3]))/2)
    #cv2.destroyAllWindows()
    #Return 
    if (x==0 & y==0):
        return False, [0, 0]
    #point = str(x) + " " + str(y)
    #print(point)
    for i in range(-2, 2):
        for j in range(-2, 2):
            img[y+i, x+j] = [0, 0, 255]
    return True, [x, y]
Scale = 1
selROI = selectROI()
for path in paths:
    #Open file
    print("Open: ", path)
    img = cv2.imread(path)
    # roi = cv2.imread("ROI.png") #truong hop da ve file ROI san
    # img = apply_roi(img, roi)
    #cv2.imwrite(os.path.basename(path), img)
    
    #read name file
    base = os.path.basename(path)
    fileTxt = os.path.splitext(base)[0] + ".txt"
    #set up
    points = []
    firstline = True
    if (unlabeled and os.path.isfile(fileTxt)):
        print(path, "has been labeled")
        continue
    cv2.destroyAllWindows()
    #
    img = selROI.runInterface(path)
    #...
    #Co su kien bat phim r -> remove ROI
    #Phim p -> apply ROI
    img = cv2.resize(img, None, fx=Scale, fy=Scale)
    if (os.path.isfile(fileTxt)): #Check tep txt ton tai hay khong
        f = open(fileTxt, "r")  # Mo tep
        points_temp = f.readlines()
        f.close()
        for i in points_temp:
            point = i.replace("\n", "")
            point = point.split(" ")
            #Scale diem
            x = round(int(point[0])*Scale)
            y = round(int(point[1])*Scale)
            #Them diem vao list Point
            points.append([x, y])
            #Ve cham xanh cac diem
            for a in range(-2, 2):
                for b in range(-2, 2):
                    img[y + a, x + b] = [0, 255, 0]
    # save annotation to "points"
    flag, pointTemp = AnnotateImage(img)
    while flag:
        points.append(pointTemp)
        flag, pointTemp = AnnotateImage(img)
    if len(points) == 0: continue
    points_temp = points.copy()
    points = ""
    if(len(points_temp)>0):
        point = points_temp[0]
        x = point[0]
        y = point[1]
        points += str(round(x / Scale)) + " " + str(round(y / Scale))
        for i in range(1, len(points_temp)):
            point = points_temp[i]
            x = point[0]
            y = point[1]
            points += "\n" + str(round(x / Scale)) + " " + str(round(y / Scale))

    #show the result
    #cv2.destroyAllWindows()
    #cv2.imshow("Result", img)
    #cv2.waitKey(0)
    cv2.destroyAllWindows()

    #write file txt
    print(points)
    f = open(fileTxt, 'w')
    f.write(points)
    f.close()
    print("Saving... ", fileTxt, "...Done!")

    #Wait Key
    #pause = input("Press enter to continue, press key + enter to exit: ")
    #if pause == '':
    #    continue

    #print("Exit")
    #break