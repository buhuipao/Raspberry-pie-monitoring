# _*_ coding: utf-8 _*_

'''
以树莓派为服务端，把H.264编码视频流放到8000tcp端口, 推流到七牛的pili平台，具体七牛的pili平台设置见官方文档
利用七牛的pili库，生成推流地址，fork出子进程，python调用shell利用之前编译好的FFMPEG连接8000端口,

ffmpeg的编译参考官网: https://trac.ffmpeg.org/wiki/CompilationGuide/Ubuntu
七牛的pili推流文档：https://github.com/pili-engineering/pili-sdk-python
树莓派摄像头的python库文档：http://picamera.readthedocs.io/en/release-1.12/ 及GitHub: https://github.com/waveform80/picamera
'''

import socket
import time
import picamera
import pili
import os
import sys
from monitor import run as monitoring
import multiprocessing


def gen_url():
    mac = pili.Mac('illyLZP9RlWGikwwITutZvqqZTz73B8kTceDJ1gG', 'Qi3iL46RypaqivLD0_D7zRkijgD1jQEPdstMNh2w')
    hub = 'raspi'
    key = 'raspi_key'
    publish = 'pili-publish.raspi-live.buhuipao.com'
    rtmp = 'pili-live-rtmp.raspi-live.buhuipao.com'
    hls = 'pili-live-hls.raspi-live.buhuipao.com'
    publish_url = pili.rtmp_publish_url(publish, hub, key, mac, 3600)
    rtmp_url = pili.rtmp_play_url(rtmp, hub, key)
    print('rtmp player url: %s' % rtmp_url)
    hls_url = pili.hls_play_url(hls, hub, key)
    print('hls player url: %s' % hls_url)
    return publish_url


def recoding():
    camera = picamera.PiCamera()
    camera.resolution = (860, 480)
    camera.framerate = 36
    server_socket = socket.socket()
    server_socket.bind(('0.0.0.0', 8000))
    server_socket.listen(5)
    # server_socket.accept()[0] 是返回的新的套结字对象, server_socket.accept()[1]是连接的客户端地址
    connection = server_socket.accept()[0].makefile('wb')
    try:
        camera.start_recording(connection, format='h264')
        while 1:
            camera.wait_recording(10)
            camera.capture(time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime())+'.jpeg', use_video_port=True)
        camera.stop_recording()
    finally:
        connection.close()
        server_socket.close()


def pushing():
    url = gen_url()
    time_title = "fontfile=/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf:x=w-tw:fontcolor=white:fontsize=30:text='%{localtime\:%X}'"
    cmd = 'ffmpeg -i tcp://127.0.0.1:8000 -vf vflip -r 36 -codec copy -threads 8 -preset ultrafast  -an -b:v 1000k -vcodec libx264 -s 860x480 -vf drawtext="' + time_title + '" -f flv "' + url + '"'
    '''
    while True:
        try:
    	    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    	    s.connect((ip,int(port)))
    	    s.shutdown(2)
	    break
	except:
	    pass
    '''
    time.sleep(1)
    try:
        os.system(cmd)
    except Exception as e:
	print('Push living stream faild, error is %s' % e)


def main():
    worker_1 = multiprocessing.Process(target=recoding, args=())
    worker_2 = multiprocessing.Process(target=pushing, args=())
    worker_3 = multiprocessing.Process(target=monitoring, args=())
    worker_1.start()
    worker_2.start()
    worker_3.start()
    worker_1.join()
    worker_2.join()
    worker_3.join()

if __name__ == '__main__':
    main()
