#-*- coding: utf-8 -*-
#Need python3, flask
"""
bot.py
flask를 사용하여 웹서버를 구동하는 코드

작  성 : 정보보호학과 15학번 임재연
"""
############Module import############
import json

from flask import Flask, request, jsonify
############Module import############
import mnu_func as fu

app = Flask(__name__)

firstMenu = ["식단표", "인트라넷"] # 초기 메뉴설정 부분
dormiMenu = ["기존관 식단","BTL 식단"]
BTLMenu = ["BTL 아침","BTL 점심","BTL 저녁","BTL 오늘","BTL 내일"]
foodMenu = ["기존관 아침","기존관 점심","기존관 저녁","기존관 오늘","기존관 내일"]

"""
# example for fu.send_text()

def send_text(text,menu):
	data = {'message':{},keyboard:{}}
	data['message']['text'] = text
	data['keyboard']['type']='buttons'
	data['keyboard']['buttons']=menu
	return json.dumps(data,ensure_ascii=False)
"""

@app.route("//message", methods=['GET', 'POST'])
@app.route("/message", methods=['GET', 'POST'])
#메시지 처리부분



def message():
  userRequest = json.loads(request.get_data().decode())
  print(userRequest['user_key']+" - "+userRequest['content'])
  if userRequest['type'] != "text": #메시지의 타입이 텍스트일 경우
    fu.save_pic(userRequest)
    return fu.send_text("지원하지 않는 기능입니다..",firstMenu)
### 식단표
  elif userRequest['content'] == "식단표":
    return fu.send_text("기존관, BTL을 선택해 주세요",dormiMenu)
  elif userRequest['content'] == "기존관 식단":
    return fu.send_text("확인하고자 하는 메뉴를 선택해주세요.",foodMenu)
  elif userRequest['content'] == "BTL 식단":
    return fu.send_text("기존관, BTL을 선택해 주세요",BTLMenu)
  elif userRequest['content'] in BTLMenu:
    return fu.send_menu(userRequest,"_btl")
  elif userRequest['content'] in foodMenu:
    return fu.send_menu(userRequest,"")
### 식단표 끝


  elif userRequest['content'] == "인트라넷":
    return fu.send_link("목포대학교 모바일 인트라넷 페이지 입니다.","http://www.mokpo.ac.kr/groups/www/images/common/h_logo.png",\
      "200","45","목포대학교 인트라넷","http://intra.mokpo.ac.kr:7777/mobile/Login.htm",firstMenu)
  else:
    return fu.send_text("지원하지 않는 기능입니다..",firstMenu)



@app.route("//keyboard", methods=['GET', 'POST'])
@app.route("/keyboard", methods=['GET', 'POST'])
def key():
  return """{ "type" : "buttons", "buttons" : """+'["'+'","'.join(firstMenu)+'"]'+"""}"""

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=80, threaded=True)
