import pandas as pd

def groupby_valcount(review_df):
    polarity_list = []
    for polarity in review_df.polarity.to_list():
        polarity_list.extend(eval(polarity))

    review_df_2 = review_df.drop(columns='polarity')
    review_df_2['polarity'] = polarity_list
    valcount_by_bizid = review_df_2.groupby('biz_id')['polarity'].value_counts().unstack().fillna(0).astype(int)
    valcount_by_bizid = valcount_by_bizid.rename(columns={0:-1}) # 부정은 극성 0으로 되어 있는데 부정 극성을 -1로


def add_z_score(df): # df: 극성별 개수가 저장된 dataframe
    s_values = {}  # 각 biz_id의 s 값을 저장할 딕셔너리
    for id, counts in df.iterrows():
        a = counts.get(1, 0)    # pol 값이 1(긍정)인 개수
        b = counts.get(-1, 0)   # pol 값이 -1(부정)인 개수
        c = counts.get(0, 0)    # pol 값이 0인 개수 // 식당별 리뷰는 0값이 없음.
        n = a + b + c           # 총 개수
        if n != 0:
            s = (a - b) / n     # s 값 계산
        else:
            s = 0               # n이 0인 경우 s = 0으로 설정
        s_values[id] = s    # s 값을 biz_id별로 저장

    # 전체 s 값의 최소값과 최대값 계산
    s_min = min(s_values.values())
    s_max = max(s_values.values())

    # 각 biz_id에 대해 z 값 계산 및 리스트에 저장
    z_list = []
    for id, s in s_values.items():
        # z 값 계산: (s - s_min) / (s_max - s_min) * 4 + 1
        if s_max - s_min == 0:  # s_max와 s_min이 동일할 경우 z 값 설정
            z = 1  # 모든 값이 동일한 경우 z는 1로 설정 (분모가 0이 되는 것을 방지)
        else:
            z = ((s - s_min) / (s_max - s_min)) * 4 + 1
        z_list.append(z)  # z 값을 리스트에 추가
    
    df['score'] = z_list
    return df
