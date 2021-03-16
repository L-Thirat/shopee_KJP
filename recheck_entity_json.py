import json
import pandas as pd

dataset = "data/train.csv/train.csv"
hash_dataset = "data/train.csv/hash_train.csv"
# dataset = "data/test.csv/test.csv"

train_ner_filename = "train_ner.json"
val_ner_filename = "val_ner.json"

pd.set_option('display.max_columns', 20)

cols = ["raw_address", "POI/street"]
train_en = "POI"

df = pd.read_csv(dataset, usecols=cols)
hash_df = pd.read_csv(hash_dataset, usecols=["raw_address"])
hash_df["hash_raw_address"] = hash_df["raw_address"]
del hash_df["raw_address"]

df = pd.concat([df, hash_df], axis=1)

# df = pd.read_csv(train_file, usecols=cols, nrows=5)

split_data = df["POI/street"].str.split("/", n=1, expand=True)
df["POI"] = split_data[0]
df["street"] = split_data[1]

POI = set(df["POI"])

with open(val_ner_filename, "r", encoding='utf-8') as json_file:
    TEST_DATA = json.load(json_file)

for item in TEST_DATA:
    start = item[1]["entities"][0][0]
    end = item[1]["entities"][0][1]
    txt = (item[0][start:end])
    if txt not in POI:
        print(txt)

with open(train_ner_filename, "r", encoding='utf-8') as json_file:
    TEST_DATA = json.load(json_file)

for item in TEST_DATA:
    start = item[1]["entities"][0][0]
    end = item[1]["entities"][0][1]
    txt = (item[0][start:end])
    if txt not in POI:
        print(txt)
