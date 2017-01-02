#!/bin/bash
#ps -aux | grep "\.py" | head -n 2 | awk '{print $2}'| xargs sudo kill

nohup python monitor.py >output2 2>&1 &
nohup python pi.py >output1 2>&1 &
