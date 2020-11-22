import os
import glob
import cv2
#Change Folder, example: "D:/IT Majors/Thesis Outline/testLabel/"
direc = "C:/Users/BuiLong/source/CV/density/Demo Data/"
os.chdir(direc)
paths = [item for item in os.listdir() if ".jpg" in os.path.basename(item)]
print(paths)
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
Scale = 2

unlabeled = False #Browse only unlabeled images
#unlabeled = False #Browse through all images
for path in paths:
    #Open file
    print("Open: ", path)
    img = cv2.imread(path)
    img = cv2.resize(img, None, fx=Scale, fy=Scale)
    #read name file
    base = os.path.basename(path)
    fileTxt = os.path.splitext(base)[0] + ".txt"
    #set up
    points = []
    firstline = True
    if (unlabeled and os.path.isfile(fileTxt)):
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
        continue
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
