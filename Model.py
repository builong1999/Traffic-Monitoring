import Model.error_function as loss_function
from Model.model import CSRModel
from Model.load_data.load_dataset import LoadDataset

CSRNet = CSRModel()
loss = loss_function.MeanError

#1. Loading dataset
data_path = "C:\\Users\\BuiLong\\source\\CV\\density\\Data\\Data_exp"
density_path = "C:\\Users\\BuiLong\\source\\CV\\density\\Data\\Ground"
x_train,y_train,x_val,y_val = LoadDataset(data_path,density_path).get_dataset()

#2 Run freeze time
CSRNet.run_freeze_time(x_train,y_train,x_val,y_val,loss_function=loss)

#3 Run unfreeze time
CSRNet.run_unfreeze_time(x_train,y_train,x_val,y_val,loss_function=loss)

#4 Show History
CSRNet.loss_during_time()