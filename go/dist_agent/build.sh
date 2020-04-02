#!/bin/bash

etcd_root="/opt/zxb/dev"

cp -r ../dist_agent ${etcd_root}/etcd/contrib/

mkdir -p ${etcd_root}/src/go.etcd.io

ln -s ${etcd_root}/etcd ${etcd_root}/src/go.etcd.io/etcd


cd ${etcd_root}/src/go.etcd.io/etcd/contrib/dist_agent

export GOPATH=${etcd_root}

go build


