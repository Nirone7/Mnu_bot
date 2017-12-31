"""
views.py

사용자로부터 받은 요청을 처리하는 부분
urls.py에서 요청에 따라 기능들이 실행된다.

작  성  :  정보보호학과 15학번 임재연

"""


from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .additional import function_call, save_media
from .models import *
#from .forms import *
import datetime
# Create your views here.


"""
함수명 :  keyboard
가장 처음 사용자가 카카오톡 채팅방에 접속했을때 초기 화면에 관한 부분이다.
아래 함수에서는 초기메뉴를 호출한다.
"""
def keyboard(request):
	key = Keyboard.objects.get(name='초기메뉴')		#데이터베이스에서 초기메뉴의 값을 가져온다.
	data = key.Get_keyboard()		# keyboard 객체에서 json 형식으로 만들어진 값을 반환받는다.
	return HttpResponse(data) # 반환값 : {"buttons": ["식단표", "인트라넷", "도움말"], "type": "buttons"}


"""
함수명 : message
사용자로부터 메시지를 받고 응답값을 정해 반환해준다.
"""
@csrf_exempt	# csrf 토큰이 없어도 정상적으로 요청을 처리할 수 있게 해준다.
def message(request):
	userRequest = json.loads(request.body.decode())	#사용자의 메시지를 가져온다.
	if userRequest['type'] != "text":	# 메시지의 타입을 검사하여 text가 아니면 미디어이므로 해당 미디어를 저장한다.
		try:
			save_media(userRequest)	#additional.py에 있는 함수로 사용자의 요청으로부터 미디어를 추출하여 저장한다.
		except:
			pass
	try:
		message = Message.objects.get(request=userRequest['content'])	#사용자가 입력한 메시지를 DB에서 검색한다.
	except:
		message = Message.objects.get(request="실패")	#조회에 실패한경우에는 해당 메시지를 찾을 수 없다는 메시지를 반환한다.
	if "function_call" in message.text:	#응답값의 텍스트부분에 function_call이라는 문자열이 있으면 확장 모듈로 넘긴다.
		message.text = function_call(message.text) #메시지의 텍스트를 함수를 실행한 반환값으로 바꾼다.
	data = message.Get_message() #json형식으로 변환후 return 해준다.
	
	return HttpResponse(data)

