import os
import cv2
Scale = 1.5
unlabeled = False #Browse only unlabeled images
direc = os.getcwd()   
os.chdir(direc)
paths = [item for item in os.listdir() if ".jpg" in os.path.basename(item)]
# labels = [item for item in os.listdir() if ".txt" in os.path.basename(item)]
# for label in labels:
#     name = os.path.splitext(label)[0]
#     print(label)
#     print(name)
#     image = name + '.jpg'
#     if image not in images:
#         os.remove(label)
#     print('remeve ' + label)
def AnnotateImage(img, imgOriginal, points,label = False):
    # Select ROI
    r = cv2.selectROI("Click or Select Bounding Box to Annotate a Vehicle", img, fromCenter=False, showCrosshair=False)
    x = int((int(r[0])+int(r[0] + r[2]))/2)
    y = int((int(r[1])+int(r[1] + r[3]))/2)
    if (x==0 & y==0):
        return False
    if not label:
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
    if label:
        points.append([x, y])
    return True
#unlabeled = False #Browse through all images
labeled = 'labeled.txt'
pathslabeled = []
if os.path.exists(labeled):
    f = open('labeled.txt', 'r')
    pathslabeled = f.readlines()
    f.close()
pathslabeled = [item.split('\n')[0] for item in pathslabeled]
#print(pathslabeled)
for path in paths:
    #print(path)
    if path in pathslabeled:
        continue
    #Open file
    print("Open: ", path)
    img = cv2.imread(path)
    img = cv2.resize(img, None, fx=Scale, fy=Scale)
    imgOriginal = img.copy()
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
    flag = AnnotateImage(img,imgOriginal,points)
    while flag:
        flag = AnnotateImage(img,imgOriginal,points)
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
    f = open('labeled.txt', 'a+')
    f.write(path + '\n')
    f.close()



