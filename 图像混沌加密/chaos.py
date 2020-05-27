'''*************************************************
Copyright (C), 2018-2022,Literature Tech. Co., Ltd.
source:    None
Author:    Written by Mr.YangWenxuan
Version:   1.0
Date:      2020.05.20
Description:  
Others:   None
Function List:  main
History:  The first edition 2020.05.19
*************************************************'''
import numpy as np
from PIL import Image

'''
加密:
	-key: 密钥
	-imgpath: 待加密图像路径
	-start: 将生成的混沌序列，从第start个之后开始作为加密用序列
'''
def encryption(key, imgpath, start=500, x0=0.1):
	if key > 4 or key < 3.57:
		print('[Error]: Key must between <3.57-4>...')
		return None
	if x0 >= 1 or x0 <= 0:
		print('[Error]: x0 must between <0-1>...')
		return None
	img = Image.open(imgpath)
	img_en = Image.new(mode=img.mode, size=img.size)
	width, height = img.size
	chaos_seq = np.zeros(width * height)
	for _ in range(start):
		x = key * x0 * (1 - x0)
		x0 = x
	for i in range(width * height):
		x = key * x0 * (1 - x0)
		x0 = x
		chaos_seq[i] = x
	idxs_en = np.argsort(chaos_seq)
	i, j = 0, 0
	for idx in idxs_en:
		col = int(idx % width)
		row = int(idx // width)
		img_en.putpixel((i, j), img.getpixel((col, row)))
		i += 1
		if i >= width:
			j += 1
			i = 0
	img_en.save('encryption.%s' % imgpath.split('.')[-1], quality=100)


'''
解密:
	-key: 密钥
	-imgpath: 待解密图像路径
	-start: 将生成的混沌序列，从第start个之后开始作为解密用序列
'''
def decryption(key, imgpath, start=500, x0=0.1):
	if key > 4 or key < 3.57:
		print('[Error]: Key must between <3.57-4>...')
		return None
	if x0 >= 1 or x0 <= 0:
		print('[Error]: x0 must between <0-1>...')
		return None
	img = Image.open(imgpath)
	img_de = Image.new(img.mode, img.size)
	width, height = img.size
	chaos_seq = np.zeros(width * height)
	for _ in range(start):
		x = key * x0 * (1 - x0)
		x0 = x
	for i in range(width * height):
		x = key * x0 * (1 - x0)
		x0 = x
		chaos_seq[i] = x
	idxs_de = np.argsort(chaos_seq)
	i, j = 0, 0
	for idx in idxs_de:
		col = int(idx % width)
		row = int(idx // width)
		img_de.putpixel((col, row), img.getpixel((i, j)))
		i += 1
		if i >= width:
			j += 1
			i = 0
	img_de.save('decryption.%s' % imgpath.split('.')[-1], quality=100)



if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('-m', '--mode', help='<en> to encryption, <de> to decryption', default='en')
	parser.add_argument('-k', '--key', help='key for encryption or decryption.', default=3.58)
	parser.add_argument('-i', '--image', help='image to encryption or decryption.', default='test.jpg')
	args = parser.parse_args()
	if args.mode == 'en':
		encryption(key=float(args.key), imgpath=args.image)
	else:
		decryption(key=float(args.key), imgpath=args.image)