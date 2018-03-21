# -*- coding: utf-8 -*-
# A lambda function to interact with AWS RDS MySQL
# @author =__Uluç Furkan Vardar__


import requests
from bs4 import BeautifulSoup
import pymysql
import sys
from slacker import Slacker
from datetime import datetime, timedelta
# needed lib imported

global now_time
global now_time1

REGION = 'us-east-1'
rds_host  = #your database host 
name = #your name
password = #your password
db_name = # your db_name
telegram_ID= #'your_id'
slack_ID= #'your_ID'
telegramChatID= #'your_chat_id'


telegramBotURL = 'https://api.telegram.org/'+telegram_ID+'/sendmessage?'    
slack=Slacker(slack_ID)

URLC='chat_id='+str(telegramChatID)+'&parse_mode=HTML&disable_web_page_preview=true&text='
telegramBotURL+=URLC

def googleNewsCrawler():

    global now_time
    global now_time1
    now_time1 = datetime.now()+ timedelta(hours=3) ## because of the server on the amazon current time diffrent
    now_time = '{:%H:%M}'.format(now_time1)

    #url of the page
    url='https://news.google.com/news/headlines?ned=tr_tr&hl=tr&gl=TR'
    #---getting source code of all page and creatin of firs BeautifulSoup object
    source_code=requests.get(url)
    plain_text=source_code.text
    sourceSoup=BeautifulSoup(plain_text,"html.parser")
    #---

    update_id=get_Update_id()
    #---
    global now_time
    global now_time1
    before_time=datetime.now() + timedelta(hours=2.5) +timedelta(minutes=15)
    before_timee=  '{:%H:%M}'.format(before_time)
    #--

    txt = []
    slacktxt = []
    recordList = []
    slackrecordList = []
    counter= []
    label = []

    for i in range (0,8):
        recordList.append("")
        slackrecordList.append("")
        counter.append(0)
        slacktxt.append("")
        txt.append("")
    label.append("En Çok Okunan Haberler")
    label.append("Dünya")
    label.append("Türkiye")
    label.append("Ekonomi")
    label.append("Bilim/Teknoloji")
    label.append("Magazin")
    label.append("Spor")
    label.append("Sağlık")

    #print "id bu ", update_id
    #---step by step into to 'En çok okunan haberler headers, urls, minutes and sources'
    for innerSoup1 in sourceSoup.find_all('div', {'class': 'WyeMbd'}):
        innerSoup1Source = BeautifulSoup(str(innerSoup1), "html.parser")
        for innerSoup2 in innerSoup1Source.find_all('c-wiz', {'jsrenderer': 'Jzy2fd'}):
            labell=innerSoup2.get('data-label')
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
                        save_New(url2,header,resource,before_time,update_id,conv(labell).lower())

                        slackUrlHeader=  conv(header) + '\n'+ str(url2) +'\n'
                        slackResource='Kaynak : '+str(resource)+ '\n'
                        slackTime="Süre : "+str(conv(before_time))+"\n\n"
                        slacktemptext=slackUrlHeader+slackResource+slackTime

                        url_header="<a href=\""+ str(url2) +'\">'+ conv(header)+'</a> \n'
                        resoruce_text='Kaynak : <b>'+str(resource)+ '</b>\n'
                        time="Süre : "+str('<b>'+conv(before_time)+'</b>')+"\n\n"
                        temptext=url_header+resoruce_text+time
                        for i in range(len(label)):
                            if labell==label[i]:
                                slackrecordList[i]+=slacktemptext
                                recordList[i]+=temptext
                                if "Hürriyet" in slacktemptext:
                                    counter[i]+=1

    for i in range(len(recordList)):
        if counter[i] == 0 :
            txt[i]="\n"+str(before_timee) +" : "+ str(now_time) +" zaman diliminde Google News verilerine göre <b>" + label[i] + "</b> kategorisinde hurriyet.com.tr üzerinde <b>haber bulunmamaktadır.</b>\n\n\n"
            slacktxt[i]="\n"+str(before_timee) +" : "+ str(now_time) +" zaman diliminde Google News verilerine göre " + label[i] + " kategorisinde hurriyet.com.tr üzerinde haber bulunmamaktadır.\n\n\n"
        elif counter[i] >0:
            txt[i]= "\n"+str(before_timee) +" : "+ str(now_time) +" zaman diliminde Google News verilerine göre <b>" + label[i] + "</b> kategorisinde hurriyet.com.tr üzerinde<b> "+str(counter[i])+"</b> haber bulunmaktadır.\n\n"
            slacktxt[i]= "\n"+str(before_timee) +" : "+ str(now_time) +" zaman diliminde Google News verilerine göre " + label[i] + " kategorisinde hurriyet.com.tr üzerinde "+str(counter[i])+" haber bulunmaktadır.\n\n"

    for i in range(len(recordList)):
        row = take_the_rule(conv(label[i]), int(now_time1.weekday() + 1), "T")
        flag = sendOrNo(row)
        if flag:
            print("sonuc ", flag)
            print "telegramda ",conv(label[i])," kategorisine mesaj gönderildi\n\n"
            temp="<pre> "+label[i]+" Kategorisinde Güncelleme  </pre>"+txt[i]+recordList[i]
            source_code = requests.get(telegramBotURL + temp)


    for i in range(len(recordList)):
        slackmessage=slacktxt[i]+slackrecordList[i]
        tag=str('#'+conv(label[i])).lower()
        if tag == "#en cok okunan haberler":
            tag="#cok-okunan-haberler"
        row = take_the_rule( conv(label[i]) , int(now_time1.weekday()+1) , "S" )
        flag = sendOrNo(row)
        if flag:
            print("sonuc ", flag)
            print "Slackte ", conv(label[i]), " kategorisine mesaj gönderildi\n\n"
            slack.chat.post_message(tag,slackmessage)

    row = take_the_rule("tagler", int(now_time1.weekday() + 1), "S")
    flag = sendOrNo(row)
    if flag:
    #---step by step into to Tags
        tags=""
        print "\n\ntagler*"
        for innerTag1 in sourceSoup.find_all('div', {'class':'QWD7rd JHzJp'}):
            innerTag1Source=BeautifulSoup(str(innerTag1),"html.parser")
            for innerTag2 in innerTag1Source.find_all('c-wiz', {'jsdata': 'deferred-i7'}):
                innerTag2Source=BeautifulSoup(str(innerTag2),"html.parser")
                for innerTag3 in innerTag2Source.find_all('div', {'class': 'Q3vG6d kzAuJ'}):
                    tag=innerTag3.string
                    tags+=tag+"\n"
                    print "tag saving",conv(tag),conv(update_id)
                    save_Tag(tag,update_id)
        mess="\n"+str(before_timee) +" : "+ str(now_time) +" zaman diliminde Google News verilerine göre popüler #Tagler"+tags
        slack.chat.post_message('#populer-tagler',mess)
    #---



def take_the_rule(topic, dayOfTheWeek, platform):
    conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
    with conn.cursor() as cur:
        cur.execute("""select * from innodb.RULES as r where innodb.r.topic="%s" and innodb.r.dayOfTheWeek=%s and innodb.r.platform="%s" """ % (
            str(topic), str(dayOfTheWeek), str(platform)))
        conn.commit()
        cur.close()
        for row in cur:
            for i in range(1,len(row)):
                print row[i],
            return row ## always the first row returns

def save_Tag(tag, update_id):
    conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
    with conn.cursor() as cur:
        cur.execute("""call innodb.createTag("%s", %s );""" % (conv(tag), conv(update_id)))
        conn.commit()
        cur.close()

def save_New(url, header, resource, before_time, update_id, label):
    conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
    with conn.cursor() as cur:
        cur.execute("""call innodb.createNew("%s","%s","%s","%s",%s,"%s");""" % (
        conv(url), conv(header), conv(resource), conv(before_time), conv(update_id), conv(label)))
        conn.commit()
        cur.close()

def get_Update_id():
    conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
    with conn.cursor() as cur:
        cur.execute("""INSERT INTO innodb.Updates (Update_Time) VALUES ( NOW() );""")
        cur.execute("""SELECT  MAX( u.update_id ) FROM innodb.Updates as u;""")
        conn.commit()
        cur.close()
        for row in cur:
            return str(row[0])

def conv(a):
    a = str(a)
    for x in range(0, len(a)):
        a = a.replace('\"', '\'')
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
        a = a.replace('/', '-')

    return a

#This method writen for to make desition abour a message send or not
def intervalCheck(period,fromstarting,now):
    date_format = "%H:%M"
    z = datetime.strptime("00:00", date_format) #zero time
    #print "initial ", z
    for i in range(0, 96): # there are only 96 15minutes exist in e one day
        multiple_time= z + timedelta(minutes=period*i)
        deltaMultiple=multiple_time-z
        #print "bound1 ",deltaMultiple - timedelta(minutes=8) ," bound2 ",deltaMultiple + timedelta(minutes=8)
        if deltaMultiple - timedelta(minutes=8) <= fromstarting <= deltaMultiple +timedelta(minutes=8):
            #print fromstarting,"send"
            return True
        else:
            if now<multiple_time:
                print fromstarting,"not send zaman tutmadı"
                return False
    return False

def sendOrNo(row):
    global now_time
    if row==None or row[2] == None :
        return False
    global now_time1
    print "\n\nsorgu nun icerigi ",row
    dayOfTheWeek=int(now_time1.weekday()+1)
    if dayOfTheWeek==row[2] : #day check
        date_format = "%H:%M"
        a = datetime.strptime(row[3], date_format) #start time
        b = datetime.strptime(row[4], date_format) # end time
        c = datetime.strptime(str(now_time), date_format) #now
        if a < c < b:
            #print "in"
            d=c-a #time from the opening
            #print "a",a,"\nb",b,"\nc",c,"\nd",d
            print "ne zmandir acik ", d
            return intervalCheck(int(row[5]),d,c) ## if periof is okey send otherwise dont
        else:
            print 'No!'
            return False
    else :
        print"dont send"
        return False

def main(event, context):
    googleNewsCrawler()








