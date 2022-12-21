from matplotlib.pyplot import get
import numpy as np 
import pandas as pd
from sklearn.decomposition import TruncatedSVD
#from website import init

from numpy import dot
from numpy.linalg import norm
import init



def make_list(datas):
    lst = []
    for i in datas:
        lst.append(i[0])
    return lst

#데이터 호출함수=> 추후 DB 에서 호출하게끔 개선하기 (완료)
def get_data():
    db = init.connect_db()
    cursor = db.cursor()

    #webtoon_info to dataframe
    query ="select column_name from information_schema.columns where table_name='webtoon_info'"
    cursor.execute(query)
    datas = cursor.fetchall()
    column = make_list(datas)
    
    query = "select * from webtoon_info"
    cursor.execute(query)
    datas = cursor.fetchall()
    webtoon_data = pd.DataFrame(datas,columns=column)
    
    #survey to dataframe 
    query = "select column_name from information_schema.columns where table_name='survey'"
    cursor.execute(query)
    datas = cursor.fetchall()
    column = make_list(datas)

    query = "select * from survey"
    cursor.execute(query)
    datas = cursor.fetchall()
    rating_data = pd.DataFrame(datas,columns=column)
    
    return rating_data,webtoon_data

# -정구리- 협업필터링
#데이터 전처리
def preprocessing_data(rating_data,webtoon_data):
    #webtoon_no -> no (for merge)
    rating_data = rating_data.rename(columns={'webtoon_no':'no'})
    
    #필요없는 데이터들 drop
    webtoon_data.drop(['likes','fake_intro','real_intro','first_register_date','last_register_date','author','status','episodes','age','rate'],axis=1,inplace=True)

    #merge, drop (no 기준으로 merge)
    usr_webtoon_data = pd.merge(rating_data,webtoon_data,on="no")
    #drop unnecessary columns
    usr_webtoon_data = usr_webtoon_data.drop(['no','link','genre1_pre','genre2_pre'],axis=1)

    #make pivot
    usr_webtoon_pivot = usr_webtoon_data.pivot_table('score',index="user",columns='title')

    #NaN -> 0.0 SVD 동작을 위해선 Nan 형태가 있으면 안된덩 ㅋㅋ
    usr_webtoon_pivot = usr_webtoon_pivot.fillna(0)
    
    #column <-> row
    webtoon_usr_pivot = usr_webtoon_pivot.values.T
    webtoon_usr_pivot.shape

    webtoon_title = usr_webtoon_pivot.columns

    return webtoon_usr_pivot,webtoon_title

def truncateSVD(rating_data,webtoon_data):
    webtoon_usr_pivot,webtoon_title  = preprocessing_data(rating_data,webtoon_data)
    #임의의 12개의 조건 생성
    SVD = TruncatedSVD(n_components=12) 
    matrix = SVD.fit_transform(webtoon_usr_pivot)

    corr = np.corrcoef(matrix)

    return corr,webtoon_title

def recommand_webtoon(title):
    result = [] #최종 결과 들어갈 list
    rating_data,webtoon_data = get_data() #데이터 호출하기 
    corr,webtoon_title = truncateSVD(rating_data,webtoon_data) #model 에 돌리기 
    webtoon_title_list = list(webtoon_title) #웹툰 제목 호출하기
    target = webtoon_title_list.index(title) #입력받은 웹툰의 index
    corr_target = corr[target]
    
    #딕셔너리로 바꾼 뒤에 상위 5개만 출력 + 자기 자신 제외하기
    dic_corr = dict(enumerate(corr_target))
    dic_corr = list(dict(sorted(dic_corr.items(),key=lambda item:item[1],reverse=1)).keys())[:6] #6인 이유는 자기자신 제외를 위해
    for i in dic_corr:
        result.append(webtoon_title[i])
    return result[1:]
    




#재현이소스

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


def main():
    result = recommand_webtoon('마루는 강쥐')
    print(result)
    print(dsModel(1))

if __name__ =='__main__':
    main()



