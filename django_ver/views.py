from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import CreateView, UpdateView,FormView
import json
from .additional import function_call, save_media
from .models import *
from .forms import *
import datetime

def keyboard(request):
	key = Keyboard.objects.get(name='초기메뉴')
	data = key.Get_keyboard()
	return HttpResponse(data)

@csrf_exempt
def message(request):
	userRequest = json.loads(request.body.decode())
	if userRequest['type'] != "text":
		try:
			save_media(userRequest)
		except:
			pass
	try:
		message = Message.objects.get(request=userRequest['content'])
	except:
		message = Message.objects.get(request="실패")
	if "function_call" in message.text:
		print("function_call excuted")
		message.text = function_call(message.text)
	data = message.Get_message()
	
	return HttpResponse(data)

