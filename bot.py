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
from utils.Findlocation import Findlocation

from django.http import HttpRequest

from module.Around import Around
from module.highway_heeji import Highway
from module.festival import festival
from module.Weather import Weather_crawl
from module.FindTag import FindTag
from config.help import help


# 전처리 객체 생성
p_full = Preprocess(
    word2index_dic = 'train_tools/dict/intent1_dict_20221120.bin',
    userdic = 'utils/user_dic.tsv'
)
p_car_walk = Preprocess(
    word2index_dic = 'train_tools/dict/chatbot_dict_car.bin',
    userdic = 'utils/user_dic.tsv'
)
p_season = Preprocess(
    word2index_dic = 'train_tools/dict/season_dict_20221119.bin',
    userdic = 'utils/user_dic.tsv'
)
p_city = Preprocess(
    word2index_dic = 'train_tools/dict/citynature_dict_221120.bin',
    userdic = 'utils/user_dic.tsv'
)
p_activity = Preprocess(
    word2index_dic = 'train_tools/dict/activity_dict_bilstm_221119.bin',
    userdic = 'utils/user_dic.tsv'
)
p_null = Preprocess(
    word2index_dic = 'train_tools/dict/chatbot_dict_full.bin',
    userdic = 'utils/user_dic.tsv'
)

# 의도 파악 모델 (1)
intent = IntentModel(model_name='models/intent/Epoch_046_Val_0.010.h5', preprocess=p_full)

# 의도 파악 모델 (2) : car/walk
intent_car_walk = IntentModel_Car_Walk(model_name='models/intent/221122_intent_car_walk_model.h5', preprocess=p_car_walk)

# 의도 파악 모델 (2) : season
intent_season = IntentModel_Season(model_name='models/intent/intent_model_season_221120.h5', preprocess=p_season)

# 의도 파악 모델 (2) : city/nature
intent_city = IntentModel_City(model_name='models/intent/intent_model_citynature_cnn_221120.h5', preprocess=p_city)

# 의도 파악 모델 (2) : activity
intent_activity = IntentModel_Activity(model_name='models/intent/intent_model_activity_bilstm_221120.h5', preprocess=p_activity)

# 개체명 인식 모델
ner = NerModel(model_name='models/ner/ner_model.h5', preprocess=p_null)

# 클라이언트 요청을 수행하는 쓰레드(에 담을) 함수
def to_client(conn, addr, params):
    db = params['db']

    try:
        db.connect()
        intent_name = None
        intent_reco = None
        intent_reco_name = None
        ner_predicts = None
        ner_tags = None
        met_code=None
        loc_code=None
        ner_list = []
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
        recv_location = recv_json_data['User_Location']    # 클라이언트로부터 전송된 질의어
        print("recv_location:", recv_location)


        #=================================
        # decode: (encoding: str = ..., errors: str = ...) -> str
        # Decode the bytes using the codec registered for encoding.

        # encoding
        # The encoding with which to decode the bytes.
        #=================================

        if recv_location != None:
            State.user_location = recv_location
            print("State.user_location:", State.user_location)
        # user_idx = request.session['login']

        # # 유저 DB에 저장된 location 불러오기
        # fl = Findlocation(db)
        # State.user_location = fl.select_location(user_idx)

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
            ner_predicts = ner.predict(query)
            print("ner_predicts:", ner_predicts)
            ner_tags = ner.predict_tags(query)
            for ne in ner_predicts:
                if ne[1] != 'O':
                    ner_list.append(ne[0])
        
            print("😢😢State.user_location:", State.user_location)
            print("😢😢ner_predicts:", ner_predicts)
            print("😢😢ner_tags:", ner_tags)
            print("😢😢ner_list:", ner_list)

            if intent_name == "길찾기":
                # count = 0
                fw_list = []
                for loc in ner_list:
                    # 몇개 들어왔니?
                    if loc in FindTag().location:
                        # count+=1
                        fw_list.append(loc)
                if len(fw_list) == 1:       # 여행지 변수가 있다는 얘기
                    fw_list.append(State.user_location)
                    ner_list = fw_list
                    print('ner_list 개수 : ', ner_list)
                    ner_predicts = [ner_predicts[0], (State.user_location, 'B_location')]

                    ner_tags.append("B_location")
                    print("ner_predicts : ", ner_predicts)
                    print("ner_list:" , ner_list)
            elif len(ner_list) and ner_list[0] in FindTag().location:
                pass
            elif intent_name in ["교통현황", "리스트 불러오기", "인사", "도움말", "챗봇종료", "기타"]:
                pass
                    
            else:
                fw_list = []
                for loc in ner_list:
                    # 몇개 들어왔니?
                    if loc in FindTag().location:
                        fw_list.append(loc)
                if len(fw_list) == 0:       # 여행지 변수가 있다는 얘기
                    fw_list.append(State.user_location)
                    ner_list = fw_list
                    
                    ner_predicts = [(State.user_location, 'B_location')]
                    
                    ner_tags = []
                    ner_tags.append("B_location")
                    
                    print("ner_predicts : ", ner_predicts)
                    print("ner_list:" , ner_list)

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
                print('ner_tags 너 몇개양? ', ner_tags)
                answer_text, answer_contents = f.search(intent_name, ner_tags)
                

                if intent_name == '교통현황':
                    # if len(ner_list) ==1:
                    if len(ner_list):
                        if ner_list[0] in FindTag().highway:
                            way = Highway(ner_list[0])
                            print('희지 교통현황 들어옴')
                            print('ner_list: ',ner_list)
                            answer_contents = way.bot_sum()
                            print('answer_contents: ',answer_contents)
                        else:
                            raise Exception('희지오류났어용!!!!!!!!!!!!!!!')
                    else:
                        raise Exception('희지오류났어용!!!!!!!!!!!!!!!---1')
                    
                elif intent_name == "주변검색":
                    print('ㅠㅠㅠㅠㅠㅠㅠ')
                    if len(ner_list):
                        print("주변검색_ner_list:", ner_list)
                        print("주변검색_ner_list[0]:", ner_list[0])
                        if ner_list[0] in FindTag().location:
                            print('여기인가요??')
                            answer_contents = Around(db).search_around(ner_list[0])
                        else:
                            raise Exception('희지오류났어용!!!!!!!!!!!!!!!22222222222')
                    else:
                        raise Exception('희지오류났어용!!!!!!!!!!!!!!!22222222222-1')

                elif intent_name=="축제":     
                    if len(ner_list):
                        print("축제_ner_list:", ner_list)
                        print("축제_ner_list[0]:", ner_list[0])
                        if ner_list[0] in FindTag().location:  
                            print("전범수 :",ner_list[0])
                            answer_contents=festival(db).fes_sum(ner_list[0])
                            print('크롤링 :', answer_contents)
                            try:
                                met_code=answer_contents[0]['met_code']
                                loc_code=answer_contents[0]['loc_code']
                            except:
                                met_code=None
                                loc_code=None
                                answer = answer_contents
                                print("에러 답변이요 :",answer)
                                answer_contents = ""
                                print("열리는 축제 없음")
                        else:
                            raise Exception('희지오류났어용!!!!!!!!!!!!!!!3333333333')
                    else:
                        raise Exception('희지오류났어용!!!!!!!!!!!!!!!3333333333-1')

                elif intent_name=="날씨":
                    if len(ner_list):
                        if ner_list[0] in FindTag().location:
                            answer_contents = Weather_crawl().weather(ner_list[0])
                        else:
                            raise Exception('희지오류났어용!!!!!!!!!!!!!!!4444444444')
                    else:
                        raise Exception('희지오류났어용!!!!!!!!!!!!!!!4444444444----1')

                elif intent_name== "여행지정보":
                    if len(ner_list):
                        if ner_list[0] in FindTag().location:
                            pass
                        else:
                            raise Exception('희지오류났어용!!!!!!!!!!!!!!!555555555555')
                    else:
                        raise Exception('희지오류났어용!!!!!!!!!!!!!!!55555555555----1')
                
                elif intent_name=="길찾기":
                    if 1 <= len(ner_list) and  len(ner_list) <=2 :
                        if len(ner_list) <=2:
                            for ner_name in ner_list:
                                if ner_name in FindTag().location:
                                    pass
                                else:
                                    raise Exception('희지오류났어용!!!!!!!!!!!!!!66666666')
                    else:
                        raise Exception('희지오류났어용!!!!!!!!!!!!!!66666666 ----1')

                elif intent_name=="도움말" or intent_name=='기타':
                    answer_contents = help.help_comment

                elif intent_name=="리스트 불러오기":
                    pass

            # 최종 결과 확인
            print("END_Answer_text :", answer_text)
            print("END_Answer_contents :", answer_contents)


            # BIO 태그 개체명으로 변경
            if ner_predicts != None:
                print("여기임?")
                answer = f.tag_to_word(ner_predicts, answer_text)
            else:
                answer = answer_text
            print(type(answer))

            # 추천 State 작업
            if State.state != None and State.state != 4:
                answer = f.reco_to_word(intent_reco_name, answer)
                State.state += 1
            elif State.state == 4:
                State.state = None
                State.q = None

        # 의도분류 인식 오류
        except Exception as e:
            print(e)
            answer = "죄송해요 무슨 말인지 모르겠어요. 조금 더 공부 할게요."
            answer_contents = None

        # WEB Client 전송 데이터 (JSON)
        sent_json_data_str = {    # response 할 JSON 데이터를 준비할 겁니다~
            "Query" : query,
            "Answer": answer,
            "AnswerContents" : answer_contents,
            "Intent": intent_name,
            "IntentReco" : intent_reco_name,
            "NER": str(ner_predicts),
            "NerTags": ner_tags,
            "NerList" : ner_list,
            "met_code" : met_code,
            "loc_code" : loc_code
        }

        # JSON 변환 및 출력 확인
        message = json.dumps(sent_json_data_str)
        print("=++++++++++++++++++")
        print("message type:",type(message))
        print(message)
        print("=++++++++++++++++++")
        
        # 데이터 전송
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





