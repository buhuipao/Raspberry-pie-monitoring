# _*_ coding: utf-8 _*_

'''
演绎网上别人的脚本，加了些条件判断，满足基本图片相似判断
判断相同形状的图片采用精确匹配(根据形状进行切割获取高能区)，如是不同形状则采用模糊匹配(8*8)
'''

import cv2
import numpy as np
from compiler.ast import flatten
import sys


def p_hash(img, shape=True):
    '''shape参数用于比较两张图片, 默认为True'''
    # 加载并调整图片为高x宽灰度图片
    img = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
    h, w = (48, int(48*img.shape[1]/img.shape[0])) if shape else (48, 48)
    # 宽度必须为偶数，否则Dct变换会报错
    if w % 2 != 0:
        w = w - 1

    # 三个参数分别为源，图片的x&y(也就是宽&高), 缩小处理方法
    img = cv2.resize(img, (w, h), interpolation=cv2.INTER_CUBIC)

    # 创建二维列表
    vis0 = np.zeros((h, w), np.float32)
    vis0[:h, :w] = img

    # 二维Dct变换
    vis1 = cv2.dct(cv2.dct(vis0))

    # 利用离散余弦变换，截取左上角高能指纹区
    if w > h:
        # 高宽比, 保持较窄的为8
        vis1.resize(8, int(8*w/h))
    else:
        vis1.resize(int(8*h/w), 8)

    # 把二维list变成一维list
    img_list = flatten(vis1.tolist())

    # 计算均值
    avg = sum(img_list)/len(img_list)
    avg_list = ['0' if i < avg else '1' for i in img_list]

    # 得到16进制哈希值
    # print(''.join(['%x' % int(''.join(avg_list[x:x+4]), 2) for x in range(0, len(avg_list), 4)]))
    return avg_list


def diff(img1_list, img2_list):
    if len(img1_list) != len(img2_list):
        return 'diff'
    img1_list = map(int, img1_list)
    img2_list = map(int, img2_list)
    matV = np.mat([img1_list, img2_list])
    smstr = np.nonzero(matV[0]-matV[1])
    # 巨坑! 相同的库Mac和Linux的结果不太一样, 注释的是Mac下的汉明距离
    # return False if np.shape(smstr[0])[0] <= 5 else True
    return False if np.shape(smstr[0])[1] <= 5 else True


# 判断图片的形状是否相似, 即判断长宽比值
def same_shape(img1, img2):
    img1 = cv2.imread(img1, cv2.IMREAD_GRAYSCALE)
    shape1 = int(48*img1.shape[1]/img1.shape[0])
    img2 = cv2.imread(img2, cv2.IMREAD_GRAYSCALE)
    shape2 = int(48*img2.shape[1]/img2.shape[0])
    return True if shape1 == shape2 else False


def imgs(img1, img2):
    # 先判断图片的形状是否相似
    result = same_shape(img1, img2)
    img1_list = p_hash(img1, result)
    img2_list = p_hash(img2, result)
    # print(diff(img1_list, img2_list))
    return diff(img1_list, img2_list)

if __name__ == '__main__':
    imgs(sys.argv[1], sys.argv[2])
