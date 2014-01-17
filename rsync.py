#!/usr/bin/env python
# синхронизируем два каталога
 
from subprocess import call
import sys
import time
import subprocess

source = "/tmp/sync_dir_A/" # обратите внимание на закрывающий слэш
target = "/tmp/sync_dir_B"
rsync = "rsync"
arguments = "-av"
cmd = "%s %s %s %s" % (rsync, arguments, source, target)
 
def sync():
    while True:
        ret = call(cmd, shell=True)
        if ret !=0:
            print "resubmitting rsync"
            time.sleep(30)
        else:
            print "rsync was succesful"
            subprocess.call("mail -s 'jobs done' admin@acidnation.ru", shell=True)
            sys.exit(0)
sync()