"""

동적으로 처리해야하는 기능들을 함수로 정의하여 기능 실행
ex) 식단표 > 오늘 아침의 식단을 조회하여 보여줘야함 등..

작  성 : 정보보호학과 15학번 임재연

"""





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

# 이미지를 저장하는 부분 , message 의 type이 text가 아니면 실행된다.
def save_media(userRequest):  #이미지 저장부분(매개변수는 전달된 요청값(콘텐츠,타입,메시지)데이터)
	user = userRequest['user_key']
	imgSrc = userRequest['content']
	imgContent = urllib2.urlopen(imgSrc).read()
	imgFileName = basename(urp.urlsplit(imgSrc)[2]).replace("../","")
	with open("/home/nirone7/JY/media/{}_".format(user)+imgFileName, 'wb') as imgFile:
		imgFile.write(imgContent)

# message 값으로 'funcuion_call(get_food,"기존관 아침")' 과 같이 전달받는다
# function_call(함수, 매개변수) 와 같이 사용하며
# 다양한 취약점이 있지만 카카오톡을 통해 접근하는 경우에는 데이터베이스에 접근이 
# 불가능 하므로 eval문자열만 막아두었다.
def function_call(message):
	foo,var = re.findall("\((.*?)\)",message)[0].split(",") # function_call(foo,var) => foo = foo, var = var
	if "eval" in foo:
		return "No hack..."
	try:
		data = eval("{}({})".format(foo,var))
		return data
	except:
		data = "정의되지 않은 기능입니다."
		return data





# 요청에 따라 데이터베이스에서 식단정보를 가져와서
#조건에 맞게 조합 후 반환해준다.
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
			



