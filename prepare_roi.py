from os import replace
from PreStage.ROI.make_roi import selectROI
path = 'E:/YoloV4/PVT3'
selROI = selectROI(direc = path, replaceImg = False, scale = 1, ROIColor = (0,0,0)) 
#replace img with ROI if relapceImg = True else create folder RoiImage and save image with ROI
#selROI.createROI() #create new ROI img
selROI.applyROI() 