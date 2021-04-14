import cv2
import numpy as np
from PreStage.Background.remove_background import BackgroundRemover
video_path = "E:/test.mp4"

br = BackgroundRemover(scale=0.25)
br.remove_background_video(video_path, show=True)
