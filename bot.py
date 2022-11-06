'''
thread : 쓰레드
리퀘스트가 들어오면 별도의 쓰레드를 활용한다

# 파이썬은 원래 기본적으로 한번에 하나의 쓰레드밖에 실행 못한다
# 'threading 모듈'을 통해 (내부적으로) 코드를 interleaving 방식으로 분할 실행함으로
# 멀티 쓰레딩 비슷(?)하게 동작시킨다.

'''
import threading
import json

from config.DatabaseConfig import *   # 임포트는 함수 변수 클래스
from utils.Database import Database
from utils.Botserver import BotServer
from utils.Preprocess import Preprocess
from models.intent.IntentModel import IntentModel
from models.ner.NerModel import NerModel
from utils.Findanswer import Findanswer

# 전처리 객체 생성
p = Preprocess(word2index_dic='train_tools/dict/chatbot_dict.bin',
               userdic='utils/user_dic.tsv')

# 의도 파악 모델
intent = IntentModel(model_name='models/intent/intent_model.h5', preprocess=p)

# 개체명 인식 모델
ner = NerModel(model_name='models/ner/ner_model.h5', preprocess=p)

# 클라이언트 요청을 수행하는 쓰레드(에 담을) 함수
def to_client(conn, addr, params):
    db = params['db']

    try:
        db.connect()

        # 데이터 수신
        read = conn.recv(2048)   # 수신 데이터가 있을 때까지 블로킹(대기) / 최대 2048 버퍼에 담음
        print('===========================')
        print('Connection from: %s' % str(addr))

        if read is None or not read:
            # 클라이언트 연결이 끊어지거나, 오류가 있는 경우
            print('클라이언트 연결 끊어짐')
            exit(0)     # Thread 종료

        # json 데이터로 변환
        recv_json_data = json.loads(read.decode())   #파이썬객체로만들어주는 작업
        print("데이터 수신 : ", recv_json_data)
        query = recv_json_data['Query']    # 클라이언트로부터 전송된 질의어


        #=================================
        # decode: (encoding: str = ..., errors: str = ...) -> str
        # Decode the bytes using the codec registered for encoding.

        # encoding
        # The encoding with which to decode the bytes.
        #=================================


        # 파이썬으로 지금 클라이언트의 질의어를 받앗다? 그러면~

        # 의도 파악
        intent_predict = intent.predict_class(query)
        intent_name = intent.labels[intent_predict]

        # 개체명 파악
        ner_predicts = ner.predict(query)
        ner_tags = ner.predict_tags(query)

        # 답변 검색
        try:
            f = Findanswer(db)
            answer_text, answer_image = f.search(intent_name, ner_tags)
            answer = f.tag_to_word(ner_predicts, answer_text)

        except:
            answer = "죄송해요 무슨 말인지 모르겠어요. 조금 더 공부 할게요."
            answer_image = None

        sent_json_data_str = {    # response 할 JSON 데이터를 준비할 겁니다~
            "Query" : query,
            "Answer": answer,
            "AnswerImageUrl" : answer_image,
            "Intent": intent_name,
            "NER": str(ner_predicts)
        }

        message = json.dumps(sent_json_data_str)
        print("=++++++++++++++++++")
        print("message type:",type(message))
        print(message)
        print("=++++++++++++++++++")
        conn.send(message.encode())    # resoponse 


    except Exception as ex:
        print(ex)
    
    finally:
        if db is not None:
            db.close()
        conn.close()        # 응답이 끝나면 클라이언트와의 연결(클라이언트 소켓) 도 close 해야 한다.


if __name__ == '__main__':

    # 질문/답변 학습 디비 연결 객체 생성
    db = Database(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db_name=DB_NAME
    )
    print("DB 접속")


    # ① 챗봇 소켓 서버 생성
    port = 5050     # 서버의 통신포트
    listen = 100    # 최대 클라이언트 연결수

    # 봇 서버 동작
    bot = BotServer(port, listen)
    bot.create_sock()
    print('bot start')

    while True:
        conn, addr = bot.ready_for_client()   # 클라이언트가 요청이 올때까지 리스닝함(대기) 하다가 연결 수락되면~! 저 2개 리턴

        params = {
            "db": db,
        }


        # 요청이 올때마다 쓰레드 하나 보내고, 또들어오면 또보내고 또보내고.....While True (무한 루트)
        client = threading.Thread(target=to_client, args=(conn, addr, params))   # to_client로 저변수들이 넘어간다~
        client.start()     # 쓰레드 시작





