# _*_ coding: utf-8 _*_

'''
用bypy库手动鉴权,文档地址：https://github.com/houtianze/bypy
'''

from baidu import ByPy
import os
import notice
import phash
import time

def monitor():
    start = time.time()
    # 统计目录下的png图片
    files = [f for f in os.listdir('.') if f.find('png') != -1]

    # 目录下图片数目是否为2
    if len(files) < 2:
        return
    bypy = ByPy()
    bypy.upload(files[-1])

    # 如果两幅图指纹不同, 发送邮件和短信，否则只保留最后一张图片
    if phash.imgs(files[-2], files[-1]):
        notice.send_notice()
    else:
        print('Pictures are same!')
        os.remove(files[:-1])
        print time.time()-start
        return

if __name__ == '__main__':
    monitor()
