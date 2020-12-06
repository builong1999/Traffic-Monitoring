"""
Author: Long Bui
Github: https://github.com/builong1999
"""
import h5py
import scipy.io as io
import PIL as Image
import numpy as np
import os
from matplotlib import pyplot as plt
from scipy.ndimage.filters import gaussian_filter 
import scipy
from scipy import spatial
from matplotlib import cm as CM
from os import walk
import time

class GaussianParse():
    def __init__(self, is_sample_img = True, is_create_tree = True,count = False,blur=0.1, dpi=300):
        self.sample_img = is_sample_img
        self.create_folder_tree = is_create_tree
        self.blur_constaint = blur
        self.dpi_constaint = dpi
        self.is_count = count
        self.folder_tree = []


    def set_path(self, image_path, density_h5_path, density_img_sample_path = ""):
        self.image_path = image_path
        self.density_h5_path = density_h5_path
        self.density_img_path = density_img_sample_path
        self.list_image()
        self.make_dictionary(density_h5_path)
        self.make_dictionary(density_img_sample_path)

    def list_image(self):
        if self.image_path[-1] != '/':
            self.image_path += '/'
        f = []
        for root,direct,files in os.walk(self.image_path):
            for file in files:
                if file == "desktop.ini": continue
                if file[-3:] not in ['png','jpg']: continue
                if root[-1] != '/':
                    root +="/"
                f.append(root+file)
            if self.create_folder_tree:
                t = root[len(self.image_path):]
                if len(t) > 0:
                    self.folder_tree.append(t)
        self.list_image_paths = f

    def gaussian_filter_density(self, gt):
        blur_ = self.blur_constaint
        density = np.zeros(gt.shape, dtype=np.float32)
        gt_count = np.count_nonzero(gt)
        if gt_count == 0:
            return density
        pts = np.array(list(zip(np.nonzero(gt)[1].ravel(), np.nonzero(gt)[0].ravel())))
        leafsize = 2048
        tree = spatial.KDTree(pts.copy(), leafsize=leafsize)
        distances, locations = tree.query(pts, k=4)
        for i, pt in enumerate(pts):
            pt2d = np.zeros(gt.shape, dtype=np.float32)
            pt2d[pt[1],pt[0]] = 1.
            if gt_count > 1:
                sigma = (distances[i][1]+distances[i][2]+distances[i][3])*blur_
            else:
                sigma = np.average(np.array(gt.shape))/2./2. #case: 1 point
            density += scipy.ndimage.filters.gaussian_filter(pt2d, sigma, mode='constant')
        return density

    def make_dictionary(self,root_path):
        if root_path[-1] != '/':
            root_path += '/'
        if self.create_folder_tree:
            for folder in self.folder_tree:
                if not os.path.exists(root_path+folder):
                    os.makedirs( root_path + folder)

    def find_string_first_different(self, s1, s2):
        len1 = len(s1)
        len2 = len(s2)
        length = len1 if len1 < len2 else len2
        for index in range(len(length)):
            if s1[index] != s2[index]:
                break;
        return index


    def run(self):
        
        image_path_length = len(self.image_path)
        try:
            index = 0
            stime = time.time()
            for img_path in self.list_image_paths:
                index +=1
                count = 0
                #Log to user
                print(index, ": (", img_path, end="),(")
                image_path = img_path[:-3]
                point_lists = []
                with open(image_path+"txt",'r') as f:
                    point_lists = f.readlines()
                    f.close()
                img= plt.imread(img_path)
                k = np.zeros((img.shape[0],img.shape[1]))
                for i in range(0,len(point_lists)):
                    data = point_lists[i].rstrip('\n').split(' ')
                    if int(data[1])<img.shape[0] and int(data[0])<img.shape[1]:
                        k[int(data[1]),int(data[0])]=1
                        count+=1
                k = self.gaussian_filter_density(k)
                file_extend = image_path[image_path_length:]
                h5_path = self.density_h5_path + "/" + file_extend
                
                with h5py.File(h5_path+"h5", 'w') as hf:
                        hf['density'] = k
                if self.sample_img:
                    sample_path  = self.density_img_path+ "/" + file_extend
                    plt.figure(dpi=300)
                    plt.axis('off')
                    plt.margins(0, 0)
                    plt.imshow(k, cmap=CM.jet)
                    plt.savefig(sample_path, dpi=self.dpi_constaint, bbox_inches='tight', pad_inches=0)


                if self.is_count:
                    print(count,">",round(k.sum(),3),"),(", end="")
                print( round((time.time() - stime),3),"s)")
                stime = time.time()

                

        except FileNotFoundError as error:
            error = str(error)
            raise FileNotFoundError("Error, no density labeled found for: "+ error[38:])