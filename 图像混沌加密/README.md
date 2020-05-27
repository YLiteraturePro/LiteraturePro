# :sunglasses: 图像混沌加密
* Python版本：3.6.4
* numpy模块
* pillow模块

## :grey_question: 原理简介
已知Logistic函数系统方程：

      X(k + 1) = u * X(k) * [1 - X(k)],k = 0,1,...,n

当满足以下条件时：

      0 < X(0) < 1
      3.57 < u ≤ 4

Logistic函数.工作于混沌状态，即通过系统方程产生的序列是无序不可预测的，具有较高的安全性。将其用于图像加密的方案有许多种，本人将实现其中-种较为简单的方案，即利用混沌序列对图像各点的像素值进行重排序，从而实现图像加密的效果。具体而言，即将混沌序列中的每个序列值与图像中的每个像素点一一对应。 加密时，像素点的位置由其对应的序列值在整个序列中的相对大小决定;解密时，只要生成相
同的混沌序列，然后根据混沌序列值将各像素点放回原位就好啦~

## :haircut:实现代码
* 仓库文件 chaos.py

```Python
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
```


*  -m 代表选择加密/解密，-k 代表密钥，-i 则代表待处理的图像。
#### 加密jpg

      python chaos.py -i test.jpg -k 3.57245
      
#### 解密jpg

      python chaos.py -i encryption.jpg -m dn -k 3.57245

#### 加密png

      python chaos.py -i test.png -k 3.57245

#### 解密png

      python chaos.py -i encryption.png -m dn -k 3.57245

## :eyes:实现效果

* 这是算法的一些结果(从左到右是输入，加密，输出)

* Png
<p align='center'>
  <img src='image/test.png' height='290' width='290'/>
  <img src='image/encryption.png' height='290' width='290'/>
  <img src='image/decryption.png' height='290' width='290'/>
</p>
* Jpg
<p align='center'>
  <img src='image/test.jpg' height='290' width='290'/>
  <img src='image/encryption.jpg' height='290' width='290'/>
  <img src='image/decryption.jpg' height='290' width='290'/>
</p>


## :exclamation:说明

* Jpg格式不建议使用，图像还原会失真
