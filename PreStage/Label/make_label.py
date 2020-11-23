"""
Author: Duong Le
Github: https://github.com/lhduong1999
"""
import os
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
        print(self.paths)
    
    def AnnotateImage(self, Image):
        showCrosshair = False
        fromCenter = False
        r = cv2.selectROI("Click or Select Bounding Box to Annotate a Vehicle", Image, fromCenter, showCrosshair)
        x = int((int(r[0])+int(r[0] + r[2]))/2)
        y = int((int(r[1])+int(r[1] + r[3]))/2)
        if (x==0 & y==0):
            return False, [0, 0]
        for i in range(-2, 2):
            for j in range(-2, 2):
                img[y+i, x+j] = [0, 0, 255]
        return True, [x, y]

    def start(self):
        scale = self.scale
        unlabeled = self.unlabeled
        for path in self.paths:
            #Open file
            print("Open: ", path)
            img = cv2.imread(path)
            img = cv2.resize(img, None, fx=scale, fy=scale)
            base = os.path.basename(path)
            fileTxt = os.path.splitext(base)[0] + ".txt"
            points = []
            firstline = True
            if (unlabeled and os.path.isfile(fileTxt)):
                print(path, "has been labeled")
                continue
            if (os.path.isfile(fileTxt)):
                f = open(fileTxt, "r")
                points_temp = f.readlines()
                f.close()
                for i in points_temp:
                    point = i.replace("\n", "")
                    point = point.split(" ")
                    x = round(int(point[0])*scale)
                    y = round(int(point[1])*scale)
                    points.append([x, y])
                    for a in range(-2, 2):
                        for b in range(-2, 2):
                            img[y + a, x + b] = [0, 255, 0]
            flag, pointTemp = self.AnnotateImage(img)
            while flag:
                points.append(pointTemp)
                flag, pointTemp = self.AnnotateImage(img)
                continue
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
            cv2.destroyAllWindows()

            print("|| ",points, end="")
            f = open(fileTxt, 'w')
            f.write(points)
            f.close()
            print("Saving... ", fileTxt, "...Done!")
