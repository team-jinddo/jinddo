import pandas as pd
import numpy as np

df_path = "C:/Users/SesacPython/Desktop/final_project/sorted_res_fin_without_content.csv"
type_set_path = "C:/Users/SesacPython/Desktop/final_project/bizid_url_fin.csv"


def load_data(df_path, type_set_path):
   
    sorted_res_df = pd.read_csv(df_path, index_col=0)
    type_set = sorted(set(pd.read_csv(type_set_path, index_col=0)['res_type_filter'].to_list()))
    
    return sorted_res_df, type_set


def one_hot_encoding_type(sorted_res_df, type_set):
    # data 준비
    author_id_list = sorted_res_df.author_id.to_list()
    sorted_res_list = sorted_res_df.sorted_res.to_list()

    # unique type 가져오기
    type_list = [eval(items) for items in sorted_res_list]
    type_to_col = {t: i for i, t in enumerate(type_set)}

    # one-hot encoding
    one_hot_array = np.zeros((len(type_list), len(type_set)), dtype=int)
    for i, types in enumerate(type_list):
        for t in types:
            if t in type_to_col:
                one_hot_array[i, type_to_col[t]] = 1

    # Dataframe으로 저장
    one_hot_encoded = pd.DataFrame(one_hot_array, columns=type_set)
    one_hot_encoded.insert(0, 'author_id', author_id_list)
    return one_hot_encoded

sorted_res_df, type_set = load_data(df_path, type_set_path)

one_hot_encoding_type(sorted_res_df,type_set)