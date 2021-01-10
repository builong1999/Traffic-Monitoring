import numpy as np
import h5py
import os
from os import listdir
from os.path import isfile, join
import json
class caclGAME:
    def __init__(self,groundtruthPath,predictionPath):
        self.groundtruthPath = groundtruthPath
        self.predictionPath = predictionPath
        self.item = [item for item in os.listdir(groundtruthPath) if ".h5" in os.path.basename(item)]
    def Padding(self, arr):
        w, h = arr.shape
        new_shape = [w, h]
        if w%2 == 1:
            new_shape[0] += 1
        if h%2 == 1:
            new_shape[1] += 1
        new_array = np.zeros(new_shape)
        for i in range(arr.shape[0]):
            for j in range(arr.shape[1]):
                new_array[i][j] = arr[i][j]
        return new_array

    def GAME_recursive(self,pre, gth, level, currentLevel = 0):
        if currentLevel == level:
            return abs(np.sum(pre) - np.sum(gth))
        else:
            pre = self.Padding(pre)
            gth = self.Padding(gth)
            ws_pre, hs_pre = pre.shape[0]//2, pre.shape[1]//2
            ws_gth, hs_gth = gth.shape[0]//2, gth.shape[1]//2
            pre_val = [pre[0:ws_pre, 0:hs_pre],
                    pre[0:ws_pre, hs_pre:],
                    pre[ws_pre:, 0:hs_pre],
                    pre[ws_pre:, hs_pre:]]
            gth_val = [gth[0:ws_gth, 0:hs_gth],
                    gth[0:ws_gth, hs_gth:],
                    gth[ws_gth:, 0:hs_gth],
                    gth[ws_gth:, hs_gth:]]
            currentLevel += 1
            res = []
            for a in range(4):
                res.append(self.GAME_recursive(pre_val[a], gth_val[a], level, currentLevel))
            return sum(res)
    def Start(self):
        totalFile = len(self.item)
        print('Totalfile: {val:d}'.format(val = totalFile))
        mae, game1, game2, game3, game4 = 0,0,0,0,0
        for file in self.item:
            arrGT = np.array(h5py.File(join(self.groundtruthPath,file), "r")['density'])
            arrPre = np.array(h5py.File(join(self.predictionPath,file), "r")['density'])
            mae += self.GAME_recursive(arrPre,arrGT,0)
            game1 += self.GAME_recursive(arrPre,arrGT,1)
            game2 += self.GAME_recursive(arrPre,arrGT,2)
            game3 += self.GAME_recursive(arrPre,arrGT,3)
            game4 += self.GAME_recursive(arrPre,arrGT,4)
        print('GAME0 (MAE): {val:.4f} '
                    .format(val=mae/totalFile))
        print('GAME1: {val:.4f} '
                    .format(val=game1/totalFile))
        print('GAME2: {val:.4f} '
                    .format(val=game2/totalFile))
        print('GAME3: {val:.4f} '
                    .format(val=game3/totalFile))
        print('GAME4: {val:.4f} '
                    .format(val=game4/totalFile))
c = caclGAME('E:/CSRNet/groundtruth','E:/CSRNet/prediction')
c.Start()