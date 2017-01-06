# _*_ coding: utf-8 _*_

'''
采用阿里大于平台推送的短信，依靠mailgun推送邮件, 接下来可能会改用极光的短信推送
'''
import requests
import top
import re
import os


def send_mail(imglist):
    '''
    imglist的长度应该为2
    '''
    with open('mail.html', 'r') as f:
        html_tmp = f.read().replace('IMG1', imglist[0]).replace('IMG2', imglist[1])
    url = "https://api.mailgun.net/v3/your_mail_domain/messages"
    auth = ("api", "your_mailgun_domain_key")
    imgs = [("inline", open(imglist[0])), ("inline", open(imglist[1]))]
    payload = {"from": "Raspberry Pi<Raspi_notice@buhuipao.com>",
               "to": mail_list,
               "subject": "来自树莓派报警",
               "html": html_tmp}
    r = requests.post(url, auth=auth, files=imgs, data=payload)
    print(r.json())


def send_sms():
    url = 'gw.api.taobao.com'
    appkey = 'your_app_key'
    secret = 'your_app_secret'
    port = 80
    req = top.api.AlibabaAliqinFcSmsNumSendRequest(url, port)
    req.set_app_info(top.appinfo(appkey, secret))

    req.format = "json"
    req.extend = "123456"
    req.sms_type = "normal"
    req.sms_free_sign_name = "不会跑"
    req.rec_num = ','.join(number_list)
    req.sms_template_code = " "

    try:
        r = req.getResponse()
        print(r)
    except Exception as e:
        print(e)


def send_notice(imgs):
    '''
    pattern = re.compile(r'jpeg')
    files = [f for f in os.listdir('.') if re.search(pattern, f.split('.')[-1])]
    if len(files) < 2:
        return
    else:
        imgs = files[-2:]
    '''
    send_sms()
    send_mail(imgs)


def send_voice():
    url = 'gw.api.taobao.com'
    appkey = 'your_app_key'
    secret = 'your_app_secret'
    port = 80
    req = top.api.AlibabaAliqinFcVoiceNumSinglecallRequest(url, port)
    req.set_app_info(top.appinfo(appkey, secret))

    req.format = "json"
    req.extend = "12345"
    req.called_num = "13700000000"
    req.called_show_num = "4001112222"
    req.voice_code = "Your voice id"
    try:
        resp = req.getResponse()
        print(resp)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    send_notice()
