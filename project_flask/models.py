from matplotlib.pyplot import get
import numpy as np 
import pandas as pd
from sklearn.decomposition import TruncatedSVD
from website import init




#데이터 호출함수=> 추후 DB 에서 호출하게끔 개선하기
def get_data():
    db = init.connect_db()
    
    #rating_data -> /Users/jungry/Desktop/bigdata/jshwebtoon/data/csv/after_pre/total_survey_221129_2.csv
    rating_data = pd.read_csv('/Users/jungry/Desktop/bigdata/jshwebtoon/data/csv/after_pre/total_survey_221129_2.csv')
    webtoon_data= pd.read_csv('/Users/jungry/Desktop/bigdata/jshwebtoon/data/csv/after_pre/webtoon_preprocessing_221219.csv')
    
    return rating_data,webtoon_data

# -정구리- 협업필터링
#데이터 전처리
def preprocessing_data(rating_data,webtoon_data):
    #webtoon_title -> title (for merge)
    rating_data = rating_data.rename(columns={'webtoon_title':'title'})
    #필요없는 데이터들 drop
    webtoon_data.drop(['likes','fake_intro','real_intro','first_register_date','last_register_date','author','status','episodes','age','rate'],axis=1,inplace=True)

    #merge, drop
    usr_webtoon_data = pd.merge(rating_data,webtoon_data,on="title")
    usr_webtoon_data = usr_webtoon_data.drop(['webtoon_num','genre1_pre','genre2_pre'],axis=1)

    #make pivot
    usr_webtoon_pivot = usr_webtoon_data.pivot_table('webtoon_ratings',index="user",columns='title')

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
    rating_data,webtoon_data = get_data()
    corr,webtoon_title = truncateSVD(rating_data,webtoon_data)
    webtoon_title_list = list(webtoon_title)
    target = webtoon_title_list.index(title)
    corr_target = corr[target]
    result = list(webtoon_title[(corr_target>=0.80)])[:200]

    return result
    



def main():
    
    result = recommand_webtoon('가비지타임')


if __name__ =='__main__':
    main()


