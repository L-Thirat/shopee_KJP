import pandas as pd
from numpy.core.defchararray import find
import json

dataset = "data/train.csv/train.csv"
# dataset = "data/test.csv/test.csv"

train_ner_filename = "train_ner.json"
val_ner_filename = "val_ner.json"

pd.set_option('display.max_columns', 20)

cols = ["raw_address", "POI/street"]

df = pd.read_csv(dataset, usecols=cols)
# df = pd.read_csv(train_file, usecols=cols, nrows=5)

split_data = df["POI/street"].str.split("/", n=1, expand=True)
df["POI"] = split_data[0]
df["street"] = split_data[1]

df['POI_in'] = df.apply(lambda x: x["POI"] in x["raw_address"], axis=1)
df['street_in'] = df.apply(lambda x: x["street"] in x["raw_address"], axis=1)

df["mock_street"] = " " + df["street"] + " "
a = df.mock_street.values.astype(str)
b = df.raw_address.values.astype(str)
df["start_street"] = find(b, a) + 1

df["mock2_street"] = " " + df["street"] + ","
a = df.mock2_street.values.astype(str)
df["start2_street"] = find(b, a) + 1

a = df.street.values.astype(str)
df["cur_start_street"] = find(b, a) #+ 1


# kembangan utara b,
df.loc[df['start_street'] == 0, 'start_street'] = df["start2_street"]
df.loc[df['start_street'] == 0, 'start_street'] = df["cur_start_street"]
# df[df['start_street'] == 0]["start_street"] = df["cur_start_street"]

# df.loc[df['mock_start_street'] == -1, 'start_street'] = df["cur_start_street"]
# df.loc[df['Country']=='USA','z'] = foo['x']
# df["start_street"] = df['start_street'].where(df['mock_start_street'] == -1, df['start_street'])

df["end_street"] = df["start_street"] + df["street"].str.len()

# todo word tokenize
# STREET_NAMES = list(set(df["street"]))
# print(STREET_NAMES)
# df.loc[df['start_street'] == 0, 'start_street'] = df["raw_address"].str.split(r"\+|=", expand=True)

# print(df)
# asd
ner_def = []
for index, row in df.iterrows():
    if row["street"] and row['start_street'] != -1:
        start = row['start_street']
        end = row['end_street']

        # todo rule-based -> ? (testing)
        raw_address = row['raw_address']
        if row['end_street'] < (len(raw_address)):
            if raw_address[row['end_street']] != " ":
                raw_address = raw_address[:row['end_street']] + " " + raw_address[row['end_street']:]
        if row['start_street'] > 0:
            if raw_address[row['start_street']-1] != " ":
                raw_address = raw_address[:row['start_street']] + " " + raw_address[row['start_street']:]
                start += 1
                end += 1
        ner = {
            "entities": [(start, end, "LOCATION")]
        }
        ner_def.append((raw_address, ner))

train_val_per = int(len(ner_def) * 0.15)

with open(train_ner_filename, 'w', encoding='utf-8') as f:
    TRAIN_DATA = ner_def[:-train_val_per]
    json.dump(TRAIN_DATA, f)

with open(val_ner_filename, 'w', encoding='utf-8') as f:
    TEST_DATA = ner_def[-train_val_per:]
    json.dump(TEST_DATA, f)