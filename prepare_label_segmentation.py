from operator import truediv
from PreStage.Label.make_label_segmentation import MakeLabelSegmentation
import glob
import os
imgPath = 'E:/YoloV4/PVT3/ROIImage' #Recommended: ROI this directory in advance!
resultPath = 'E:/YoloV4/PVT3/Label'
make_label = MakeLabelSegmentation(src_path = imgPath, result_path = resultPath, use_labeled = True, scale = 1.2)
make_label.start()
#Left mouse button: select vehicle 
#SHIFT+left mouse button: select ROI
#CTRL+left mouse button: select Street
#'r'/SPACE: reset all         'w': change vision
#'p': prev image              'n': next image
#'s'/ENTER: save label        'q'/ESC: exit