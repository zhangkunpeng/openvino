#!/bin/python
# Manage the process of openvino

import os
import time
import signal
import central

pid = os.fork()

def write_info():
    info = ''
    usb_info = os.popen('lsusb')
    disk_info = os.popen('lsblk')
    len_usb = 0
    for line in usb_info:
        len_usb += 1
    info += str(len_usb)
    
    for line in disk_info:
        info += str(line)
    f = open('status', 'w')
    f.write(info)
    f.close()
    return info

def stop_model():
    model_info = os.popen('pgrep -f intel')
    model_pids = []
    for single_pid in model_info:
        if single_pid:
            model_pids.append(int(single_pid))
    if len(model_pids) > 1:
        for model_pid in model_pids:
            try:
                os.kill(model_pid, signal.SIGKILL)
            except Exception:
                continue
            print 'kill' + str(model_pid)

def check_new_model(version):
    new_version = central.get_version()
    return version != new_version

while True:
    time.sleep(2)
    version == central.get_version()
    if pid == 0:
        os.system('python openvino_run_all.py '+ version )
    else:
        while True:
            time.sleep(2)
            if os.path.isfile('./status'):
                old_file = open('status', 'r')
                old_info = old_file.read()
                old_file.close()
                info = write_info()
                if old_info != info or check_new_model():
                    stop_model()
                    break
            else:
                write_info()
                break
            
    
    


