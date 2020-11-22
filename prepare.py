from Data/PreStage/Gaussian/gaussian.py import Gaussian

image_path = 'C:/Users/BuiLong/source/CV/density/Data/Data_exp'
density_h5_path = 'C:/Users/BuiLong/source/CV/density/Data/Ground'
density_path = 'C:/Users/BuiLong/source/CV/density/Data/Ground_img'

Gau = GaussianParse()
Gau.set_path(image_path,density_h5_path,density_path)
Gau.run()