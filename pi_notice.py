# _*_ coding: utf-8 _*_

'''
短信的发送采用了阿里的大于平台，而邮件发送采用了搜狐的sendcloud平台
不多说， 阿里大于平台的API有错误不好用，感觉很乱没人维护，sendcloud的API没啥缺点，但是邮件限制很不舒服
所以，之后的脚本准备采用极光推送的短信API，mailgun的邮件API(一个月限制发10,000, 绝对够了)
'''
import requests
import top
import re
import os


def send_mail(filelist):
    # 检查图片文件数目是否为2
    filelist = filelist[-2:] if len(filelist) > 2 else filelist
    if len(filelist) == 2:
        files = [("embeddedImage", (filelist[0], open(filelist[0], 'rb'), 'application/octet-stream')),
                ("embeddedImage", (filelist[1], open(filelist[1], 'rb'), 'application/octet-stream'))]
    else:
        print('文件数目不够')
        return
    html_tmp = '''<p  style="color:#525866;line-height: 28px;font-size: 14px;">
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;老铁啊，监测到有人闯入寝室, 以下图片为抓拍画面:
                </p>
                <p  style="color:#525866;line-height: 28px;font-size: 14px;">
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;实时监控链接：
                </p>
                <p  style="color:#525866;line-height: 28px;font-size: 14px;">
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;http://pili-live-hls.raspi-live.buhuipao.com/raspi/raspi_key.m3u8
                </p>
                <p  style="color:#525866;line-height: 28px;font-size: 14px;">
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;rtmp://pili-live-rtmp.raspi-live.buhuipao.co/raspi/raspi_key
                </p>''' + \
                '<p>第一张图:</p> <img src="cid:'+filelist[0]+'"/> <p>第二张图:</p> <img src="cid:'+filelist[1]+'"/>'

    url = "http://sendcloud.sohu.com/webapi/mail.send.json"
    params = {"api_user": "your sendcloud.net api_user",
            "api_key": "your sendcloud.net API key",
            "from": "raspi_notice@buhuipao.com",
            "fromname": "Raspi_notice",
            "to": "chenhua22@outlook.com;xiaoziqin17@163.com",
            "subject": "来自树莓派的报警",
            "resp_email_id": "true",
            "html": html_tmp,
            "embeddedCid": ';'.join(filelist)
            }

    r = requests.post(url, files=files, data=params)
    print(r.text)


def send_sms():
    url = 'gw.api.taobao.com'
    appkey = 'your appkey'
    secret = 'app secret'
    port = 80
    req = top.api.AlibabaAliqinFcSmsNumSendRequest(url, port)
    req.set_app_info(top.appinfo(appkey, secret))

    req.format = "json"
    req.extend = "123456"
    req.sms_type = "normal"
    req.sms_free_sign_name = "不会跑"
    req.rec_num = ','.join(your numbers_list)
    req.sms_template_code = "template of sms code"

    try:
        r = req.getResponse()
        print(r)
    except Exception as e:
        print(e)


def send_notice():
    pattern = re.compile(r'png')
    imgs = [f for f in os.listdir('.') if re.search(pattern, f.split('.')[-1])]
    send_sms()
    send_mail(imgs)

if __name__ == '__main__':
    send_notice()
