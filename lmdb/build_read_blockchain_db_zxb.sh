#!/bin/sh
g++ -fpermissive -std=c++11 -I/home/zxb/workspace/bcndev/boost -I/home/zxb/workspace/bcndev/lmdb/libraries/liblmdb -I/home/zxb/workspace/bcndev/bytecoin/src \
read_peerDB.cpp \
/home/zxb/workspace/bcndev/bytecoin/src/seria/JsonInputValue.cpp \
/home/zxb/workspace/bcndev/bytecoin/src/seria/JsonOutputStream.cpp \
/home/zxb/workspace/bcndev/bytecoin/src/seria/KVBinaryInputStream.cpp \
/home/zxb/workspace/bcndev/bytecoin/src/seria/KVBinaryOutputStream.cpp \
/home/zxb/workspace/bcndev/bytecoin/src/seria/BinaryInputStream.cpp  \
/home/zxb/workspace/bcndev/bytecoin/src/seria/BinaryOutputStream.cpp \
/home/zxb/workspace/bcndev/bytecoin/src/common/BinaryArray.cpp \
/home/zxb/workspace/bcndev/bytecoin/src/common/StringView.cpp \
/home/zxb/workspace/bcndev/bytecoin/src/common/Streams.cpp \
/home/zxb/workspace/bcndev/bytecoin/src/common/MemoryStreams.cpp \
/home/zxb/workspace/bcndev/bytecoin/src/common/StringTools.cpp \
/home/zxb/workspace/bcndev/bytecoin/src/common/JsonValue.cpp \
/home/zxb/workspace/bcndev/bytecoin/src/common/Varint.cpp \
/home/zxb/workspace/bcndev/bytecoin/src/platform/Files.cpp \
-o read_peerDB /home/zxb/workspace/bcndev/lmdb/libraries/liblmdb/liblmdb.a -lpthread
