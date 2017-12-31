"""
Wmenu.py
학생생활관 홈페이지에서 식단 정보를 가져오는 코드
작  성 : 정보보호학과 15학번 김민우
"""

import time
import sys
from bs4 import BeautifulSoup
import urllib.request as urllib2
def parser(url):
        req = urllib2.Request(url)
        res = urllib2.urlopen(req)
        data = res.read()
        soup = BeautifulSoup(data,"html.parser")
        Table = soup.findAll('table',{"class":"table-tdl"})
        return Table[0].findAll("td")
def data_save(Tables,m):
    count = 0
    w = 6
    day = {0:"++상쾌한 아침++",1:"++든든한 점심++",2:"++즐거운 저녁++"}
    for i in Tables:
        if i.find_all("span"):
            continue
        if count == 3:
            count = 0
            w = w + 1
            if w == 7:
                w=0
        f = open("/home/nirone7/mnu_bot/food/"+m+"/menu_"+str(w)+"_"+str(count)+".txt","w")
        f.write(day[count]+"\\n"+i.get_text().strip().replace("\n","\\n").replace("\r",""))
        f.close()
##        f = open(m+"menu_"+str(w)+"_"+str(count)+".txt","w")
##        f.write(day[count]+"\\n"+i.get_text().strip().replace("\n","\\n").replace("\r",""))
##        f.close()
        count = count + 1
def data_save2(Tables,m):
    count = 0
    w = 0
    day = {0:"++상쾌한 아침++",1:"++든든한 점심++",2:"++즐거운 저녁++"}
    for i in Tables:
        if i.find_all("span"):
            continue
        if count == 3:
            break
        f2 = open("/home/nirone7/mnu_bot/food/"+m+"/T_menu_6"+"_"+str(count)+".txt","w")
        f2.write(day[count]+"\\n"+i.get_text().strip().replace("\n","\\n").replace("\r",""))
        f2.close()
##        f2 = open(m+"T_menu_6"+"_"+str(count)+".txt","w")
##        f2.write(day[count]+"\\n"+i.get_text().strip().replace("\n","\\n").replace("\r",""))
##        f2.close()                
        count = count+1
def main(m):
    now = time.localtime()
    url = "http://dormi.mokpo.ac.kr/www/bbs/board.php?bo_table=food"+m
    Tables=parser(url)
    data_save(Tables,m)
    url = "http://dormi.mokpo.ac.kr/www/bbs/board.php?bo_table=food"+m+"&mode=w&year="+str(now.tm_year)+"&month="+str(now.tm_mon)+"&day="+str(now.tm_mday+7)
    Tables=parser(url)
    data_save2(Tables,m)
	

if __name__=="__main__":
	main("")
	main("_btl")

