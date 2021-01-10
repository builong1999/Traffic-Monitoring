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
class Predict():
    def __init__(self,best_model,data,result,density):
        #Load best model
        model = CSRNet()
        self.model = model.cuda()
        checkpoint = torch.load(best_model)
        self.model.load_state_dict(checkpoint['state_dict'])
        print(checkpoint["epoch"])
        print(checkpoint["best_prec1"])
        self.data = data
        self.result = result
        self.density = density
    def Start(self):
        files = [f for f in listdir(self.data) if '.jpg' in f]
        transform = transforms.Compose([transforms.ToTensor(),transforms.Normalize(mean=[0.485, 0.456, 0.406],std=[0.229, 0.224, 0.225]),])
        for file in files:
            fileName = file.split('.')[0]
            image_path = join(self.data, file)
            saving_density_path =join(self.density, fileName + '.h5')
            img_raw = Image.open(image_path).convert('RGB')
            img = transform(img_raw).cuda()
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
            fig.suptitle('Kết quả dự đoán: {val1:.4f}\n Kết quả chính xác: {val2:d}'.format(val1 = actual, val2 = expect), fontsize=16)
            fig.add_subplot(1, 2, 1)
            plt.title('Image raw: '+os.path.basename(image_path))
            plt.imshow(img_raw)
            fig.add_subplot(1, 2, 2)
            plt.title('Density: '+os.path.basename(image_path).split('.')[0]+'.h5')
            plt.imshow(k, cmap=CM.jet)
            resultPath = join(self.result,'Result_' + fileName+'.png')
            plt.savefig(resultPath)
            plt.close()
            print('saving... Result_'+fileName+'.png')
