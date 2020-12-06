import Model.error_function as loss_function
from Model.model import CSRModel
from Model.load_data.load_dataset import LoadDataset

CSRNet = CSRModel()
loss = loss_function.MeanError

#1. Loading dataset
data_path = "C:/Users/BuiLong/source/CV/density/TrainData"
density_path = "C:/Users/BuiLong/source/CV/density/Density"
x_train,y_train,x_val,y_val = LoadDataset(data_path,density_path).get_dataset()
#2 Run freeze time
CSRNet.run_freeze_time(x_train,y_train,x_val,y_val,loss_function='mean_absolute_error', batch_size=2)

#3 Run unfreeze time
CSRNet.run_unfreeze_time(x_train,y_train,x_val,y_val,loss_function='mean_absolute_error')

#4 Show History
CSRNet.loss_during_time(35)