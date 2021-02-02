import cv2
import numpy as np
import sys
import os
class MakeLabelSegmentation:
    def __init__(self,src_path='',result_path='',labeled = True):
        if not os.path.exists(result_path):
            os.makedirs(result_path)
            print('%s not exists, create '%result_path)
        self.left_mouse_down = False
        self.src_path = src_path
        self.result_path = result_path
        self.radius = 6
        self.max_radius = 50
        self.use_prev_mask = False
        self.cur_mouse = (0,0)
        self.labeled = labeled
        self.COLOR_ROI = (0,0,255) #red
        self.COLOR_STREET = (0,255,0) #green
        self.COLOR_VEHICLE = (255,0,0) #blue
        self.windownname = "Image Segmentation"
        cv2.namedWindow(self.windownname)
        cv2.setMouseCallback(self.windownname, self.on_mouse, self)
        cv2.createTrackbar('Brush size',self.windownname,self.radius,self.max_radius,self.nothing)
    def mask2color(self,mask):
        r,c = mask.shape[:2]
        color = np.zeros((r,c,3),np.uint8)
        color[np.where(mask==0)] = self.COLOR_ROI 
        color[np.where(mask==1)] = self.COLOR_STREET
        color[np.where(mask==2)] = self.COLOR_VEHICLE
        return color

    def color2mask(self,color):
        #print(color)
        r,c = color.shape[:2]
        mask = np.ones((r,c),np.uint8)
        mask[np.where((((color-self.COLOR_ROI<= (1,1,1))&((color-self.COLOR_ROI>= (0,0,0))))|(color <= (1,1,1))).all(axis=2))] = 0
        mask[np.where(((color-self.COLOR_STREET<= (1,1,1))&((color-self.COLOR_STREET>= (0,0,0)))).all(axis=2))] = 1
        mask[np.where(((color-self.COLOR_VEHICLE<= (1,1,1))&((color-self.COLOR_VEHICLE>= (0,0,0)))).all(axis=2))] = 2
        return mask
        
    def on_mouse(self,event,x,y,flags,param):
        param.mouse_cb(event,x,y,flags)

    def nothing(self,x):
        pass
    def mouse_cb(self,event,x,y,flags):
        self.cur_mouse = (x,y)
        if event == cv2.EVENT_LBUTTONDOWN:
            self.left_mouse_down = True
        elif event == cv2.EVENT_LBUTTONUP:
            self.left_mouse_down = False
        if self.left_mouse_down and self.mask.size>0 and self.img.size>0:
            if flags & cv2.EVENT_FLAG_SHIFTKEY:
                cv2.circle(self.img, (x,y), self.radius, self.COLOR_ROI, -1)
                cv2.circle(self.mask, (x,y), self.radius, 0, -1)
            elif flags & cv2.EVENT_FLAG_CTRLKEY:
                cv2.circle(self.img, (x,y), self.radius, self.COLOR_STREET, -1)
                cv2.circle(self.mask, (x,y), self.radius, 1, -1)
            elif flags:
                #to mau neu nhan chuot trai
                cv2.circle(self.img, (x,y), self.radius, self.COLOR_VEHICLE, -1)
                cv2.circle(self.mask, (x,y), self.radius, 2, -1)

    def __init_mask(self):
        self.mask[:] = 1
        #mask[:10,:] = cv2.GC_PR_BGD
    def process(self):
        # if os.path.exists(self.maskPath):
        #     self.mask = self.color2mask(cv2.imread(self.maskPath))
            #self.bgdModel = np.zeros((1,65),np.float64)
            #self.fgdModel = np.zeros((1,65),np.float64)
            #cv2.grabCut(self.img, self.mask, None, self.bgdModel, self.fgdModel, 1, cv2.GC_INIT_WITH_MASK)
        while True:
            self.radius = cv2.getTrackbarPos('Brush size',self.windownname)
            color = self.mask2color(self.mask)
            alpha = 0.5
            show_img = (self.img*alpha + color*(1-alpha)).astype('uint8')
            cv2.circle(show_img, self.cur_mouse, self.radius, (200,200,200), 2)
            cv2.imshow(self.windownname,show_img)
            cv2.imshow('Review',color)
            key = cv2.waitKey(100)
            if key == ord('q') or key == 27 or key==ord('s') or key==ord('p') or key==ord('n') or key == 10 or key == 13:
                break
            elif key == ord('r') or key == 32:
                print('reset!')
                cv2.putText(show_img, 'reset...', (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255),2)
                cv2.imshow(self.windownname,show_img)
                cv2.waitKey(1)
                # mask enum
                # GC_BGD    = 0,  
                # GC_FGD    = 1, 
                # GC_PR_BGD = 2,  
                # GC_PR_FGD = 3  
                self.__init_mask()
                self.img = cv2.imread(self.imgPath)

        return key
    def start(self):
        img_dir = self.src_path
        save_dir = self.result_path
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
            print('%s not exists, create '%save_dir)
        print("Left mouse button: select vehicle ")
        print("SHIFT+left mouse button: select ROI")
        print("SHIFT+left mouse button: select Street")
        print("'r'/SPACE: reset all")
        print("'p': prev image              'n': next image")
        print("'s'/ENTER: save label        'q'/ESC: exit")
        fimglist = sorted([x for x in os.listdir(img_dir) if '.png' in x or '.jpg' in x])
        i = 0
        while i<len(fimglist):
            fimg = fimglist[i]
            self.maskPath = os.path.join(save_dir,fimg)
            self.imgPath = os.path.join(img_dir,fimg)
            print('process %s'%fimg)
            self.img = cv2.imread(self.imgPath)
            if not os.path.isfile(self.maskPath):
                self.mask = self.color2mask(self.img)
            else: 
                i+=1
                continue
            key = self.process()
            if key == ord('s') or key == 10 or key == 13:
                saveimg = os.path.join(save_dir, fimg)
                cv2.imwrite(saveimg,self.mask2color(self.mask))
                print('save label %s.'%saveimg)
                i += 1
            elif key == ord('p') and i>0:
                i -= 1
            elif key == ord('n') or key == 32:
                i += 1
            elif key == ord('q') or key == 27:
                break
