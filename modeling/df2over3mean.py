import pandas as pd

def df2over3mean(type_freq_by_user):
    over3mean = {}
    for column in type_freq_by_user.columns:
        x = type_freq_by_user[type_freq_by_user.loc[:,column]>=3]
        over3mean[column] = x.loc[:,column].mean()
    return over3mean
