"""
Author: Duong Le
Github: https://github.com/lhduong1999
"""
import os, inspect
import cv2

class MakeLabel:
    def __init__(self, direc, unlabeled = False, scale = 2):
        self.get_image_list(direc)
        self.unlabeled = unlabeled
        self.scale = scale
        pass

    def get_image_list(self, direc):
        os.chdir(direc)
        self.paths = [item for item in os.listdir() if ".jpg" in os.path.basename(item)]
        #print(self.paths)

    def AnnotateImage(self, img,imgOriginal, points):
        img = cv2.putText(img, 'Total point: ' + str(len(points)), (50, 50) , cv2.FONT_HERSHEY_SIMPLEX ,  
                   1, (255, 0, 0) , 2, cv2.LINE_AA) 
        r = cv2.selectROI("Image: " + str(self.nameImg) +" ("+ str(self.currentImg) + "/" + str(self.totalImg) + ")", img=img, fromCenter=False, showCrosshair= False)
        x = int((int(r[0])+int(r[0] + r[2]))/2)
        y = int((int(r[1])+int(r[1] + r[3]))/2)
        if (x==0 & y==0):
            return False
        #add icon to image
        if(r[2]<5 and r[3]<5):
            print('Add point') 
            for i in range(-2, 2):
                            for j in range(-2, 2):
                                img[y+i, x+j] = [0,0,255]
            points.append([x, y])
        else: 
            print('Remove point')
            x1 = int(r[0])
            x2 = int(r[0] + r[2])
            y1 = int(r[1])
            y2 = int(r[1] + r[3])
            for x in range(x1,x2):
                for y in range(y1,y2):
                    img[y, x] = imgOriginal[y,x]
                    if [x,y] in points:
                        points.remove([x, y])
        x1,x2,y1,y2 = 50,350,0,80
        for x in range(x1,x2):
                for y in range(y1,y2):
                    img[y, x] = imgOriginal[y,x]
        return True

    #start make label
    def start(self):
        scale = self.scale
        unlabeled = self.unlabeled
        self.totalImg = len(self.paths)
        self.currentImg = 0
        for path in self.paths:
            self.currentImg += 1
            #Open file
            print("Open: ", path)
            img = cv2.imread(path)
            img = cv2.resize(img, None, fx=scale, fy=scale)
            imgOriginal = img.copy()
            #read name file
            base = os.path.basename(path)
            fileTxt = os.path.splitext(base)[0] + ".txt"
            #set up
            points = []
            if (unlabeled and os.path.isfile(fileTxt)):
                f = open(fileTxt, "r")  # Mo tep
                points_temp = f.readlines()
                f.close()
                print(fileTxt,len(points_temp))
                if(len(points_temp) > 0):
                    print(path, "has been labeled")
                    continue
            if (os.path.isfile(fileTxt)): #Check tep txt ton tai hay khong
                f = open(fileTxt, "r")  # Mo tep
                points_temp = f.readlines()
                f.close()
                for i in points_temp:
                    point = i.replace("\n", "")
                    point = point.split(" ")
                    #Scale diem
                    x = round(int(point[0])*scale)
                    y = round(int(point[1])*scale)
                    #Them diem vao list Point
                    points.append([x, y])
                    #Ve cham xanh cac diem
                    for a in range(-2, 2):
                        for b in range(-2, 2):
                            img[y + a, x + b] = [0, 255, 0]
            self.nameImg = os.path.basename(path)
            # save annotation to "points"
            flag = self.AnnotateImage(img,imgOriginal,points)
            while flag:
                flag = self.AnnotateImage(img,imgOriginal,points)
            points_temp = points.copy()
            points = ""
            cv2.destroyAllWindows()
            if(len(points_temp)>0):
                point = points_temp[0]
                x = point[0]
                y = point[1]
                points += str(round(x / scale)) + " " + str(round(y / scale))
                for i in range(1, len(points_temp)):
                    point = points_temp[i]
                    x = point[0]
                    y = point[1]
                    points += "\n" + str(round(x / scale)) + " " + str(round(y / scale))
                #write file txt
                #print(points)
                print('Save file: ',fileTxt)
                f = open(fileTxt, 'w')
                f.write(points)
                f.close()
            else:
                print('Remove img: ',path)
                os.remove(path)
                self.totalImg -= 1
                self.currentImg -= 1
            #show the result
            #cv2.destroyAllWindows()
            #cv2.imshow("Result", img)
            #cv2.waitKey(0)
            
            
