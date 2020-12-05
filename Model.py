import Model.error_function as loss_function
from Model.model import CSRModel
from Model.load_data.load_dataset import LoadDataset

CSRNet = CSRModel()
loss = loss_function.MeanError

#1. Loading dataset
data_path = "C:\\Users\\BuiLong\\source\\CV\\density\\TrainData"
density_path = "C:\\Users\\BuiLong\\source\\CV\\density\\Density"
x_train,y_train,x_val,y_val = LoadDataset(data_path,density_path, image_num=50).get_dataset()
print(x_train.shape)
print(y_train.shape)
print(x_val.shape)
print(y_val.shape)
#2 Run freeze time
CSRNet.run_freeze_time(x_train,y_train,x_val,y_val,loss_function=loss)

#3 Run unfreeze time
CSRNet.run_unfreeze_time(x_train,y_train,x_val,y_val,loss_function=loss)

#4 Show History
CSRNet.loss_during_time(35)