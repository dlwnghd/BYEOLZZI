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
from config.State import State
from utils.Database import Database
from utils.Botserver import BotServer
from utils.Preprocess import Preprocess
from models.intent.IntentModel import IntentModel
from models.intent.IntentModel_season import IntentModel_Season
from models.intent.IntentModel_car_walk import IntentModel_Car_Walk
from models.intent.IntentModel_city import IntentModel_City
from models.intent.IntentModel_activity import IntentModel_Activity
from models.ner.NerModel import NerModel
from utils.Findanswer import FindAnswer

# 전처리 객체 생성
p_full = Preprocess(word2index_dic='train_tools/dict/chatbot_dict_full.bin',
               userdic='utils/user_dic.tsv')
p_car_walk = Preprocess(word2index_dic='train_tools/dict/chatbot_dict_car_walk.bin',
               userdic='utils/user_dic.tsv')
p_season = Preprocess(word2index_dic='train_tools/dict/chatbot_dict_season.bin',
               userdic='utils/user_dic.tsv')
p_city = Preprocess(word2index_dic='train_tools/dict/chatbot_dict_city.bin',
               userdic='utils/user_dic.tsv')
p_activity = Preprocess(word2index_dic='train_tools/dict/chatbot_dict_activity.bin',
               userdic='utils/user_dic.tsv')

# 의도 파악 모델 (1)
intent = IntentModel(model_name='models/intent/intent_model_test_full.h5', preprocess=p_full)

# 의도 파악 모델 (2) : car/walk
intent_car_walk = IntentModel_Car_Walk(model_name='models/intent/intent_model_car_walk.h5', preprocess=p_car_walk)

# 의도 파악 모델 (2) : season
intent_season = IntentModel_Season(model_name='models/intent/intent_model_season.h5', preprocess=p_season)

# 의도 파악 모델 (2) : city/nature
intent_city = IntentModel_City(model_name='models/intent/intent_model_city.h5', preprocess=p_city)

# 의도 파악 모델 (2) : activity
intent_activity = IntentModel_Activity(model_name='models/intent/intent_model_activity.h5', preprocess=p_activity)

# 개체명 인식 모델
ner = NerModel(model_name='models/ner/ner_model.h5', preprocess=p_full)

# 클라이언트 요청을 수행하는 쓰레드(에 담을) 함수
def to_client(conn, addr, params):
    db = params['db']

    try:
        db.connect()
        intent_name = None
        intent_reco = None
        intent_reco_name = None
        ner_predicts = None
        print("Start_State.state:", State.state)

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
        if State.state == None:
            intent_predict = intent.predict_class(query)
            intent_name = intent.labels[intent_predict]

            if intent_name == '추천':
                print("추천 의도 들어옴")
                State.state = 0

        if State.state == 0:
            pass

        elif State.state == 1:
            intent_reco = intent_car_walk.predict_class(query)
            intent_reco_name = intent_car_walk.labels[intent_reco]
            State.q = str(intent_reco)

        elif State.state == 2:
            intent_reco = intent_season.predict_class(query)
            intent_reco_name = intent_season.labels[intent_reco]
            State.q += str(intent_reco)

        elif State.state == 3:
            intent_reco = intent_city.predict_class(query)
            intent_reco_name = intent_city.labels[intent_reco]
            State.q += str(intent_reco)

        elif State.state == 4:
            intent_reco = intent_activity.predict_class(query)
            intent_reco_name = intent_activity.labels[intent_reco]
            State.q += str(intent_reco)


        # 개체명 파악
        if State.state == None:
            ner_list = []
            ner_predicts = ner.predict(query)
            ner_tags = ner.predict_tags(query)
            for ne in ner_predicts:
                if ne[1] != 'O':
                    ner_list.append(ne[0])


        # 답변 검색
        try:
            print("FindAnswer 시작")
            print("intent_name:", intent_name)
            print("intent_reco:", intent_reco)
            print("intent_reco_name:", intent_reco_name)
            print("State.state:", State.state)
            f = FindAnswer(db)
            if State.state != None:
                answer_text, answer_contents = f.reco_search(intent_name, State.state)
            else:
                answer_text, answer_contents = f.search(intent_name, ner_tags)

            print("END_Answer_text :", answer_text)
            print("END_Answer_contents :", answer_contents)
            if ner_predicts != None:
                answer = f.tag_to_word(ner_predicts, answer_text)
            else:
                answer = answer_text
            print(type(answer))

            if State.state != None and State.state != 4:
                State.state += 1
            elif State.state == 4:
                State.state = None
                State.q = None
        except Exception as e:
            print(e)
            answer = "죄송해요 무슨 말인지 모르겠어요. 조금 더 공부 할게요."
            answer_contents = None


        sent_json_data_str = {    # response 할 JSON 데이터를 준비할 겁니다~
            "Query" : query,
            "Answer": answer,
            "AnswerContents" : answer_contents,
            "Intent": intent_name,
            "IntentReco" : intent_reco_name,
            "NER": str(ner_predicts),
            "NerList" : ner_list
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





