"""
Author: Duong Le
Github: https://github.com/lhduong1999
"""
import os, inspect
import cv2

class MakeLabel:
    def __init__(self, direc, unlabeled = False, scale = 2, mode = 1):
        self.create_button()
        self.get_image_list(direc)
        self.unlabeled = unlabeled
        self.scale = scale
        self.mode = mode
        #Mode 1 is make point 
        #Mode 2 is delete point
        pass

    #create button delete and create label
    def create_button(self):
        os.chdir(os.path.join(os.getcwd(),os.path.dirname(os.path.relpath(inspect.getfile(self.__class__)))))
        if os.path.isfile('icon.png'):
            self.icon = cv2.imread('icon.png')
        else:
            self.icon = None

    def get_image_list(self, direc):
        os.chdir(direc)
        self.paths = [item for item in os.listdir() if ".jpg" in os.path.basename(item)]
        #print(self.paths)

    def AnnotateImage(self, img,imgOriginal, points):
        if self.icon is not None:
            x, y = self.icon.shape[0:2]
            for i in range(x-1):
                for j in range(y-1):
                    img[i,j] = self.icon[i,j]
        r = cv2.selectROI("Click or Select Bounding Box to Annotate a Vehicle", img=img, fromCenter=False, showCrosshair= False)
        x = int((int(r[0])+int(r[0] + r[2]))/2)
        y = int((int(r[1])+int(r[1] + r[3]))/2)
        if (x==0 & y==0):
            return False
        #add icon to image
        if self.icon is not None:
            b, a = self.icon.shape[0:2]
            print(x,y,a,b)
            if x<a/2 and y<b:
                self.mode = 1
                print('Mode: Create')
                return self.AnnotateImage(img,imgOriginal,points)
            if x<a and x>a/2 and y<b:
                self.mode = 2
                print('Mode: Delete')
                return self.AnnotateImage(img,imgOriginal,points)
        #mode 2 is delete label
        if self.mode == 2:
            x1 = int(r[0])
            x2 = int(r[0] + r[2])
            y1 = int(r[1])
            y2 = int(r[1] + r[3])
            for x in range(x1,x2):
                for y in range(y1,y2):
                    if [x,y] in points:
                        for i in range(-2, 2):
                            for j in range(-2, 2):
                                img[y+i, x+j] = imgOriginal[y+i,x+j]
                        points.remove([x, y])
            #Get centroid
        #mode 1 is add label
        if self.mode == 1:
            for i in range(-2, 2):
                            for j in range(-2, 2):
                                img[y+i, x+j] = [0,0,255]
            points.append([x, y])
        return True

    #start make label
    def start(self):
        scale = self.scale
        unlabeled = self.unlabeled
        for path in self.paths:
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
            if (unlabeled and os.path.isfile(fileTxt) and self.mode != 2):
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
            # save annotation to "points"
            flag = self.AnnotateImage(img,imgOriginal,points)
            while flag:
                flag = self.AnnotateImage(img,imgOriginal,points)
            points_temp = points.copy()
            points = ""
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
            #show the result
            #cv2.destroyAllWindows()
            #cv2.imshow("Result", img)
            #cv2.waitKey(0)
            cv2.destroyAllWindows()
            #write file txt
            #print(points)
            f = open(fileTxt, 'w')
            f.write(points)
            f.close()
