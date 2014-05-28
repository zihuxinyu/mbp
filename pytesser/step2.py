#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#图像分割
import os, Image

j = 1
dir = "pic/"
for f in os.listdir(dir):
    if f.endswith(".gif"):
        img = Image.open(dir + f)
        for i in range(4):
            x = 16 + i * 15  #这里的数字参数需要自己
            y = 2  #根据验证码图片的像素进行
            img.crop((x, y, x + 7, y + 10)).save("pic/%d.gif" % j)  #适当的修改
            print "j=", j
            j += 1