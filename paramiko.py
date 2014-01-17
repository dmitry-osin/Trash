#!/usr/bin/env python
 
import paramiko
import os
 
hostname = '192.168.1.2'
port = 22
username = 'justz'
password = '123456'
dir_path = '/home/z/arc'
 
if __name__ == "__main__":
    t = paramiko.Transport((hostname, port))
    t.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(t)
    files = sftp.listdir(dir_path)
    for f in files:
        print 'Retrieving', f
        sftp.get(os.path.join(dir_path, f), f)
    t.close()