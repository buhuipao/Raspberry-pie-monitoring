#!/bin/bash
# 启动脚本
nohup python monitor.py >output2 2>&1 &
nohup python pi.py >output1 2>&1 &
