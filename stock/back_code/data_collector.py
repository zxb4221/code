#coding=utf8


import ConfigParser  
import urllib2
import MySQLdb
import time
import json


config = ConfigParser.ConfigParser()
config.readfp(open("../config/config.ini", "rb"))
ip = config.get("database", "ip")
port = config.get('database','port')
user = config.get('database','user')
password = config.get('database','password')




try:
    conn=MySQLdb.connect(host='127.0.0.1',user='zxb',passwd='1234',db='stock',port=3306,charset='utf8')
    conn.autocommit(1)
    cur=conn.cursor()
#    cur.execute("insert into stock_meta(code,name) values('test','test')")
#    cur.close()
#    conn.close()
except MySQLdb.Error,e:
    print "Mysql Error %d: %s" % (e.args[0], e.args[1])


# 凤凰财经沪A股、深A票列表
url_HA="http://app.finance.ifeng.com/hq/list.php?type=stock_a&class=ha"
url_SA="http://app.finance.ifeng.com/hq/list.php?type=stock_a&class=sa"


#查询股票时，一次查询多少个
STOCK_QUERY_SIZE=50

def CollectStockMetaData():
    print "CollectStockMetaData..."
    print "read stock_meta..."

    codes=[]
    try:
        sql = "select code from stock_meta"
        cur.execute(sql)
        results = cur.fetchall()
        for row in results:
            codes.append(row[0])
    except Exception,e:
        print e
    
    urls = [url_HA,url_SA]
    for url in urls:   
        
        print "connect url:" + url

        response=urllib2.urlopen(url)
        cont=response.read()            #从up中读入该HTML文件

        
        index = cont.find('<div class="result">')
        cont = cont[index:len(cont)]

        index = cont.find('<li>')
        cont = cont[index:len(cont)]

        index = cont.find('</ul>')
        cont = cont[0:index]

        cont = cont.strip()


        while(cont != ""):
            itemBeginIndex = cont.find('<li>')
            itemEndIndex = cont.find('</li>')
            item = cont[itemBeginIndex:itemEndIndex+5]
            cont = cont[itemEndIndex+5:len(cont)]
    
    
            itemBeginIndex = item.find('">')
            itemEndIndex = item.find('</a>')
            item = item[itemBeginIndex+2:itemEndIndex]

    
            stockName = item[0:item.find('(')]
            stockCode = item[item.find('(')+1:item.find(')')]
            
            if(stockCode in codes):
                codes.remove(stockCode)
                continue


            #TODO code正确性判断
            sql = "replace into stock_meta(code,name) values('%s','%s')" %(stockCode,stockName)   
            try:
                cur.execute(sql)
                print "####" + sql + "####"
            except Exception,e:
                print e

        print cont
    
    #删除的code
    for code in codes:
        sql = "delete from stock_meta where code='%s'" %(code)
        try:
            cur.execute(sql)
            print "####" + sql + "####"
        except Exception,e:
            print e

def CollectStockDataByHttps(codes):
    print "CollectStockData..."

    baseUrl = 'https://hq.finance.ifeng.com/q.php?l='
    url = baseUrl
    for code in codes:

        if(code[0] == '6'):
            url = url + "sh" + code + ","
        elif(code[0] == '0'):
            url = url + "sz" + code + ","
        else:
            print "stock code invalid,code:" + code
            continue

    while True:
        try:
                    
            response=urllib2.urlopen(url,timeout=10)
            content = response.read()
        except Exception,e:
            print e
            print url
            time.sleep(2)
            continue

        while content.find('[') != -1:
            #+3是为了去除前缀，如sz,sh
            codeReturn = content[content.find('"')+3:content.find(':')-1]

            indexBegin = content.find('[')
            indexEnd = content.find(']')
            itemsText = content[indexBegin+1:indexEnd]
            content = content[indexEnd+1:len(content)]
                    
            if(itemsText == "" or itemsText.find(',') == -1):
                continue
            items = itemsText.split(',')
            if(len(items) <= 0):
                continue
            value = items[len(items)-1]
            try:
                if(float(value) > 10000 or float(value) <= 0.0):
                    print "stock value is not valid:%s,%s" %(code,value)
                    continue
            except Exception,e:
                print e
                        
            sql = "replace into stock_data(code,value,insert_date) values('%s',%s,date_format(now(),'%s'))" %(codeReturn,value,"%Y-%m-%d")
            try:
                cur.execute(sql)
                print codeReturn + ":" + value
            except Exception,e:
                print e
        break

def CollectStockData():
    codes = []
    try:
        sql = "select code from stock_meta"
        cur.execute(sql)
        results = cur.  fetchall()
        for row in results:
            codes.append(row[0])
            
    except Exception,e:
        print e
    
    count = 0
    codesToProcess=[]
    for code in codes:
        codesToProcess.append(code)
        if(len(codesToProcess) >= STOCK_QUERY_SIZE): 
             CollectStockDataByHttps(codesToProcess)
             time.sleep(2)
             codesToProcess=[]
    CollectStockDataByHttps(codesToProcess)

if __name__=='__main__':
    CollectStockMetaData()
    CollectStockData()
