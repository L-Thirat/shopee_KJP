import pandas as pd
import json

dataset = "data/train.csv/train.csv"
hash_dataset = "data/train.csv/hash_train.csv"
# dataset = "data/test.csv/test.csv"

train_ner_filename = "train_ner.json"
val_ner_filename = "val_ner.json"

pd.set_option('display.max_columns', 20)

cols = ["raw_address", "POI/street"]
train_en = "POI"


# todo merge correction
# with open("extract_data/poi_corection-3.json", "r", encoding='utf-8') as json_file:
#     a = json.load(json_file)
# with open("extract_data/poi_corection-3.json", "r", encoding='utf-8') as json_file:
#     b = json.load(json_file)
# for item in b:
#     if item not in a:
#         a[item] = b[item]
# with open("extract_data/corr_poi_street.json", 'w', encoding='utf-8') as f:
#     json.dump(a, f)

with open("extract_data/corr_poi_street.json", "r", encoding='utf-8') as json_file:
    corrections = json.load(json_file)
# invt_corrections = {}
# for item in corrections:
#     invt_corrections[corrections[item]] = item

df = pd.read_csv(dataset, usecols=cols)

df['raw_address'] = df['raw_address'].replace(corrections, regex=True)
df.to_csv(hash_dataset, index=False)
