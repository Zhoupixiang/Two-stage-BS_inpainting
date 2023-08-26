## This is the final fix to restore the 256*256 size image to 256*1024 size image
import cv2
import numpy as np
import matplotlib.pyplot as plt
import glob
from PIL import Image
import imageio

Mask_Paths = glob.glob("")  # 1024*256的Mask的路径

data_Paths = glob.glob("")  # 原图片的路径

recovery_Paths = glob.glob("")  # 通过网络去掉的遮挡的图片路径，256*256*3

Save_path = ""  # 保存路径
# print(Mask_Paths)
# print(data_Paths)
# print(recovery_Paths)
# 单张图片进行测试
# Mask_Paths = cv2.imread('')
# data_Paths = cv2.imread("")
# recovery_Paths = cv2.imread("")
# Save_path = ""  # 保存路径
for i, masl_path in enumerate(Mask_Paths):
    # 原图
    img01 = plt.imread(r'{}'.format(data_Paths[i]))
    img = img01.copy()
    # 定义切割窗口的大小
    Windows_high = 256
    Windows_width = img.shape[1]
    # Mask
    img_mask = plt.imread(masl_path)
    row01, col01 = np.where(img_mask == 1)
    high = np.max(row01) - np.min(row01) + 1
    ex_top_high = int((Windows_high - high) / 2)
    ex_bottom_high = ex_top_high
    if ((Windows_high - high) % 2 != 0):
        ex_bottom_high += 1
    # 找到切割的位置
    top_posiotion = np.min(row01) - ex_top_high
    bottom_posiotion = np.max(row01) + ex_bottom_high
    split_mask = img_mask.copy()
    # 将mask函数0,1化
    split_mask[top_posiotion:bottom_posiotion + 1, :] = 0
    split_mask[:top_posiotion, :] = 1
    split_mask[bottom_posiotion + 1:, :] = 1
    # 将mask改为三维，与img相乘，消除原来积液部分，大小为256*256
    split_mask = split_mask.reshape(1024, 256, 1)
    blask_img = split_mask * img
    # 读取去掉积液遮挡的图片，256*256*3
    finish_img = plt.imread(r'{}'.format(recovery_Paths[i]))
    # 定义跟原图大小的模板
    zero_np = np.zeros((1024, 256, 3))
    zero_np = zero_np.astype(int)
    # 将去掉积液的图片加入到相应位置
    if(finish_img.max()<=1):
        zero_np[top_posiotion:bottom_posiotion + 1, :] = finish_img * 255
    else:
        zero_np[top_posiotion:bottom_posiotion + 1, :] = finish_img

    # 将1024*256*3大小的消除的图片  与 1024*256*3大小的只有部分的图片相加

    if(blask_img.max()<=1):
        blask_img = blask_img * 255

    blask_img = blask_img.astype('int32')
    # print(zero_np.max())
    # print(blask_img.max())
    save_img = zero_np + blask_img
    # print(zero_np)
    # plt.imshow(save_img)
    # print(np.max(blask_img[0:top_posiotion, :]))
    imageio.imsave('{0}split{1:02d}.jpg'.format(Save_path,i),save_img)
    print("第{}张图片保存成功".format(i))
    # break

