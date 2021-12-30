from skimage.feature.texture import greycomatrix, greycoprops
from skimage import data, io
from numpy import pi
import cv2
print('Hai')
path = 'static\disease_images\disease_1.png'

img = cv2.imread(path)
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ngcm = greycomatrix(img, [1], [0], 256, symmetric=False, normed=True)
# img = data.camera()

greycoprops(greycomatrix(img, distances=[1], angles=[0]), 'contrast')
# array([[34000139]], dtype=int64)

greycoprops(greycomatrix(img, distances=[1, 2], angles=[0]), 'contrast')

# array([[ 34000139],[109510654]], dtype=int64)

greycoprops(greycomatrix(
    img, distances=[1, 2], angles=[0, pi/4]), 'contrast')
# Out[43]: array([[ 34000139,  53796929],[109510654,  53796929]], dtype=int64)
print("hoi")
ss = greycoprops(greycomatrix(img, distances=[1],
                              angles=[0, pi/4, pi/2]), 'contrast')
print(ss)
# Out[44]: array([[34000139, 53796929, 20059013]], dtype=int64)
