# _*_ coding: utf-8 _*_

'''
短信的发送采用了阿里的大于平台，mailgun的邮件API,  语音提醒还没弄好
阿里大于平台的API有错误不好用，感觉很乱没人维护
'''

import requests
import top

url = 'gw.api.taobao.com'
port = 80
appkey = 'xxxxxxxx'
secret = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'


def send_mail(imglist):
    '''
    imglist的长度应该为2
    '''
    with open('mail.html', 'r') as f:
        html_tmp = f.read().replace('IMG1', imglist[0]).replace('IMG2', imglist[1])
    url = "https://api.mailgun.net/v3/mail.buhuipao.com/messages"
    auth = ("api", "key-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    imgs = [("inline", open(imglist[0])), ("inline", open(imglist[1]))]
    payload = {"from": "Raspberry Pi<Raspi_notice@buhuipao.com>",
               "to": ["xxxxxxxxx@outlook.com", "xxxxxxxxxxx@163.com"],
               "subject": "来自树莓派报警",
               "html": html_tmp}
    try:
        requests.post(url, auth=auth, files=imgs, data=payload)
    except:
        pass


def send_sms():
    req = top.api.AlibabaAliqinFcSmsNumSendRequest(url, port)
    req.set_app_info(top.appinfo(appkey, secret))

    req.format = "json"
    req.extend = "123456"
    req.sms_type = "normal"
    req.sms_free_sign_name = "不会跑"
    req.rec_num = '152xxxxxxxx,131xxxxxxxx'
    req.sms_template_code = "SMS_37695056"

    try:
        req.getResponse()
    except:
        pass


def send_voice():
    req = top.api.AlibabaAliqinFcVoiceNumSinglecallRequest(url, port)
    req.set_app_info(top.appinfo(appkey, secret))

    req.extend = ""
    req.called_num = "131xxxxxxxx"
    req.called_show_num = "01053912806"

    req.voice_code = "c5473658-73f4-4831-8f61-e1eb468c8230.wav"
    try:
        req.getResponse()
    except Exception:
        pass
