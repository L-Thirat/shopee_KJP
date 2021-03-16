import pandas as pd
import json
import re

dataset = "data/train.csv/train.csv"
hash_dataset = "data/train.csv/hash_train.csv"
# dataset = "data/test.csv/test.csv"

train_ner_filename = "train_ner.json"
val_ner_filename = "val_ner.json"

pd.set_option('display.max_columns', 20)

cols = ["raw_address", "POI/street"]
# train_en = "POI"


# todo merge correction
# with open("extract_data/poi_corection.json", "r", encoding='utf-8') as json_file:
#     a = json.load(json_file)
# with open("extract_data/poi_frequency_match1.json", "r", encoding='utf-8') as json_file:
#     a_match = json.load(json_file)
# with open("extract_data/street_corection.json", "r", encoding='utf-8') as json_file:
#     b = json.load(json_file)
# with open("extract_data/street_frequency_match1.json", "r", encoding='utf-8') as json_file:
#     b_match = json.load(json_file)
#
# output = {}
# for key in b:
#     max_key = max(b[key], key=b[key].get)
#     max_val = b[key][max_key]
#     if key in b_match:
#         if max_val > b_match[key]:
#             output[key] = max_key
#     else:
#         output[key] = max_key
#
# for key in a:
#     max_key = max(a[key], key=a[key].get)
#     max_val = a[key][max_key]
#     if key not in output:
#         if key in a_match:
#             if max_val > a_match[key]:
#                 output[key] = max_key
#         else:
#             output[key] = max_key
#
# with open("extract_data/corr_poi_street.json", 'w', encoding='utf-8') as f:
#     json.dump(output, f)
# asd

with open("extract_data/corr_poi_street.json", "r", encoding='utf-8') as json_file:
# with open("extract_data/poi_corection.json", "r", encoding='utf-8') as json_file:
    corrections = json.load(json_file)
# invt_corrections = {}
# for item in corrections:
#     invt_corrections[corrections[item]] = item

df = pd.read_csv(dataset, usecols=cols)
corr_raw_address = []

for index, row in df.iterrows():
    raw_address = row["raw_address"]
    # token = raw_address.split(" ")
    token = re.split('[^a-zA-Z0-9]+', raw_address)
    correct = []
    for t in token:
        if t in corrections:
            correct.append(corrections[t])
        else:
            correct.append(t)
    corr_raw_address.append(" ".join(correct))
df['raw_address'] = corr_raw_address
df.to_csv(hash_dataset, index=False)
