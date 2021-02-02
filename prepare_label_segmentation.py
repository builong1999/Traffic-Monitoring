from operator import truediv
from PreStage.Label.make_label_segmentation import MakeLabelSegmentation
import glob
import os
imgPath = 'E:/test' #Recommended: ROI this directory in advance!
resultPath = 'E:/res_PhamVanDong-Duong20(huongdiThuDuc)'
make_label = MakeLabelSegmentation(src_path=imgPath,result_path=resultPath)
make_label.start()
#Left mouse button: select vehicle 
#SHIFT+left mouse button: select ROI
#CTRL+left mouse button: select Street
#'r'/SPACE: reset all         'w': change vision
#'p': prev image              'n': next image
#'s'/ENTER: save label        'q'/ESC: exit