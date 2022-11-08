import tensorflow as tf
from tensorflow.keras.models import Model, load_model
from tensorflow.keras import preprocessing


# 의도 분류 모델 모듈
class IntentModel:
    def __init__(self, model_name, preprocess):

        # 의도 클래스 별 레이블
        self.labels = {0: "추천", 1: "길찾기", 2: "날씨", 3: "교통현황", 
                       4: "축제", 5:"여행지정보", 6:'주변검색', 7:'리스트불러오기',
                      8:'리스트삭제', 9:'인사', 10:'도움말',
                       11:'챗봇종료', 12: '기타'}

        # 의도 분류 모델 불러오기
        self.model = load_model(model_name)

        # 챗봇 Preprocess 객체
        self.p = preprocess


    # 의도 클래스 예측
    def predict_class(self, query):
        # 형태소 분석
        pos = self.p.pos(query)

        # 문장내 키워드 추출(불용어 제거)
        keywords = self.p.get_keywords(pos, without_tag=True)
        sequences = [self.p.get_wordidx_sequence(keywords)]

        # 단어 시퀀스 벡터 크기
#         from config.GlobalParams import MAX_SEQ_LEN
        MAX_SEQ_LEN = 20

        # 패딩처리
        padded_seqs = preprocessing.sequence.pad_sequences(sequences, maxlen=MAX_SEQ_LEN, padding='post')

        predict = self.model.predict(padded_seqs)
#         print(predict)
        print('====================================')
        if max(predict[0]) < 0.4:
            predict_class = 12
            return predict_class
        else:
            predict_class = tf.math.argmax(predict, axis=1)
            return predict_class.numpy()[0]


