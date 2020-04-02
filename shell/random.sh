#!/bin/bash

#这是一个抽奖脚本，从user数组中随机抽出一人

user=('A' 'B' 'C' 'D')
size=${#user[@]}
index=$(($RANDOM%$size))

echo ${user[$index]}
