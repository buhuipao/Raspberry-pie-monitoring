# _*_ coding: utf-8 _*_

import socket
import time
import picamera
import pili
import os


def gen_url():
    mac = pili.Mac('your qiniu AccessKey', 'your qiniu SecretKey')
    hub = 'your qiniu live hub '
    key = 'your qiniu live hub-stream'
    publish = 'your qiniu publish url'
    rtmp = 'your qiniu rtmp play url'
    hls = 'your qiniu hls play url'
    publish_url = pili.rtmp_publish_url(publish, hub, key, mac, 3600)
    rtmp_url = pili.rtmp_play_url(rtmp, hub, key)
    print('rtmp player url: %s' % rtmp_url)
    hls_url = pili.hls_play_url(hls, hub, key)
    print('hls player url: %s' % hls_url)
    return publish_url


def Pi():
    camera = picamera.PiCamera()
    camera.resolution = (854, 480)
    camera.framerate = 36
    server_socket = socket.socket()
    server_socket.bind(('0.0.0.0', 8000))
    server_socket.listen(1)
    while 1:
        connection = server_socket.accept()[0].makefile('wb')
        print('Start living...')
        try:
            camera.start_recording(connection, format='h264')
            while 1:
                camera.wait_recording(5)
            camera.stop_recording()
        finally:
            connection.close()
            server_socket.close()


def main():
    pid = os.fork()
    if pid != 0:
        child = pid
        Pi()
    else:
        url = gen_url()
        time_title = "fontfile=/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf:x=w-tw:fontcolor=white:fontsize=30:text='%{localtime\:%X}'"
        cmd = 'ffmpeg -i tcp://127.0.0.1:8000 -vf vflip -r 36 -codec copy -threads 8 -preset ultrafast  -an -b:v 1000k -vcodec libx264 -s 854x480 -vf drawtext="' + time_title + '" -f flv "' + url + '"'
        print(cmd)
        time.sleep(1)
        os.system(cmd)
        os._exit(0)
    os.waitpid(child, 0)


if __name__ == '__main__':
    main()
