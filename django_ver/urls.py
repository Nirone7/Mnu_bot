"""
urls.py
요청받은 url과 함수를 연결시켜주는 부분
작  성 : 정보보호학과 15학번 임재연

"""


from django.conf.urls import url
from . import views

#서버 주소/keyboard/로 요청이 들어오면 keyboard함수로 넘긴다. 
#서버 주소/message/로 요청이 들어오면 message함수로 넘긴다.
urlpatterns = [
    url(r'^keyboard/', views.keyboard),
    url(r'^message/',views.message),
]
