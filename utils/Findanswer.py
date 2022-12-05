from utils.Database import Database
from config.State import State


class FindAnswer:
    
    # Database 인스턴스 객체로 생성
    def __init__(self, db):
        self.db = db


    def select_state(self, user_id):
        sql = 'SELECT * FROM members WHERE id=%s' % user_id
        print("sql:",  sql)
        return self.db.select_one(sql)


    def update_state(self, user_id, state):
        # SQL
        sql='''
            UPDATE members set m_state=%d WHERE id=%s
        ''' % (state, user_id)
        print("sql:", sql)

        # 쿼리 실행
        with self.db.cursor() as cursor:
            result = cursor.execute(sql)
            # DML의 execute() return값은 몇 개의 행을 변경했는지에 대한 총 count (정수)임
        print(result, '개 row update 성공!')

    # 답변 검색
    def search(self, intent_name=None, ner_tags=None):
        print("search까지 들어왔따")
        # 의도명, 개체명으로 답변 검색
        sql = self._make_query(intent_1=intent_name, ner_tags=ner_tags)
        answer = self.db.select_one(sql)
        print("답변 테이블 :", answer)
        print("❤intent_name:", intent_name)
        print("🧡ner_tags:", ner_tags)
        print("💛sql:", sql)
        print("💚answer:", answer)

        if intent_name == "리스트불러오기":
            sql = self.call_list(intent_name, None)
            answer = self.db.select_one(sql)

        # 검색되는 답변이 없으면 의도명만 검색
        elif answer is None:
            sql = self._make_query(intent_name, None)
            answer = self.db.select_one(sql)

        return (answer['answer'], answer['answer_contents'])

    # 답변 검색
    def reco_search(self, intent_1=None, intent_2=None, ner_tags=None):

        # 추천 2번문제 ~ 4번 문제
        if intent_1 == None:
            # locations 담을 리스트 변수 선언
            location_li = []
            sql = self._make_query(intent_1=None, intent_2=intent_2)
            answer = self.db.select_one(sql)

            # 추천 답변
            if intent_2 == 4:
                # location DB 검색 SQL
                print("State.q:", State.q)
                sql_table = self._make_location(State.q)
                print("sql_table:", sql_table)
                answer_locations = self.db.select_all(sql_table)

                # answer_locations type : dict in list
                for loca in answer_locations:
                    location_li.append([loca['metro'], loca['location']])

            return (answer['answer'], location_li)

        # 1번 문제
        sql = self._make_query(intent_1, intent_2)
        answer = self.db.select_one(sql)

        # print("FindAnswer sql:", sql)
        # print("FindAnswer answer:", answer)

        return (answer['answer'], answer['answer_contents'])
        
    
    # 검색 쿼리 생성
    def _make_query(self, intent_1=None, intent_2=None, ner_tags=None):
        sql = "select * from answer"
        
        # 추천 1번 문제
        if intent_1 != None and intent_2 != None and ner_tags == None:
            sql = sql + " where intent_1 ='{}' and intent_2='{}' ".format(intent_1, intent_2)
            print("_make_query sql:", sql)

        # 추천 2번 문제 ~ 4번 문제
        elif intent_1 == None and intent_2 != None and ner_tags == None:
            sql = sql + " where intent_2='{}' ".format(intent_2)
            print("_make_query sql:", sql)

        # intent_name 만 주어진 경우
        elif intent_1 != None and intent_2 != None and ner_tags == None:
            pass

        # 도움말, 리스트뽑기, 리스트 삭제
        elif intent_1 != None and intent_2 == None and ner_tags == None:
            print('make_query:', intent_1)
            sql = sql + " where intent_1='{}' ".format(intent_1)
            print("_make_query sql:", sql)
            return sql

        # intent_name 과 개체명도 주어진 경우
        elif intent_1 != None and ner_tags != None:
            where = ' where intent_1="%s" ' % intent_1

            if intent_1 == '길찾기':
                where += " ner like '%{}%' or ".format(ner_tags[1])
                where = where[:-3] + ')'

            elif (len(ner_tags) > 0):
                where += 'and ('
                for ne in ner_tags:
                    where += " ner like '%{}%' or ".format(ne)
                where = where[:-3] + ')'

            sql = sql + where
            print("_make_query sql:", sql)

        # 동일한 답변이 2개 이상인 경우, 랜덤으로 선택
        sql = sql + " order by rand() limit 1"

        return sql        
    
    def _make_location(self, q):
        sql = "select * from location"
        sql += " where q = '{}' ".format(q)
        sql += " order by rand() limit 3"
        return sql

    # NER 태그를 실제 입력된 단어로 변환
    def tag_to_word(self, ner_predicts, answer):
        loc_list=[]

        for word, tag in ner_predicts:
            if "가는 길" in answer:
                loc_list.append(word)
            # 변환해야하는 태그가 있는 경우 추가
            elif tag == 'B_location' or tag == 'B_highway':
                answer = answer.replace(tag, word)  # 태그를 입력된 단어로 변환
        
        if "가는 길" in answer:
            answer = answer.replace("B_location", loc_list[1])
            print('loc_list: ',loc_list)
            print('loc_list[1]: ',loc_list[1])
            print('answer: 희지희즈히지흐지희짖 ',answer)
        answer = answer.replace('{', '')
        answer = answer.replace('}', '')
        
        print("tag_to_word answer : ", answer)

        return answer

    # 리스트 불러오기 쿼리문 생성
    def call_list(self, intent_1=None, intent_2=None, ner_tags=None):
        sql = "select * from member_location where m_idx = 1;"
        return sql

    # 리스트 삭제하기 쿼리문 생성
    def call_delete(self, intent_1=None, intent_2=None, ner_tags=None):
        sql = "DELETE FROM member_location WHERE m_idx = 1 AND location_list = '경기도';"
        return sql


    # 추천 태그 없애기
    def reco_to_word(self, reconame, answer):

        if reconame == '차':
            answer = answer.replace('way', reconame)
        if reconame=='뚜벅이':
            answer = "걷는 거 좋지! 어느 계절에 여행갈 계획이야?"
        elif reconame == '봄' or reconame == '여름' or reconame == '가을' or reconame == '겨울':
            answer = answer.replace('season', reconame)
        if reconame == '도시' or reconame == '자연':
            answer = answer.replace('city_nature', reconame)
        
        answer = answer.replace('{', '')
        answer = answer.replace('}', '')
        
        print("reco_to_word answer : ", answer)

        return answer