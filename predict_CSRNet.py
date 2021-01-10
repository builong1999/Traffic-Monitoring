from PreStage.Predict.predict import Predict
model_best = 'Data/0model_best.pth.tar'
dataFolder = 'E:/Demo/data'
resultFolder = 'E:/Demo/result'
densityFolder = 'E:/Demo/prediction'
#dataOnlineFolder = 'E:/CSRNet/dataOnline'
# CameraID = {}
# CameraID['LeVanViet'] = "5ad0679598d8fc001102e274"
predict = Predict(model_best,dataFolder,resultFolder,densityFolder)
predict.Start()
#predict.PredictFromCameraID(CameraID,dataOnlineFolder)
