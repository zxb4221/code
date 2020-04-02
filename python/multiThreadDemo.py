# -*- coding: utf-8 -*- 

import time
from multiprocessing import Process, Queue
import threading
import os
import signal

log_queue = Queue()

global_v = 0

def thread_run(id):
    msg = {"clusterID":id, "processID":os.getpid(), "log":"this is log info"}
    
    global global_v
    global_v = int(id)
    
    print "process:%d global_v:%d"%(os.getpid(),global_v)
    
    if id == "1":
        time.sleep(20)
    elif id == "2":
        time.sleep(1)


def main():
    
    

    print "main A global_v:%d"%global_v

    t1 = threading.Thread(target=thread_run, args=("1",))
    t2 = threading.Thread(target=thread_run, args=("2",))

    t1.start()
    t2.start()

    print "t1 is alive:%s"%(str(t1.is_alive()))
    print "t2 is alive:%s"%(str(t2.is_alive()))
    time.sleep(10)
    
    print "t1 is alive:%s"%(str(t1.is_alive()))
    print "t2 is alive:%s"%(str(t2.is_alive()))

    print "main B global_v:%d"%global_v
    
    time.sleep(12)
    print "t1 is alive:%s"%(str(t1.is_alive()))
    print "t2 is alive:%s"%(str(t2.is_alive()))



if __name__ == "__main__":
    main()
