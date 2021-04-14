from PreStage.Yolo.yolo_predict import YoloPredict

class_path = 'E:/Thesis/Yolo/yolov4-new.txt'
weights_path = 'E:/Thesis/Yolo/yolov4-custom_last_final.weights'
config_path = "E:/Thesis/Yolo/yolov4-new.cfg"
conf_threshold = 0.5
nms_threshold = 0.4

yp = YoloPredict(class_path, weights_path, config_path, conf_threshold, nms_threshold, scale=0.75)
yp.predict_image("E:/test.jpg")
