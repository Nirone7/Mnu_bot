import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "algorithm_LAB.settings")
import django
django.setup()

import re
import datetime
from mnu_bot.models import Food

import urllib.parse as urp
import urllib.request as urllib2
from os.path import basename

def save_media(userRequest):  #이미지 저장부분(매개변수는 전달된 요청값(콘텐츠,타입,메시지)데이터)
	user = userRequest['user_key']
	imgSrc = userRequest['content']
	imgContent = urllib2.urlopen(imgSrc).read()
	imgFileName = basename(urp.urlsplit(imgSrc)[2]).replace("../","")
	with open("/home/nirone7/JY/media/{}_".format(user)+imgFileName, 'wb') as imgFile:
		imgFile.write(imgContent)

def function_call(message):
	foo,var = re.findall("\((.*?)\)",message)[0].split(",") # function_call(foo,var) => foo = foo, var = var
	try:
		data = eval("{}({})".format(foo,var))
		return data
	except:
		data = "정의되지 않은 기능입니다."
		return data






## mokpo dormi food ##
def get_food(message):
	# message == "기존관/BTL 아침/점심/저녁" 형태로 받음
	# 데이터베이스에 밥을 저장할때 dormi=기존관, when=요일(숫자)아점저(012) 로 저장
	# ex dormi="기존관" , when = 01(월 점심) 0->월요일
	menu_list ={
		"아침":"0", "점심":"1", "저녁":"2",
		"오늘":"3", "내일":"4"
	}
	today = datetime.datetime.today()
	y = today.weekday()
	dormi, when = message.split(" ")
	when = menu_list[when]
	return_data = ""
	return_data += "[{}/{}/{} 식단]\n".format(today.year,today.month, today.day)
	if when in "012":	# 아점저 중에 있을 경우
		when = str(y)+when
		return_data += Food.objects.get(dormi=dormi,when=when).menu
		return return_data
	elif when == "3":	#오늘 전체 메뉴
		for i in range(0,3):
			return_data += Food.objects.get(dormi=dormi,when=str(y)+str(i)).menu +"\n"
		return return_data
	else: #내일 전체 메뉴
		if y == 5: # 토요일일때
			for i in range(0,3):
				return_data += Food.objects.get(dormi=dormi,when="9"+str(i)).menu +"\n"
		else:
			for i in range(0,3):
				return_data += Food.objects.get(dormi=dormi,when=str((y+1)%7)+str(i)).menu +"\n"
		return return_data
			



