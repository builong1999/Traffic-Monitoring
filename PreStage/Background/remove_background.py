import numpy as np
import cv2

def denoise(frame):
        frame = cv2.medianBlur(frame, 1)
        frame = cv2.GaussianBlur(frame,(5,5),0)
        return frame

class BackgroundRemover():
    def __init__(self, alpha = 0.01, scale = 1, show = False):
        self.alpha = alpha
        self.show = show
        self.scale = scale
        
    def initSubtraction(self, firstFrame, secondFrame):
        # ret, frame = self.cam.read()
        # frame = resize(frame)
        # cv2.imshow('input', frame)
        # indices, boxes, class_ids, confidences = predict_image(frame)
        # frame_yolo = secondFrame.copy()
        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        firstFrame = denoise(cv2.cvtColor(firstFrame, cv2.COLOR_BGR2GRAY))
        secondFrame = denoise(cv2.cvtColor(secondFrame, cv2.COLOR_BGR2GRAY))
        finalFrame = secondFrame*self.alpha + firstFrame * (1 - self.alpha)
        foreGround = cv2.absdiff(finalFrame.astype(np.uint8), secondFrame)
        ret, mask = cv2.threshold(foreGround, 15, 255, cv2.THRESH_BINARY)
        # apply image dilation
        kernel = np.ones((5,5),np.uint8)
        mask = cv2.dilate(mask, kernel, iterations = 1)
        # cv2.imshow('mask_', mask)	
        # frame_yolo = draw_prediction_from_indices(frame_yolo, indices, boxes, class_ids, confidences, mask)
        # mask =  draw_prediction_from_indices(mask, indices, boxes, class_ids, confidences)
        # cv2.imshow("frame_yolo",frame_yolo)
        # global index_frame
        # cv2.imwrite(f"E:/frames/frame{index_frame}.png",frame_yolo)
        # index_frame += 1
        return mask

    def remove_background_video(self, video_path):
        cam = cv2.VideoCapture(video_path)
        width = cam.get(3)
        height = cam.get(4)
        _, firstFrame = cam.read()
        firstFrame = cv2.resize(firstFrame,(int(width*self.scale), int(height*self.scale)))

        while True:
            _, secondFrame = cam.read()
            secondFrame = cv2.resize(secondFrame,(int(width*self.scale), int(height*self.scale)))
            mask = self.initSubtraction(firstFrame, secondFrame)
            if self.show:
                cv2.imshow('frame', secondFrame)
                cv2.imshow('mask', mask)
                cv2.waitKey(1)
            firstFrame = secondFrame
               
        cam.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    br = BackgroundRemover(show=True, scale = 0.5)
    br.remove_background_video("E:/test_focus.mp4")



