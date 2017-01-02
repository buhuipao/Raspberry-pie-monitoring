# 这是我的毕业设计，树莓派寝室安防监控
## 第一步: 用autossh打通内网控制障碍

树莓派安装autossh,并且生成公钥私钥

```bash
sudo apt-get install autossh
ssh-keygen
ssh-copy-id username@server_ip
```
新建autossh自启动脚本, chmod a+x autossh 并运行, 脚本的内容：
```
#!/bin/bash
/bin/su -c '/usr/bin/autossh -M 1234 -NR 19999:localhost:22 buhuipao@server_ip -p your_port' - pi &
```
复制autossh到/etc/init.d/目录下, 执行:
```
sudo update-rc.d autossh defaults 90
```
这样就可以在自己的服务器上登录你的树莓派了
```
ssh -p 19999 pi@localhost
```
## 第二步：安装必要的软件
