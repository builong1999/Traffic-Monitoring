from PreStage.Label.make_label import MakeLabel
import glob
import os
path = 'E:/traffic/NutGiaoThuDuc'
make_label = MakeLabel(direc = path,unlabeled = False, scale = 1, mode = 1)
make_label.start()
#mode = 1 is create label
#mode = 2 is delete label
