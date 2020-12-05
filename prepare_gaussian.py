from PreStage.Gaussian.gaussian import GaussianParse as GP

image_path = 'C:\\Users\\BuiLong\\source\\CV\\density\\TrainData'
density_h5_path = 'C:\\Users\\BuiLong\\source\\CV\\density\\Density'
density_path = 'C:\\Users\\BuiLong\\source\\CV\\density\\Density_Img'

Gau = GP(is_sample_img=False, blur=0.05, count=True)
Gau.set_path(image_path,density_h5_path,density_path)
Gau.run()
