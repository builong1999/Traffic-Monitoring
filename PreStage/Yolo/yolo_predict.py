import numpy as np
import cv2


def denoise(frame):
	frame = cv2.medianBlur(frame, 1)
	frame = cv2.GaussianBlur(frame,(5,5),0)
	return frame

def add_text(text, img, org = (50,50), color = (87,67,23), font = 6, fontScale = 1.5, thickness = 2, lineType = cv2.LINE_AA):
	org = (int(org[0]), int(org[1]))
	return cv2.putText(img, text, org, font, fontScale, color, thickness, lineType)

class YoloPredict():
    def __init__(self, class_path, weights_path, config_path, conf_threshold = 0.5, nms_threshold = 0.4, scale = 1):
        self.class_path = class_path
        self.weights_path = weights_path
        self.config_path = config_path
        self.conf_threshold = conf_threshold
        self.nms_threshold = nms_threshold
        self.scale = scale
        self.loadWeights()
        self.loadClass()
        
    def loadWeights(self):
        self.net = cv2.dnn.readNet(self.weights_path, self.config_path)

    def loadClass(self):
        with open(self.class_path, 'r') as f: 
	        self.classes = [line.strip() for line in f.readlines()]
        self.COLORS = np.random.uniform(0, 255, size = (3, len(self.classes)))

    def get_output_layers(self):
        layer_names = self.net.getLayerNames()
        output_layers = [layer_names[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]
        return output_layers

    def draw_prediction(self, img, class_id, confidence, x, y, x_plus_w, y_plus_h):
        label = self.classes[class_id]
        color = self.COLORS[class_id]

        cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), color, 2)
        img = add_text(label + ' : ' + str(round(float(confidence)*100)) + '%',img, (x - 10, y - 10),fontScale=0.5,thickness=1)

    def predict_indices_from_image(self, image):
        height, width = image.shape[:2]
        scale = 0.00392
        blob = cv2.dnn.blobFromImage(image, scale, (416, 416), (0, 0, 0), True, crop=False)
        self.net.setInput(blob)
        outs = self.net.forward(self.get_output_layers())

        class_ids = []
        confidences = []
        boxes = []

        # Thực hiện xác định bằng HOG và SVM
        
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    x = center_x - w / 2
                    y = center_y - h / 2
                    class_ids.append(class_id)
                    confidences.append(float(confidence))
                    boxes.append([x, y, w, h])

        return cv2.dnn.NMSBoxes(boxes, confidences, self.conf_threshold, self.nms_threshold), boxes, class_ids, confidences

    def draw_prediction_from_indices(self, image, indices, boxes, class_ids, confidences, image_background_removed = []):
        for i in indices:
            beta = 0.2
            i = i[0]
            x, y, w, h = boxes[i]
            index_x = x + int(w/2) - 7
            index_y = y + h
            # image = add_text('.',image, org = (index_x, index_y),color=(0,255,0))
            x_r, y_r, x_plus_w, y_plus_h =  round(x), round(y), round(x + w), round(y + h)
            # draw_prediction(image, class_ids[i], confidences[i], x_r, y_r, x_plus_w, y_plus_h)
            x = x - w*beta/2
            y = y - h*beta/2
            w = w + w*beta
            h = h + h*beta
            
            x_r, y_r, x_plus_w, y_plus_h =  round(x + w/6), round(y), round(x + 5*w/6), round(y + h)
            # draw_prediction(image, class_ids[i], confidences[i], x_r, y_r, x_plus_w, y_plus_h)
            # x_r, y_r, x_plus_w, y_plus_h =  round(x), round(y), round(x + w), round(y + h)
            

            if len(image_background_removed) != 0:
                x_o, y_o, w_o, h_o =  round(x + w/6), round(y), round(x + 5*w/6), round(y + h)
                obj = image_background_removed[y_o:h_o, x_o: w_o]
                
                precent = sum(sum(obj/255))/255
                if precent < 0.2:
                    continue
                sh = obj.shape[:2]

                for h in range(sh[0]):
                    for w in range(sh[1]):
                        if(abs(obj[h,w] - 255) < 5):
                            #index_x = x_o + w
                            index_y = y_o + h
                # print(f"sumobj: {round(precent,2)}",)
                # try:
                # 	cv2.imshow("obj",obj)
                # except:
                # 	print(sys.exc_info()[0])
                image = add_text('.',image, org = (index_x, index_y),color=(255,0,0))

            self.draw_prediction(image, class_ids[i], confidences[i], x_r, y_r, x_plus_w, y_plus_h)
        return image

    def predict_image(self, image_path):
        image = cv2.imread(image_path)
        height, width = image.shape[:2]
        image = cv2.resize(image, (int(width*self.scale), int(height*self.scale)))
        indices, boxes, class_ids, confidences = self.predict_indices_from_image(image)
        result = self.draw_prediction_from_indices(image, indices, boxes, class_ids, confidences) 
        cv2.imshow('result', result)
        cv2.waitKey(0)

if __name__ == "__main__":
    class_path = 'E:/Thesis/Yolo/yolov4-new.txt'
    weights_path = 'E:/Thesis/Yolo/yolov4-custom_last_final.weights'
    config_path = "E:/Thesis/Yolo/yolov4-new.cfg"
    conf_threshold = 0.5
    nms_threshold = 0.4

    yp = YoloPredict(class_path, weights_path, config_path, scale=0.5)
    yp.predict_image("E:/test.jpg")




