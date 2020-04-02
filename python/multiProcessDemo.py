# -*- coding: utf-8 -*- 

import time
from multiprocessing import Process, Queue
import threading
import os
import signal

log_queue = Queue()

global_v = 0

def process_run(id, queue):
    msg = {"clusterID":id, "processID":os.getpid(), "log":"this is log info"}
    queue.put(msg)
    
    global global_v
    global_v = int(id)
    
    print "process:%d global_v:%d"%(os.getpid(),global_v)
    
    if id == "1":
        time.sleep(20)
def thread_run():
    while True:
        value = log_queue.get(True)
        print "clusterID:%s,processID:%s,log:%s"%(value["clusterID"], value["processID"], value["log"])

        if value["clusterID"] == "0":
            return


def main():
    
    t = threading.Thread(target=thread_run, name='LogThread')
    t.start()
    

    print "main A global_v:%d"%global_v

    p1 = Process(target=process_run, args=("1",log_queue,))
    p2 = Process(target=process_run, args=("2",log_queue,))

    p1.start()
    p2.start()

    print "p1 is alive:%s"%(str(p1.is_alive()))
    print "p2 is alive:%s"%(str(p2.is_alive()))
    time.sleep(10)
    
    print "p1 is alive:%s"%(str(p1.is_alive()))
    print "p2 is alive:%s"%(str(p2.is_alive()))

    print "main B global_v:%d"%global_v
    
    time.sleep(12)
    print "p1 is alive:%s"%(str(p1.is_alive()))
    print "p2 is alive:%s"%(str(p2.is_alive()))

    log_queue.put({"clusterID":"0", "processID":os.getpid(),"log":"main thread end!"})       


if __name__ == "__main__":
    main()
