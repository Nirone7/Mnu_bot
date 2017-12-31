"""
models.py
데이터베이스에 관련된 부분들을 정의하는 부분이다.
작  성 : 정보보호학과 15학번 임재연

"""

from django.db import models
import json

# Create your models here.

class Food(models.Model):
	menu = models.TextField()
	dormi = models.CharField(max_length=3)
	when = models.CharField(max_length=2)
	def __str__(self):
		return "[{}] {}".format(self.dormi,self.when)
class User(models.Model):
	user_key = models.CharField(max_length=30)
	last_message = models.TextField()

class Keyboard(models.Model):
	name = models.CharField(max_length=30)
	button_list = models.TextField()
	keyboard_type = models.CharField(max_length=8,default="buttons")

	def __str__(self):
		return self.name
	def Set_keyboard(self, button):
		self.button_list = json.dumps(button,ensure_ascii=False)
	def Get_keyboard(self):
		data = {}
		data['type'] = "buttons"
		data['buttons'] = json.loads(self.button_list)
		return json.dumps(data,ensure_ascii=False)

class Message(models.Model):
	request = models.TextField()
	keyboard = models.ForeignKey(Keyboard)
	message_type = models.CharField(max_length=6,default='text')
	text = models.TextField()
	etc_data = models.TextField(default="{}")
	
	def __str__(self):
		return self.request

	def Set_photo(self, url, w, h):
		data =  json.loads(self.etc_data)
		data['photo']={}
		data['photo']['url'] = url
		data['photo']['width'] = int(w)
		data['photo']['height'] = int(h)
		self.etc_data = json.dumps(data,ensure_ascii=False)
	def Set_message_button(self,url,label):
		data =  json.loads(self.etc_data)
		data['message_button']={}
		data['message_button']['label'] = label
		data['message_button']['url'] = url

		self.etc_data = json.dumps(data,ensure_ascii=False)
	def Get_message(self):
		data = {"message":{}, 'keyboard':{}}
		data['message']['text'] = self.text
		data['keyboard']['type'] = self.keyboard.keyboard_type
		data['keyboard']['buttons'] = json.loads(self.keyboard.button_list)
		etc_data = json.loads(self.etc_data)
		if ("photo" in etc_data ) or ("message_button" in etc_data):
			for key in etc_data.keys():
				data['message'][key] = etc_data[key]
		return json.dumps(data,ensure_ascii=False)



