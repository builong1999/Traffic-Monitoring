
import glob
import os
path = 'E:\\traffic\\NutGiaoThuDuc\\*.txt'
list_files = glob.glob(path)
tlst = []

for file in list_files:
    length = 0
    with open(file, 'r') as f:
        length = len(f.readlines())
        f.close()
    if length < 10:
        os.remove(file)
