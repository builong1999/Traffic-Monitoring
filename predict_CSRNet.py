from PreStage.Predict.predict import Predict
model_best = 'E:/CSRNet/model/0model_best.pth.tar'
dataFolder = 'E:/Demo/PhanDangLuu-PhanXichLong'
resultFolder = 'E:/Demo/resultPhanDangLuu-PhanXichLong'
densityFolder = 'E:/Demo/densityPhanDangLuu-PhanXichLong'
dataOnlineFolder = 'E:/Demo/dataOnline'
CameraID = {}
CameraID['PhamVanDong-Duong20'] = '5d8cd7fb766c880017188954'
predict = Predict(model_best,dataFolder,resultFolder,densityFolder)
#predict.Start()
predict.PredictCameraID(CameraID,dataOnlineFolder)
