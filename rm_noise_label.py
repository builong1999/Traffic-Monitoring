
import glob
import os
path = 'C:\\Users\\BuiLong\\source\\CV\\density\\TrainData\\*.txt'
list_files = glob.glob(path)
tlst = []

for file in list_files:
    length = 0
    with open(file, 'r') as f:
        length = len(f.readlines())
        f.close()
    if length < 5:
        os.remove(file)
        os.remove(file.replace('.txt','.jpg'))
