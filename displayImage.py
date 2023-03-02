import matplotlib.pyplot as plt 
  
from astropy.visualization import astropy_mpl_style 
  
plt.style.use(astropy_mpl_style) 
from astropy.io import fits 
from astropy.utils.data import get_pkg_data_filename 
  
image_file = get_pkg_data_filename('star_Light_Blue_30_secs_001.fits') 

#Change image_file to file name of whichever file you'd like to generate an image for 
#Make sure this file is in same directory as the code. If it isn't, add the full pathname.


fits.info(image_file) 
image_data = fits.getdata(image_file, ext=0) 
print(image_data.shape) 
plt.figure() 
plt.xlim([2200, 2400]) 
plt.ylim([1600, 1800]) 
plt.imshow(image_data, cmap='gray') 
plt.colorbar() 
