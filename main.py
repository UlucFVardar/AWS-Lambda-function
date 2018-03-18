# -*- coding: utf-8 -*-
# A lambda function to interact with AWS RDS MySQL
# @author =__Uluç Furkan Vardar__

import requests
from bs4 import BeautifulSoup

import pymysql
import sys
#needed lib imported


REGION = 'us-east-1'
rds_host  = #your database host 
name = #your name
password = #your password
db_name = # your db_name


def googleNewsCrawler():
    #url of the page
    url='https://news.google.com/news/headlines?ned=tr_tr&hl=tr&gl=TR'
    #---getting source code of all page and creatin of firs BeautifulSoup object
    source_code=requests.get(url)
    plain_text=source_code.text
    sourceSoup=BeautifulSoup(plain_text,"html.parser")
    #---
    update_id=get_Update_id()
    print "id bu ", update_id
    #---step by step into to 'En çok okunan haberler headers, urls, minutes and sources'
    for innerSoup1 in sourceSoup.find_all('div', {'class': 'WyeMbd'}):
        innerSoup1Source = BeautifulSoup(str(innerSoup1), "html.parser")
        for innerSoup2 in innerSoup1Source.find_all('c-wiz', {'jsrenderer': 'Jzy2fd'}):
            label=innerSoup2.get('data-label')
            innerSoup2Source=BeautifulSoup(str(innerSoup2), "html.parser")
            for innerSoup3 in innerSoup2Source.find_all('div',{'class':'deQdld'}):
                innerSoup3Source = BeautifulSoup(str(innerSoup3), "html.parser")
                for innerSoup4 in innerSoup3Source.find_all('c-wiz',{'class':'M1Uqc kWyHVd'}):
                    innerSoup4Source = BeautifulSoup(str(innerSoup4), "html.parser")
                    for innerSoup5 in innerSoup4Source.find_all('a',{'class':'nuEeue hzdq5d ME7ew'}):
                        header=innerSoup5.string
                        url2=innerSoup5.get('href')
                        resource=""
                        before_time=""
                        for innerSoup6 in innerSoup4.find_all('span',{'class':'IH8C7b Pc0Wt'}):
                            resource=innerSoup6.string
                        for innerSoup7 in innerSoup4.find_all('span',{'class':'d5kXP YBZVLb'}):
                            before_time=innerSoup7.string
                        print "news saving",conv(url2),conv(header),conv(resource),conv(before_time),conv(update_id),conv(label)
                        save_New(url2,header,resource,before_time,update_id,label)
    #---step by step into to Tags
    print "\n\ntagler*"
    for innerTag1 in sourceSoup.find_all('div', {'class':'QWD7rd JHzJp'}):
        innerTag1Source=BeautifulSoup(str(innerTag1),"html.parser")
        for innerTag2 in innerTag1Source.find_all('c-wiz', {'jsdata': 'deferred-i7'}):
            innerTag2Source=BeautifulSoup(str(innerTag2),"html.parser")
            for innerTag3 in innerTag2Source.find_all('div', {'class': 'Q3vG6d kzAuJ'}):
                tag=innerTag3.string
                print "tag saving",conv(tag),conv(update_id)
                save_Tag(tag,update_id)
    #---
     
def save_Tag(tag,update_id):
    conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
    with conn.cursor() as cur:
        cur.execute("""call innodb.createTag("%s", %s );""" % (conv(tag),conv(update_id)))
        conn.commit()
        cur.close()
def save_New(url,header,resource,before_time,update_id,label):
    conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
    with conn.cursor() as cur:
        cur.execute("""call innodb.createNew("%s","%s","%s","%s",%s,"%s");""" % (conv(url),conv(header),conv(resource),conv(before_time),conv(update_id),conv(label)))
        conn.commit()
        cur.close()
def get_Update_id():
    conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
    with conn.cursor() as cur:
        cur.execute("""INSERT INTO innodb.Updates (Update_Time) VALUES ( NOW() );""" )
        cur.execute("""select LAST_INSERT_ID();""" )
        conn.commit()
        cur.close()
        for row in cur:
            return str(row[0])

def conv(a):
    a=str(a)
    for x in range (0,len(a)):
        a = a.replace('\"','\'')
        a = a.replace('İ', 'I')
        a = a.replace('Ş', 's')
        a = a.replace('Ç', 'C')
        a = a.replace('Ü', 'U')
        a = a.replace('Ö', 'O')
        a = a.replace('ş', 's')
        a = a.replace('ğ', 'g')
        a = a.replace('ı', 'i')
        a = a.replace('ö', 'o')
        a = a.replace('ü', 'u')
        a = a.replace('ç', 'c')
    return a
    

def main(event, context):
    googleNewsCrawler()
        

