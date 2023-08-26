## This part is for image segmentation(After use TransUNet)
import matplotlib.pyplot as plt
# ----------这个是新的分割函数，用来分割根据tansunet进行图片分割图片---------256*256大小的
import numpy as np
import cv2
from skimage.color import rgb2gray
import glob
from skimage.io import imread, imshow
import imageio
import skimage.morphology as sm
Img_Paths = glob.glob("before_split\\*.jpg")  # 需要分割图片的路径
Save_path = "./new_after_split"
split_window = 256
img_path = Img_Paths[0]
for m, img_path in enumerate(Img_Paths):
    try:
        img01 = imread(img_path)
        # plt.imshow(img01,'gray')
        selem = sm.disk(2)  # 生成结构元素
        img = img01.copy()
        # 二值化图片
        mean = np.mean(img)
        img[img < mean] = 0
        img[img >= mean] = 255
        # 开运算去干扰
        img = sm.opening(img, selem)
        row01, col01 = np.where(img != 0)
        top_position = np.min(row01)  # 人像的头部位置
        bottom_position = np.max(row01)  # 人像的脚底位置
        center_position = bottom_position
        # 从人像的脚底位置向上查找
        while center_position > int(top_position + (bottom_position - top_position) * 0.45):
            arr = img[center_position, :]
            # print(len(arr[arr == 255]))
            if len(arr[arr == 255]) >= 100:
                print("find")
                print(center_position)
                break
            center_position -= 1
        top_window = center_position - int(split_window / 2) - 20
        bottom_window = center_position + int(split_window / 2) - 20
        print("这个位置是多少？",top_window,bottom_window)
        # 这个是记录了这个图片的位置
        split_img = img01[top_window:bottom_window, :]
        imageio.imsave("{0}\\{1}".format(Save_path, img_path.split('\\')[-1]), split_img)
        print("第{}张图片保存成功".format(img_path.split('\\')[-1]))
    except Exception as ex:
        print("第{}张图片保存失败！！！！！！！！！！！！！！！！！".format(img_path.split('\\')[-1]))
        print("出现如下异常%s" % ex)
