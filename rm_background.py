import numpy as np
import cv2
import time
import os
import numpy as np
import glob
import sys

# #define
video_path = 'E:/output.avi'
class_path = 'E:/Thesis/Yolo/yolov4-new.txt'
weights_path = 'E:/Thesis/Yolo/yolov4-custom_last_final.weights'
config_path = "E:/Thesis/Yolo/yolov4-new.cfg"
conf_threshold = 0.5
nms_threshold = 0.4
alpha = 0.1
net = cv2.dnn.readNet(weights_path, config_path)
COLORS = np.random.uniform(0, 255, size = (3, 3))
classes = []
index_frame = 1
with open(class_path, 'r') as f: 
	classes = [line.strip() for line in f.readlines()]
#end define

def resize(img, size = None):
	if size == None:
		height, width = img.shape[:2]
		if width > height:
			return cv2.resize(img,(720,int(720*height/width)))
		else:
			return cv2.resize(img,(int(720*width/height), 720))
	return cv2.resize(img,size)

def add_text(text, img, org = (50,50), color = (87,67,23), font = 6, fontScale = 1.5, thickness = 2, lineType = cv2.LINE_AA):
	org = (int(org[0]), int(org[1]))
	return cv2.putText(img, text, org, font, fontScale, color, thickness, lineType)

def get_output_layers(net):
	layer_names = net.getLayerNames()
	output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
	return output_layers

def draw_prediction(img, class_id, confidence, x, y, x_plus_w, y_plus_h):
	label = classes[class_id]
	color = COLORS[class_id]

	cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), color, 2)
	img = add_text(label + ' : ' + str(round(float(confidence)*100)) + '%',img, (x - 10, y - 10),fontScale=0.5,thickness=1)

def predict_image(image):
	height, width = image.shape[:2]
	scale = 0.00392
	blob = cv2.dnn.blobFromImage(image, scale, (416, 416), (0, 0, 0), True, crop=False)
	net.setInput(blob)
	outs = net.forward(get_output_layers(net))

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

	return cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold), boxes, class_ids, confidences

def draw_prediction_from_indices(image, indices, boxes, class_ids, confidences, image_background_removed = []):
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
		else:
			image = add_text('.',image, org = (index_x, index_y),color=(0,0,255))
		draw_prediction(image, class_ids[i], confidences[i], x_r, y_r, x_plus_w, y_plus_h)

	return image

cam = cv2.VideoCapture(video_path)

# Any filter we need to apply to all frames should be put here
def denoise(frame):
	frame = cv2.medianBlur(frame, 1)
	frame = cv2.GaussianBlur(frame,(5,5),0)

	return frame

def initSubtraction(firstFrame, secondFrame):
	ret, frame = cam.read()
	frame = resize(frame)
	cv2.imshow('input', frame)
	# indices, boxes, class_ids, confidences = predict_image(frame)
	frame_yolo = secondFrame.copy()
	frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	firstFrame = denoise(cv2.cvtColor(firstFrame, cv2.COLOR_BGR2GRAY))
	secondFrame = denoise(cv2.cvtColor(secondFrame, cv2.COLOR_BGR2GRAY))
	if ret is True:
		finalFrame = secondFrame*alpha + firstFrame * (1 - alpha)
		foreGround = cv2.absdiff(finalFrame.astype(np.uint8), secondFrame)
		ret, mask = cv2.threshold(foreGround, 15, 255, cv2.THRESH_BINARY)
		# apply image dilation
		kernel = np.ones((5,5),np.uint8)
		mask = cv2.dilate(mask,kernel,iterations = 1)
		# cv2.imshow('mask_', mask)	
		# frame_yolo = draw_prediction_from_indices(frame_yolo, indices, boxes, class_ids, confidences, mask)
		# mask =  draw_prediction_from_indices(mask, indices, boxes, class_ids, confidences)
		# cv2.imshow("frame_yolo",frame_yolo)
		global index_frame
		# cv2.imwrite(f"E:/frames/frame{index_frame}.png",frame_yolo)
		index_frame += 1
		return mask
fps = 0
while (True):
	stime = time.time()
	ret, firstFrame = cam.read()
	if ret:
		firstFrame = resize(firstFrame)
		secondFrame = firstFrame
		try:
			# In this loop we can get each frame individually, to pass
			for i in range(2):
				if i == 0:
					firstRet, firstFrame = cam.read()
					firstFrame = resize(firstFrame)
				if i == 1:
					secondRet, secondFrame = cam.read()
					secondFrame = resize(secondFrame)
				else:
					mask = initSubtraction(firstFrame, secondFrame)
					fps = round(1/(time.time() - stime),2)
					mask = add_text(str(fps), mask)
					cv2.imshow('mask', mask)
					cv2.waitKey(1)
		except:
			print(sys.exc_info()[0])


cam.release()
cv2.destroyAllWindows()
