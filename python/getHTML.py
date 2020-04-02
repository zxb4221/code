# -*- coding: utf-8 -*- 
import urllib2
url="http://app.finance.ifeng.com/hq/list.php?type=stock_a&class=ha"
response=urllib2.urlopen(url)
cont=response.read()#从up中读入该HTML文件
print cont
