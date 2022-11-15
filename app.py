from flask import Flask, request, jsonify, abort
import socket
import json


# 챗봇 엔진 서버 접속 정보
# 이전에 만든 챗봇 엔진 서버에서 설정한 포트를 사용해야 한다
host = "127.0.0.1"  # 챗봇 엔진 서버 IP 주소
port = 5050  # 챗봇 엔진 서버 통신 포트

# Flask 어플리케이션
app = Flask(__name__)

from flask_cors import CORS
CORS(app)

# 챗봇 엔진 서버와 통신 (소켓 통신!)
# 질의를 전송하고, 답변데이터를 수신한 경우 JSON 문자열을 dict 객체로 변환
def get_answer_from_engine(bottype, query, location):    
        # 챗봇 엔진 서버 연결
    mySocket = socket.socket()
    mySocket.connect((host, port))            #서버를 요청 해당 주소쪽으로~

    # 챗봇 엔진 질의 요청
    json_data = {                              # 해당 서버로 보낼거~~~~우리 서버(api서버말고)
        'Query': query,
        'User_Location': location,
        'BotType': bottype,
    }
    print("json_data:", json_data)
    message = json.dumps(json_data)
    mySocket.send(message.encode())

    # 챗봇 엔진 답변 출력
    data = mySocket.recv(40560).decode()
    ret_data = json.loads(data)
    print("ret_data :", ret_data)

    # 챗봇 엔진 서버 연결 소켓 닫기
    mySocket.close()

    return ret_data



@app.route("/", methods=['GET'])
def index():
    return ('hello')

#챗봇 엔진 query 전송 API
@app.route("/query/<bot_type>", methods=['POST'])
def query(bot_type):

    body = request.get_json()
    ret = {}
    try:
        if bot_type == 'TEST':
            # TODO: 챗봇엔진에 소켓통신하여 query 를 보내고 답을 받아오기
            ret = get_answer_from_engine(bottype=bot_type, query=body['query'], location=body['user_location'])
            print("ret: ", ret, "type: ", type(ret))
            return jsonify(ret)
        elif bot_type =="KAKAO":
            #카카오 처리
            pass
        elif bot_type == "NAVER":
            # 네이버톡 처리
            pass
        else:
            # 정의되지 않은 boy type의 경우 404 에러
            abort(404)

    except Exception as ex:
        # 오류 발생시 500에러
        abort(500)    

if __name__ == "__main__":
    app.run(host='127.0.0.10', port=5000, debug=True)