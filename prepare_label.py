from PreStage.Label.make_label import MakeLabel
import glob
import os
path = 'E:/PhamVanDong-Duong20(huongdiSanbay)'
make_label = MakeLabel(direc = path,unlabeled = True, scale = 1.5)
make_label.start()
#click mouse and enter is make label
#drag mouse and enter is delete label