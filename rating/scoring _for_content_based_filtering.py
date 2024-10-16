import pandas as pd
import warnings
warnings.filterwarnings('ignore')

# Load data
def load_data(file_path):
    return pd.read_csv(file_path, index_col=0)

# Split data by taste
def split_data_by_taste(review_df):
    taste_dfs = {}
    taste_keywords = {
       'spicy': ['맵', '매운', '매워', '매웠', '매움', '맵찔', '맵싹', '맵칼', '화끈', '얼큰', '맵콤', '메콤', '매운', '매콤', '얼얼', '신라면보다는', '자극'],
       'sweet': ['달달', '달콤', '달짝', '달착', '달큰', '단짠', '맵달'],
       'salty': ['짠', '짭짤', '짭잘', '간간', '짭조', '짭쪼', '단짠', '자극', '짜요', '짜고', '짜네', '짰'],
       'sour': ['새콤', '시큼', '상큼', '산미'],
       'soft': ['담백', '고소', '구수', '깔끔', '개운', '진국', '뽀얗', '우러', '진한', '찐한', '깊', '깊고']
    }

    for taste, keywords in taste_keywords.items():
        taste_df = review_df[review_df['content'].str.contains('|'.join(keywords))]
        taste_df = taste_df[~taste_df['content'].str.contains('안' + taste)]
        taste_dfs[taste] = taste_df

    return taste_dfs

# Group by valcount and add z-score
def process_review_df(review_df, name):
    test = groupby_valcount(review_df)
    score_df = add_z_score(test)
    score_df.columns = ['-1', '1', f'{name}_score']
    score_df = score_df[[f'{name}_score']]
    return score_df

def groupby_valcount(review_df):
    polarity_list = []
    for polarity in review_df.polarity.to_list():
        polarity_list.extend(eval(polarity))

    review_df_2 = review_df.drop(columns='polarity')
    review_df_2['polarity'] = polarity_list
    valcount_by_bizid = review_df_2.groupby('biz_id')['polarity'].value_counts().unstack().fillna(0).astype(int)
    valcount_by_bizid = valcount_by_bizid.rename(columns={0:-1}) # 부정은 극성 0으로 되어 있는데 부정 극성을 -1로

    return valcount_by_bizid

def add_z_score(df): # df: 극성별 개수가 저장된 dataframe
    s_values = {}  # 각 biz_id의 s 값을 저장할 딕셔너리
    for id, counts in df.iterrows():
        a = counts.get(1, 0)    # pol 값이 1(긍정)인 개수
        b = counts.get(-1, 0)   # pol 값이 -1(부정)인 개수
        c = counts.get(0, 0)    # pol 값이 0인 개수 // 식당별 리뷰는 0값이 없음.
        n = a + b + c           # 총 개수
        if n!= 0:
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

# Merge taste dataframes
def merge_taste_dfs(taste_dfs):
    merged_df = pd.merge(taste_dfs['spicy'], taste_dfs['sweet'], on='biz_id', how='outer')
    for name in ['salty','sour','soft']:
        merged_df = pd.merge(merged_df, taste_dfs[name], on='biz_id', how='outer')
    return merged_df

# Main function
def main():
    file_path = './review_data_fin_polarity.csv'
    review_df = load_data(file_path)
    taste_dfs = split_data_by_taste(review_df)
    taste_dfs = {name: process_review_df(taste_df, name) for name, taste_df in taste_dfs.items()}
    for name, taste_df in taste_dfs.items():
        taste_df = taste_df.reset_index()
        taste_dfs[name] = taste_df
    merged_df = merge_taste_dfs(taste_dfs)
    merged_df.to_csv('./restaurant_taste_scores.csv')

if __name__ == '__main__':
    main()