"""


기존관 및 BTL 식단표를 가져오는 부분 (django Ver)

작 성 : 정보보호학과 15학번 김민우

수 정 : 정보보호학과 15학번 임재연

"""

"""

crontab을 통해 주기적으로 실행시켜줘야 함
현재 서버 옵션
5,55 23,0 * * *  python위치 파일위치/Wmenu.py
-> 매일 0시 5분 / 0시 55분 / 23시 5분 /  23시 55분
-> 하루에 4번 데이터를 파싱하여 데이터베이스에 저장시킴

"""



import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "algorithm_LAB.settings")
import django
django.setup()

import time
import sys
from bs4 import BeautifulSoup
import urllib.request as urllib2

from mnu_bot.models import Food

def parser(url):
        req = urllib2.Request(url)
        res = urllib2.urlopen(req)
        data = res.read()
        soup = BeautifulSoup(data,"html.parser")
        Table = soup.findAll('table',{"class":"table-tdl"})
        return Table[0].findAll("td")
def data_save(Tables,m):
    when = ["아침","점심","저녁"]
    dormi =  {"":"기존관","_btl":"BTL"}
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
				# w => 요일 , count => 아점저
        menu = day[count]+"\n"+i.get_text().strip().replace("\r","")
        food = Food.objects.get_or_create(dormi=dormi[m],when=str(w)+str(count))[0]
        food.menu = menu
        food.save()
        count = count + 1
def data_save2(Tables,m):
    when = ["아침","점심","저녁"]
    dormi = {"":"기존관","_btl":"BTL"}
    count = 0
    w = 0
    day = {0:"++상쾌한 아침++",1:"++든든한 점심++",2:"++즐거운 저녁++"}
    for i in Tables:
        if i.find_all("span"):
            continue
        if count == 3:
            break
				#다음주 월요일의 메뉴 파싱 when = 9
        menu = day[count]+"\n"+i.get_text().strip().replace("\r","")
        food = Food.objects.get_or_create(dormi=dormi[m],when="9"+str(count))[0]
        food.menu = menu
        food.save()
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
