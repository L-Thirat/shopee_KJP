import spacy
import random
import time
import warnings
import json
import pandas as pd
import numpy as np

dataset = "data/train.csv/train.csv"

pd.set_option('display.max_columns', 20)

cols = ["raw_address", "POI/street"]
train_en = "POI"

df = pd.read_csv(dataset, usecols=cols)
split_data = df["POI/street"].str.split("/", n=1, expand=True)
if train_en == "POI":
    df["POI"] = split_data[0]
else:
    df["street"] = split_data[1]

s_split = (df['raw_address'].str.split(',', expand=True))
df = pd.concat([s_split, df], axis=1)
df["comma_n"] = np.NaN


def comma_count(i=0):
    if i == s_split.shape[1]:
        pass
    else:
        df.loc[((df[train_en] == df[i]) & (df[train_en] != "")), 'comma_n'] = i
        i += 1
        comma_count(i=i)


comma_count()
df["comma_n"] = df["comma_n"].fillna(s_split.shape[1]+1)
df["count_comma"] = df['raw_address'].str.count(',')
print(df["count_comma"].value_counts(dropna=False))
print(df[0])
print(df[1])
print(df[2])
# df['POI_in'] = df.apply(lambda x: x[train_en] in x["raw_address"], axis=1)

pdca_comma = (df[["count_comma", "comma_n"]].groupby(["count_comma", "comma_n"]).size())
print(pdca_comma)
# 43040 pos 0 /

"""
if count_comma in [4] -> POI = split comma 0

if one comma = street
    ex mas bah ii, = /
    ex yos suda, = yos suda

if "jl ..", "jalan..", "jl.", "jln " -> both POI + street
    ex jl. pasar senen dlm. ..
        STREET = jl. pasar senen
        POI = pasar senen
    ex jalan setu baru studio alam tvri rt 01 01 kelurahan sukmajaya (pabrik roti arb)
        STREET = jalan + setu baru (2words)
        POI = setu baru
    ex jl.setu baru tvri (hj.dimun) kp.sidamukti rt03 rw06 no:85 kelurahan sukamaju
        STREET = jl. + setu baru (2words)
        POI = jl.setu baru
"""

"""
Word correction
indon = indonesia
"""