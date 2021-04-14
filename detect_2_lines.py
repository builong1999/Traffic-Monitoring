import cv2
import numpy as np
import math

def find_length_2_points(p1,p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1] - p2[1])**2)

def sort_point_to_poly(points,w,h):
    list1 = []
    list2 = []
    for point in points:
        if point[0] < w/2:
            list1.append(point)
        else:
            list2.append(point)
    list1 = sorted(list1,key=lambda k:k[1], reverse=True)
    list2 = sorted(list2,key=lambda k:k[1])
    return list1 + list2

def find_intersect(line1, line2, w, h):
    a0, a1 = line1
    b0 ,b1 = line2
    xa1 = 0
    xa2 = w
    xb1 = 0
    xb2 = w
    pa1y = int(a1*xa1 + a0)
    if pa1y < 0:
        pa1y = 0
        xa1 = int(-a0/a1)
    pa2y = int(a1*xa2 + a0)
    if pa2y < 0:
        pa2y = 0
        xa2 = int(-a0/a1)
    pb1y = int(b1*xb1 + b0)
    if pb1y < 0:
        pb1y = 0
        xb1 = int(-b0/b1)
    pb2y = int(b1*xb2 + b0)
    if pb2y < 0:
        pb2y = 0
        xb2 = int(-b0/b1)
    if(xa1 > w or xa1 < 0 or xa2 > w or xa2 < 0 or pa1y > h or pa2y > h or pb1y > h or pb2y > h):
        return []
    return [0,h],[xb1, pb1y],[xb2, pb2y],[xa1, pa1y],[xa2, pa2y],[w,h], find_length_2_points([xa1, pa1y],[xb1, pb1y]) + find_length_2_points([xa2, pa2y],[xb2, pb2y])

def region_of_interest(img, vertices):
    mask = np.zeros_like(img)
    channel_count = img.shape[2]
    match_mask_color = (255,) * channel_count
    cv2.fillPoly(mask, vertices, match_mask_color)
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image

def points_to_line(points):
    Xtemp = []
    ytemp = []
    for point in points:
        Xtemp.append(point[0])
        ytemp.append(point[1])
    #Use Linear Regression
    X = np.array([Xtemp]).T
    y = np.array([ytemp]).T
    
    # Building Xbar 
    one = np.ones((X.shape[0], 1))
    Xbar = np.concatenate((one, X), axis = 1)
    # Calculating weights of the fitting line 
    A = np.dot(Xbar.T, Xbar)
    b = np.dot(Xbar.T, y)
    w = np.dot(np.linalg.pinv(A), b)
    w_0 = w[0][0]
    w_1 = w[1][0]
    return round(w_0, 5), round(w_1, 5)

cap = cv2.VideoCapture("E:/Thesis/Video/PVD-1.mp4")
width = cap.get(3)
height = cap.get(4)
height_resize = 720
width_resize = int(width*height_resize*1.0/height)
k = 1
lines_rm = {}
while True:
    _, frame = cap.read()
    #frame = cv2.resize(frame,(width_resize,height_resize))
    img = cv2.resize(frame, (width_resize, height_resize))
    if height > width:
        img = img[height_resize - width_resize:,:width_resize]
    #show_image("Original", img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # detect edges
    edges = cv2.Canny(gray, 150, 300)

    lines = cv2.HoughLinesP(
        edges,
        rho=1.0,
        theta=np.pi/180,
        threshold=20,
        minLineLength=30,
        maxLineGap=10        
    )

    # draw lines
    line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    line_color = [0, 255, 0]
    line_thickness = 2
    dot_color = [0, 255, 0]
    dot_size = 3
    points = []
    #line_img = cv2.bitwise_and(line_img, line_img, mask = mask)
    for line in lines:
        poly = []
        for x1, y1, x2, y2 in line:
            if math.sqrt((x1-x2)**2 + (y1-y2)**2) < 70:
                continue
            points.append([(x1,y1),(x2,y2),math.sqrt((x1-x2)**2 + (y1-y2)**2)])

    points = sorted(points,key=lambda kv: kv[2],reverse=True)
    for i in range(2):
        p1, p2, d = points[i]
        w0, w1 = points_to_line(points[i][0:2])
        cv2.line(line_img, p1, p2, line_color, line_thickness)
        if (w0,w1) not in lines_rm.keys():
            lines_rm[(w0,w1)] = 1
        else:
            lines_rm[(w0,w1)] += 1
    if k == 50: 
        break
    overlay = cv2.addWeighted(img, 0.8, line_img, 1.0, 0.0)
    k += 1

lines_rm = sorted(lines_rm.items(),key=lambda kv: kv[1], reverse=True)

l1 = lines_rm[0][0]
points = []
for i in range(1,len(lines_rm)):
    l2 = lines_rm[i][0]
    listfi = find_intersect(l1,l2,width_resize, height_resize)
    if len(listfi) > 0:
        points.append(listfi)
points = sorted(points,key=lambda kv: kv[len(points[0])-1], reverse=True)
mask = sort_point_to_poly(points[0][:len(points[0])-1],width_resize,height_resize)
while True:
    _, frame = cap.read()
    img = cv2.resize(frame, (width_resize, height_resize))
    if height > width:
        img = img[height_resize - width_resize:,:width_resize]
    cropped_image = region_of_interest(img, np.array([mask], np.int32),)
    cv2.imshow('crop',cropped_image)
    cv2.waitKey(1)
   