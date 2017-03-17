# _*_ coding: utf-8 _*_ 

'''
用bypy库手动鉴权,文档地址：https://github.com/houtianze/bypy
'''
from baidu import ByPy
import os
import notice
import phash
import time
# from pdb import set_trace


def monitor(count):
    '''
    先排序图片名，再统计目录下的jpeg图片数目是否为大于2
    传入的参数count是为了表示报警级别:
    count: 0, 不报警;
    count: 0~2, 邮件报警;
    count: 3~5, 邮件+短信报警;
    count: 6~N, 邮件+短信+电话报警;
    '''

    files = sorted([f for f in os.listdir('.') if f.find('jpeg') != -1])
    if len(files) < 2:
        return min(count, 5)
    remote_path = '-'.join(files[-1].split('-')[:3]) + '/' + files[-1]
    try:
        bypy = ByPy()
        bypy.upload(files[-1], remote_path)
    except:
        pass

    # 如果两幅图指纹不同, 发送邮件和短信, 最后只保留最后一张图片
    print('Start diff imges...')
    if phash.imgs_diff(files[-2], files[-1]):
	count += 1
	try:   
            notice.send_mail(files[-2:])
	    if 6 > count >= 3:
                notice.send_sms()
	    elif count >= 6:
	    	notice.send_voice()
	except:
	    pass
    else:
	count = count - 3 if count - 3 >= 0 else 0
    for img in files[:-1]:
        os.remove(img)
    # 假设遇到长时间报警(count>>6)之后间歇正常(count-3仍然大于6)
    # 不应该一直语音报警，而是取count和5的较小值进行报警降级
    return min(count, 5)

def run():
    count = 0
    while True:
        start = time.time()
        count = monitor(count)
	print(type(count), count)
        used = time.time() - start
        time.sleep(10-used) if used <= 10 else 0
	
if __name__ == '__main__':
    run()
