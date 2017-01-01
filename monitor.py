# _*_ coding: utf-8 _*_

'''
用bypy库手动鉴权,文档地址：https://github.com/houtianze/bypy
'''

from baidu import ByPy
import os
import phash
import notice
import time

def monitor():
    start = time.time()
    # 统计目录下的png图片
    files = [f for f in os.listdir('.') if f.find('png') != -1]

    # 目录下图片数目是否为2
    if len(files) < 2:
        return
    bypy = ByPy()
    bypy.upload(files[1])

    # 如果两幅图没有什么不同, 删除第一幅图
    if not phash.imgs(files[0], files[1]):
        print('Pictures are same!')
        os.remove(files[0])
        print time.time()-start
        return
    notice.send_notice()

if __name__ == '__main__':
    monitor()
