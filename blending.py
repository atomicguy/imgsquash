'''
Pad equirect image from pano using PIL/Pillow.
'''

from PIL import Image, ImageOps, ImageFilter
from PIL.Image import BILINEAR
from math import sqrt, sin, cos, atan2
import dialogs
import photos

def blending(img):
	size = img.size
	w = size[0]
	h = size[1]
	newSize = [w, h * 2]
	blendImg = Image.new('RGB', newSize)

	topRowBox = (0,0,w,1)
	topRow = img.crop(topRowBox)
	for k in range(0,h):
		blendImg.paste(topRow, (0,k))

	bottomRowBox = (0,h-1,w,h)
	bottomRow = img.crop(bottomRowBox)
	for k in range(h,h*2):
		blendImg.paste(bottomRow, (0,k))

	blendImg = blendImg.filter(ImageFilter.MedianFilter(15))

	h2 = int(h/2)
	h3 = int(h/3)
	for k in range(h3,h):
		blendImg.paste(topRow, (0,k))
	for k in range(h+h2,h+h2+h3):
		blendImg.paste(bottomRow, (0,k))

	blendImg = blendImg.filter(ImageFilter.MedianFilter(9))

	blendImg.paste(img, (0, int(size[1]/2)))
	texture = blendImg.resize((4096,2048),BILINEAR)
	return texture

def main():
	i = dialogs.alert('Image', '', 'Demo Image', 'Select from Photos')
	if i == 1:
		img = Image.open('test:Lenna')
	else:
		img = photos.pick_image()
	blending(img).show()
	print('Tip: You can tap and hold the image to save it to your photo library.')

if __name__ == '__main__':
	main()
