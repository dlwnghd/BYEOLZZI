from utils.Database import Database

class Findlocation:
    
    # Database 인스턴스 객체로 생성
    def __init__(self, db):
        self.db = db

    def select_location(self, user_id):
        sql = 'SELECT m_location FROM members WHERE id=%s' % user_id
        print("sql:",  sql)
        user_loca = self.db.select_one(sql)
        print("user_loca:" , user_loca)
        print("user_loca['m_location']:" , user_loca['m_location'])
        return user_loca['m_location']