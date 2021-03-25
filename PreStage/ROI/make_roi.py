import os
import cv2
import numpy as np
class selectROI():
    def __init__(self, direc = os.getcwd(), replaceImg = False, scale = 1, ROIColor = (0,0,0)):
        self.get_image_list(direc)
        self.direc = direc
        self.replaceImg = replaceImg
        self.scale = scale
        self.roiName = 'ROI.jpg'
        self.ROIColor = ROIColor
    #Get all image from direc
    def get_image_list(self, direc):
        os.chdir(direc)
        self.paths = [item for item in os.listdir() if ".jpg" in os.path.basename(item) or ".png" in os.path.basename(item) ]
    #Bat su kien click
    def clickPolygonPoints(self, event, x, y, flags, param):
        image_temp = self.refImage.copy()
        if(self.clickEventsEnabled == True):
            if event == cv2.EVENT_LBUTTONDOWN:
                self.refPt.append((x,y))
                if(len(self.refPt) > 1):
                    cv2.line(self.refImage, self.refPt[-1], self.refPt[-2], (0,0,255), 1)
                    cv2.imshow("refImage", self.refImage)
            elif event ==  cv2.EVENT_MOUSEMOVE:
                if(len(self.refPt) > 0):
                    cv2.line(image_temp, self.refPt[-1], (x,y), (0,0,255), 1)
                cv2.imshow("refImage", image_temp)
                image_temp = self.refImage
 
    def applyROI(self):
        if not os.path.isfile(self.roiName):
            print("Please create ROI !!")
        else:
            src = cv2.imread(self.roiName)
            folder = ''
            if not self.replaceImg:
                os.makedirs(self.direc + '/RoiImage', exist_ok=True)
                folder = 'RoiImage/'
            for path in self.paths:
                if path == self.roiName:
                    continue
                img = cv2.imread(path)
                roi = cv2.resize(src=src, dsize=(img.shape[1], img.shape[0]))
                assert img.shape[:2] == roi.shape[:2]
                # scale ROI to [0, 1] => binary mask
                thresh, roi = cv2.threshold(roi, thresh=128, maxval=1, type=cv2.THRESH_BINARY)
                # apply ROI on the original image
                img[np.where((roi==[0,0,0]).all(axis=2))] = self.ROIColor
                savename = folder + path[:-3] + "png"
                cv2.imwrite(savename, img)
                print('ROI ' + savename + ' successfull!')
            print('Done!...')
            if self.replaceImg:
                print('Remove ' + self.roiName)
                os.remove(self.roiName)

    #Ve Roi mask    
    def createROI(self):
        if(len(self.paths) == 0):
            print('Folder empty!')
            return
        self.refImage = cv2.imread(self.paths[0])
        self.refImage = cv2.resize(self.refImage, (int(self.refImage.shape[1] * self.scale), int(self.refImage.shape[0] * self.scale)), interpolation = cv2.INTER_AREA)

        originalRefImage = self.refImage.copy()
        cv2.namedWindow("refImage")
        self.clickEventsEnabled = True #enable event click
        self.refPt = []
        cv2.setMouseCallback("refImage", self.clickPolygonPoints)
        while True:
            cv2.imshow("refImage", self.refImage)
            key = cv2.waitKey(0)
            print(key)
            #reset image
            if key == ord("r"):
                self.refImage = originalRefImage.copy()
                self.refPt = []
                self.currPt, self.nextPt = 0, 1
            #apply image
            if key == ord("p") or key == 13: #press p or enter
                self.clickEventsEnabled = False #disable event click
                self.refImage = originalRefImage.copy()
                break
        #Make the background color white
        width, height = self.refImage.shape[0:2]
        imageROI = self.refImage.copy()
        for i in range(width):
            for j in range(height):
                imageROI[i, j] = [255,255,255]
        #Add ROI to background
        pointsArray = np.array(self.refPt)
        mask = np.zeros(imageROI.shape, dtype=np.uint8)
        white = (255,255,255)
        cv2.fillPoly(mask, np.int32([pointsArray]), white)
        self.refImage = cv2.bitwise_and(imageROI, mask) 
        
        #Show and save result
        cv2.destroyAllWindows()
        cv2.imshow("Result", self.refImage)  
        print("Saving",self.roiName)
        cv2.imwrite(self.roiName, self.refImage)
        print("Done.")
        cv2.waitKey(0)
        cv2.destroyAllWindows()