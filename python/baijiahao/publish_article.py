#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import json
import argparse
import sys

def read_file(file_path):
    f = open(file_path, 'r')
    content = f.read()
    f.close()
    return content 

def main():
    parser = argparse.ArgumentParser(description='manual to this script',add_help=False)
    parser.add_argument('-i', '--app_id', dest='app_id', type=str, help='app_id', default = None)
    parser.add_argument('-k', '--app_token', dest='app_token', type=str, help='app_token', default = None)
    parser.add_argument('-f', '--file_path', dest='file_path', type=str, help='file_path', default = None)
    parser.add_argument('-t', '--title', dest='title', type=str, help='title', default = None)
    parser.add_argument('-h', '--help', dest='help', action='store_true', help='help infomation', default=False)
    args = parser.parse_args()
    
    if args.app_id is None:
        print ("app_id can't be None!")
        sys.exit(-1)
    if args.app_token is None:
        print ("app_token can't be None!")
        sys.exit(-1)
    if args.file_path is None:
        print ("file_content can't be None!")
        sys.exit(-1)
    if args.title is None:
        print ("title can't be None!")
        sys.exit(-1)
    content = read_file(args.file_path)

    obj = {}
    obj["app_id"] = args.app_id
    obj["app_token"] = args.app_token
    obj["title"] = args.title
    #obj["cover_images"] = []
    #obj["is_original"] = 1
    obj["origin_url"] = "https://www.jianshu.com/u/4485630816d3"
    obj["content"] = content

    
    url = "http://baijiahao.baidu.com/builderinner/open/resource/article/publish"
    body = json.dumps(obj)
    print (body)
    headers = {"content-type": "application/json"}
    response = requests.post(url, data = body, headers = headers)
    print (response.text)
    print (response.status_code)

if __name__ == "__main__":
    main()
