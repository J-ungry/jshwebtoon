import pandas as pd
import numpy as np
from numpy import dot
from numpy.linalg import norm
import init

#코사인 유사도
def cos_sim(A, B):
    return dot(A, B)/(norm(A)*norm(B))

def dsModel(webtoon_no):

    db=init.connect_db()
    cursor=db.cursor()

    #이미지 특징 vector select
    sql = 'select resnet from thumb'
    cursor.execute(sql)
    tup = cursor.fetchall()
    db.close()

    vec = []
    for y in range(len(tup)):
        vec.append(eval(tup[y][0]))

    #유사도 계산
    sim = []
    for x in range(0,2044):
        sim.append(cos_sim(vec[webtoon_no-1],vec[x]))

    #유사도 상위 10개 웹툰번호 return
    df = pd.DataFrame(sim, columns=['sim'])
    return df.sort_values('sim', ascending=False)[:10].index + 1



print(dsModel(1))