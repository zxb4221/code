#!/usr/bin/python2.7
# -*- coding: UTF-8 -*-

import etcd3
import time

def main():
    key = "/zxb/test"
    etcd_server = "127.0.0.1"
    etcd_port = "2379"
    etcd_user = "admin"
    etcd_password = "admin"
    
    ttl = 30
    
    etcdClient = etcd3.Etcd3Client(host=etcd_server,port=etcd_port,user=etcd_user,password=etcd_password,timeout=3)
    node_lease = None
    
    while True:
        
        if node_lease == None:
            node_lease = etcdClient.lease(ttl)
            etcdClient.put(key,"123456",node_lease)
        else:
            node_lease.refresh()
            print etcdClient.get(key)
            
        time.sleep(10)


if __name__ == "__main__":
    main()

