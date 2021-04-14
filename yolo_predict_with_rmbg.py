from PreStage.Yolo.yolo_predict import YoloPredict
from PreStage.Background.remove_background import BackgroundRemover
import cv2
##Define
video_path = "E:/test.mp4"
scale = 0.25

class_path = 'E:/Thesis/Yolo/yolov4-new.txt'
weights_path = 'E:/Thesis/Yolo/yolov4-custom_last_final.weights'
config_path = "E:/Thesis/Yolo/yolov4-new.cfg"
conf_threshold = 0.5
nms_threshold = 0.4

yp = YoloPredict(class_path, weights_path, config_path, conf_threshold, nms_threshold)
br = BackgroundRemover()

cam = cv2.VideoCapture(video_path)
width = cam.get(3)
height = cam.get(4)
_, firstFrame = cam.read()
firstFrame = cv2.resize(firstFrame,(int(width*scale), int(height*scale)))

while True:
    _, secondFrame = cam.read()
    secondFrame = cv2.resize(secondFrame,(int(width*scale), int(height*scale)))
    mask = br.initSubtraction(firstFrame, secondFrame)
    firstFrame = secondFrame.copy()
    cv2.imshow('mask', mask)
    indices, boxes, class_ids, confidences = yp.predict_indices_from_image(secondFrame)
    result = yp.draw_prediction_from_indices(secondFrame, indices, boxes, class_ids, confidences, mask)

    cv2.imshow('result', result)
    cv2.waitKey(1)
    
        
cam.release()
cv2.destroyAllWindows()