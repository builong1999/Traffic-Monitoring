from PreStage.Gaussian.gaussian import GaussianParse as GP

image_path = 'C:/Users/BuiLong/source/CV/density/Data/Data_exp'
density_h5_path = 'C:/Users/BuiLong/source/CV/density/Data/Ground'
density_path = 'C:/Users/BuiLong/source/CV/density/Data/Ground_img'

Gau = GP(blur=0.05, count=True)
Gau.set_path(image_path,density_h5_path,density_path)
Gau.run()
