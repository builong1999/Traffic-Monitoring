import os
from .model import CSRNet
import torch
from matplotlib import pyplot as plt
from os import listdir
from os.path import isfile, join
import numpy as np
import PIL.Image as Image
from torchvision import datasets, transforms
import h5py
from matplotlib import pyplot as plt
from matplotlib import cm as CM
import os
import urllib.request
from datetime import datetime
import time
import pytz
import re
import json
class Predict():
    def __init__(self,best_model,data,result,density):
        #Load best model
        model = CSRNet()
        self.model = model.cuda()
        checkpoint = torch.load(best_model)
        self.model.load_state_dict(checkpoint['state_dict'])
        print(checkpoint["epoch"])
        print(checkpoint["best_prec1"])
        if not os.path.exists(result):
                os.makedirs(result) 
                print("Directory '% s' created" % result) 
        if not os.path.exists(density):
                os.makedirs(density) 
                print("Directory '% s' created" % density) 
        self.data = data
        self.result = result
        self.density = density
        self.transform = transforms.Compose([transforms.ToTensor(),transforms.Normalize(mean=[0.485, 0.456, 0.406],std=[0.229, 0.224, 0.225]),])
    def PredictImg(self,image_path):
        fileName = os.path.basename(image_path).split('.')[0]
        saving_density_path =join(self.density, fileName + '.h5')
        img_raw = Image.open(image_path).convert('RGB')
        img = self.transform (img_raw).cuda()
        output = self.model(img.unsqueeze(0))  
        k = output.cpu().detach().numpy().squeeze()
        #save h5 file
        with h5py.File(saving_density_path, 'w') as hf:
            hf['density'] = k
        #fplot image and result
        fileTxt = join(self.data, fileName + '.txt')
        expect = ''
        if(os.path.isfile(fileTxt)):
            f = open(fileTxt, "r")  # Mo tep
            expect = len(f.readlines())
        actual = np.sum(output.cpu().detach().numpy().squeeze()) 
        fig = plt.figure(figsize=(12,5))
        if expect != '':
            fig.suptitle('Kết quả dự đoán: {val1:.4f}\n Kết quả chính xác: {val2:d}'.format(val1 = actual, val2 = expect), fontsize=16)
        else:
            fig.suptitle('Kết quả dự đoán: {val:.4f}\n'.format(val = actual), fontsize=16)
        fig.add_subplot(1, 2, 1)
        plt.title('Image raw: '+os.path.basename(image_path),fontsize=7)
        plt.imshow(img_raw)
        fig.add_subplot(1, 2, 2)
        plt.title('Density: '+os.path.basename(image_path).split('.')[0]+'.h5',fontsize=7)
        plt.imshow(k, cmap=CM.jet)
        resultPath = join(self.result,'Result_' + fileName+'.png')
        plt.savefig(resultPath)
        plt.close()
        print('save result: ' + os.path.realpath(resultPath))
    def PredictCameraID(self,CameraID,folderSave,n = 1, waitSeconds = 150):
        # setup time zone
        tz_VN = pytz.timezone('Asia/Ho_Chi_Minh')
        #create directory
        for CameraName in CameraID.keys():
            # Directory 
            directory = os.path.join(folderSave, CameraName)
            # Create the directory 
            if not os.path.exists(directory):
                os.makedirs(directory) 
                print("Directory '% s' created" % directory) 
        #save Image
        domain = "http://giaothong.hochiminhcity.gov.vn/render/ImageHandler.ashx?id="
        i = 0
        while(i<n):
            i += 1
            now = datetime.now(tz_VN) # current date and time
            date_time = now.strftime("%d%m%Y_%H%M%S")
            for CameraName in CameraID.keys():
                imageLink = domain+CameraID[CameraName]
                imagePath = os.path.join(folderSave,CameraName,CameraName+"_"+str(date_time)+ ".jpg") 
                #print('Dia diem: ' + CameraName)
                #print('Link image: ' + imageLink)
                #print('Created image: ' + imagePath)
                urllib.request.urlretrieve(imageLink,imagePath)
                #imShow(imagePath)
                print("save image: " + os.path.realpath(imagePath))
                self.PredictImg(imagePath)
            if i<n: time.sleep(waitSeconds) #delay
    def Start(self):
        files = [f for f in listdir(self.data) if '.jpg' in f]
        for file in files:
            self.PredictImg(image_path = join(self.data, file))
            
