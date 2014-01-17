import socket,ConfigParser,sys,thread,time,datetime,os

def servmon(ip,port,ithread,icmd):
#    print icmd
    print "Thread " + str(ithread) + " of monitoring server started\n"
    retry = 0
    while 1:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect((ip, int(port)))
        sock.send('\377\377\377\377TSource Engine Query\0')
        print "Thread " + str(ithread)+": "+ "Send ok to "+ip+":"+port+" waiting response for 45 sec....\n"
        sock.settimeout(45)
        try:
            text=sock.recv(1024)
        except Exception, e:
            print "Thread " + str(ithread)+": " + "Error:%s"%e + " on server ip"+ip+":"+port
            retry = retry + 1
            print "retry: " + str(retry)
            if retry > 3:
                print "Thread " + str(ithread)+": " + "retry is more than 3, send restart cmd to system!"
                print icmd
                os.system(icmd)
            time.sleep(13)
            pass
        else:
            if text.find('cstrike') > 1:
                print "Thread " + str(ithread)+": "+ "Response ok from "+ip+":"+port+" next retry to request is 45 sec.\n"
                retry = 0
            time.sleep(45)



srvcs = [ics.strip("\n") for ics in open('server.list')]

print "list of loaded servers:"
for ics in srvcs:
    ip,port,icmd = ics.split(":")
    print ip+":"+port
print "\n"
ithread = 0
for ics in srvcs:
    ip,port,icmd = ics.split(":")
    ithread = ithread + 1
    thread.start_new_thread(servmon, (ip,port,ithread,icmd))
while 1:
		time.sleep(10)
		print "I'm still work and monitoring your servers:)"
