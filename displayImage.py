import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
plt.style.use(astropy_mpl_style)

from astropy.io import fits
from astropy.utils.data import get_pkg_data_filename

image_file = get_pkg_data_filename('star_Light_Blue_45_secs_034.fits')

"""
Change image_file to file name of whichever file you'd like to generate 
an image for. Make sure this file is in same directory as the code. 
"""

fits.info(image_file)
image_data = fits.getdata(image_file, ext=0)
print(image_data.shape)
plt.figure()

"""
Run this code, note down the approximate location of the star in the image,
then uncomment lines 24 and 25 and adjust x and y limits to obtain 
a close-up of the star.
"""

#plt.xlim([2350, 2400])
#plt.ylim([1675, 1700])


plt.imshow(image_data, cmap='gray')
plt.colorbar()
plt.show()
