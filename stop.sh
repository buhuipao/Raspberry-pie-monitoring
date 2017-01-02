#!/bin/bash
# 停止脚本
ps -aux | grep "python" | grep -v "grep"| awk '{print $2}'| xargs sudo kill