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
        # 의도명, 개체명으로 답변 검색
        sql = self._make_query(intent_1=intent_name, ner_tags=ner_tags)
        answer = self.db.select_one(sql)

        print("✅intent_name:", intent_name)
        print("✅ner_tags:", ner_tags)
        print("sql:", sql)
        print("answer:", answer)

        # 검색되는 답변이 없으면 의도명만 검색
        if answer is None:
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
    
        # 의도명, 개체명으로 답변 검색
        # sql = self._make_query(intent_1, intent_2, ner_tags)
        # answer = self.db.select_one(sql)

        print("FindAnswer sql:", sql)
        print("FindAnswer answer:", answer)

        # 검색되는 답변이 없으면 의도명만 검색
        # if answer is None:
        #     sql = self._make_query(intent_1, intent_2, None)
        #     answer = self.db.select_one(sql)

        # return (answer['answer'], answer['answer_image'])
        return (answer['answer'], answer['answer_contents'])
        
    
    # 검색 쿼리 생성
    def _make_query(self, intent_1=None, intent_2=None, ner_tags=None):
        sql = "select * from answer"
        
        # 추천 1번 문제
        if intent_1 != None and intent_2 != None and ner_tags == None:
            sql = sql + " where intent_1 ='{}'".format(intent_1)
            print("❤️intent_1:",intent_1)
            print("🧡intent_2:",intent_2)
            print("🧡ner_tags:",ner_tags)
            print("_make_query sql:", sql)

        # 추천 2번 문제 ~ 4번 문제
        elif intent_1 == None and intent_2 != None and ner_tags == None:
            print("💛intent_1:",intent_1)
            print("💚intent_2:",intent_2)
            sql = sql + " where intent_2='{}' ".format(intent_2)
            print("_make_query sql:", sql)

        # intent_name 만 주어진 경우
        elif intent_1 != None and intent_2 != None and ner_tags == None:
            pass

        # 도움말, 리스트뽑기, 리스트 삭제
        elif intent_1 != None and intent_2 == None and ner_tags == None:
            sql = sql + " where intent_1='{}' ".format(intent_1)
            print("_make_query sql:", sql)

        # intent_name 과 개체명도 주어진 경우
        elif intent_1 != None and ner_tags != None:
            print("💙intent_1:",intent_1)
            print("💜ner_tags:",ner_tags)
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
            print("ner_tags:", ner_tags)

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
        print("================")
        print(ner_predicts)
        print(ner_predicts[1][0])
        print(answer)
        print("================")
        loc_list=[]

        print("함수 안의 loc_list : ", loc_list)

        for word, tag in ner_predicts:
            
            # 변환해야하는 태그가 있는 경우 추가
            if "길 안내" in answer and tag == 'B_location':
                loc_list.append(word)
            elif tag == 'B_location' or tag == 'B_highway':
                answer = answer.replace(tag, word)  # 태그를 입력된 단어로 변환
                
        if "길 안내" in answer:
            answer = answer.replace("B_location", loc_list[1])
        
        print("loc_list : ", loc_list)
        
        answer = answer.replace('{', '')
        answer = answer.replace('}', '')

        print("tag_to_word answer : ", answer)

        return answer