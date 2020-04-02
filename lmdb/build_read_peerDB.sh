#!/bin/sh
g++ -fpermissive -std=c++11 -I/root/git/boost_1_67_0 -I/root/git/lmdb/libraries/liblmdb -I/root/git/bytecoin/src \
read_peerDB.cpp \
/root/git/bytecoin/src/seria/JsonInputValue.cpp \
/root/git/bytecoin/src/seria/JsonOutputStream.cpp \
/root/git/bytecoin/src/seria/KVBinaryInputStream.cpp \
/root/git/bytecoin/src/seria/KVBinaryOutputStream.cpp \
/root/git/bytecoin/src/seria/BinaryInputStream.cpp  \
/root/git/bytecoin/src/seria/BinaryOutputStream.cpp \
/root/git/bytecoin/src/common/BinaryArray.cpp \
/root/git/bytecoin/src/common/StringView.cpp \
/root/git/bytecoin/src/common/Streams.cpp \
/root/git/bytecoin/src/common/MemoryStreams.cpp \
/root/git/bytecoin/src/common/StringTools.cpp \
/root/git/bytecoin/src/common/JsonValue.cpp \
/root/git/bytecoin/src/common/Varint.cpp \
/root/git/bytecoin/src/platform/Files.cpp \
-o read_peerDB /root/git/lmdb/libraries/liblmdb/liblmdb.a -lpthread
