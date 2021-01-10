from PreStage.Predict.predict import Predict
model_best = 'E:/CSRNet/model/0model_best.pth.tar'
dataFolder = 'E:/Demo/data'
resultFolder = 'E:/Demo/result'
densityFolder = 'E:/Demo/density'
dataOnlineFolder = 'E:/Demo/dataOnline'
CameraID = {}
CameraID['LeVanViet'] = "5ad0679598d8fc001102e274"
CameraID['PhamVanDong-Duong20'] = '5d8cd7fb766c880017188954'
predict = Predict(model_best,dataFolder,resultFolder,densityFolder)
#predict.Start()
predict.PredictCameraID(CameraID,dataOnlineFolder)
