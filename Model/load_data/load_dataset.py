import numpy as np
import glob
import h5py
import cv2


class LoadDataset():
    def __init__(self,  real_img_path, density_path,
                        ratio = 0.8, image_num = True, image_extension = ".jpg" , log='logging.txt',
                        epoch_data = 1,
                        threads = 4):
        self.data_folder_path = real_img_path.rstrip('\\') + "\\"
        self.density_folder_path = density_path.rstrip('\\') + "\\"
        self.now_data = 0
        self.extension = image_extension
        data_path = self.__init_used_image(image_num, self.__get_dataset_path(image_extension))
        self.__splice_train_val(ratio, data_path)
        self.threads = threads
    
    def __get_dataset_path(self, image_extension):
        return np.array(glob.glob(self.data_folder_path+ "*"+ image_extension))

    def __init_used_image(self, image_num, data_path):
        if image_num is True:
            return data_path
        else:
            return data_path[:image_num]
    
    def __splice_train_val(self, ratio, data_path):
        length = len(data_path)
        splice_pivot = int(ratio*length)
        np.random.shuffle(data_path)
        self.train_data = data_path[:splice_pivot]
        self.val_data = data_path[splice_pivot:]
        # self.epoch = epoch_data*len(self.train_data)

    def preprocess_input(image,target):
        #crop image
        #crop target
        #resize target
        crop_size = (int(image.shape[0]/2),int(image.shape[1]/2))
        
        
        if random.randint(0,9)<= -1:            
                dx = int(random.randint(0,1)*image.shape[0]*1./2)
                dy = int(random.randint(0,1)*image.shape[1]*1./2)
        else:
                dx = int(random.random()*image.shape[0]*1./2)
                dy = int(random.random()*image.shape[1]*1./2)

        #print(crop_size , dx , dy)
        img = image[dx : crop_size[0]+dx , dy:crop_size[1]+dy]
        
        target_aug = target[dx:crop_size[0]+dx,dy:crop_size[1]+dy]
        #print(img.shape)

        return(img,target_aug)

    def get_dataset(self):
        size = (450,800)
        try:
        #Get Train data
            extension_length = len(self.extension)
            x_train,y_train,x_val,y_val = np.asarray([]),np.asarray([]),np.asarray([]),np.asarray([])
            count = 0
            temp_val, temp_test = [], []
            for image in self.train_data:
                count+=1
                # Read x train element
                t = cv2.resize(cv2.imread(image),size)
                tshape = t.shape
                temp_val.append(t)
                # Read y train element
                name = image.split('\\')[-1][:-extension_length]+".h5"
                gt_file = h5py.File(self.density_folder_path+name,'r')
                temp_test.append(cv2.resize(np.asarray(gt_file['density']), (int(tshape[1]/8),int(tshape[0]/8))))
                print("Loading ", count,"-",tshape," : ", image)
                
            x_train = np.array(temp_val)
            y_train = np.array(temp_test)

            temp_val = []
            temp_test = []

            for image in self.val_data:
                count+=1
                # Read x train element
                t = cv2.resize(cv2.imread(image),size)
                temp_val.append(t)
                tshape = t.shape
                # Read y train element
                name = image.split('\\')[-1][:-extension_length]+".h5"
                gt_file = h5py.File(self.density_folder_path+name,'r')
                temp_test.append(cv2.resize(np.asarray(gt_file['density']), (int(tshape[1]/8),int(tshape[0]/8))))
                print("Loading ", count,"-",tshape," : ", image)

            x_val = np.array(temp_val)
            y_val = np.array(temp_test)

            return x_train,y_train,x_val,y_val

        except FileNotFoundError as e:
            raise "File not found: " + es
    
    # def thread_get_dataset()
