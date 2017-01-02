# _*_ coding: utf-8 _*_

'''
用bypy库手动鉴权,文档地址：https://github.com/houtianze/bypy
'''
from baidu import ByPy
import os
import test as notice
import phash
import time


def monitor():
    start = time.time()
    # 统计目录下的png图片
    files = [f for f in os.listdir('.') if f.find('jepg') != -1]

    # 目录下图片数目是否为2
    if len(files) < 2:
        return
    bypy = ByPy()
    print(files[-1])
    bypy.upload(files[-1])

    # 如果两幅图指纹不同, 发送邮件和短信，否则只保留最后一张图片
    if phash.imgs(files[-2], files[-1]):
        notice.send_notice(files[-2:])
        print(time.time()-start)
    else:
        print('Pictures are same!')
        for img in files[:-1]:
            os.remove(img)
        print(time.time()-start)
        return

if __name__ == '__main__':
    monitor()
