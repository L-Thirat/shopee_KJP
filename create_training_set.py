import pandas as pd
from numpy.core.defchararray import find
import json
import numpy as np

dataset = "data/train.csv/train.csv"
hash_dataset = "data/train.csv/hash_train.csv"
# dataset = "data/test.csv/test.csv"

train_ner_filename = "train_ner.json"
val_ner_filename = "val_ner.json"

pd.set_option('display.max_columns', 20)

cols = ["raw_address", "POI/street"]
train_en = "street"


# todo train
df = pd.read_csv(dataset, usecols=cols)
hash_df = pd.read_csv(hash_dataset, usecols=["raw_address"])
# hash_df = pd.read_csv(hash_dataset, usecols=cols)
hash_df["hash_raw_address"] = hash_df["raw_address"]
del hash_df["raw_address"]

df = pd.concat([df, hash_df], axis=1)

split_data = df["POI/street"].str.split("/", n=1, expand=True)
df["POI"] = split_data[0]
df["street"] = split_data[1]

# df['POI_in'] = df.apply(lambda x: x["POI"] in x["raw_address"], axis=1)
# df['street_in'] = df.apply(lambda x: x["street"] in x["raw_address"], axis=1)

# todo correction
with open("extract_data/corr_poi_street.json", "r", encoding='utf-8') as json_file:
    corrections = json.load(json_file)


def gen_entity_pos(col_name):
    b = df[df[col_name] != ""].raw_address.values.astype(str)
    df.loc[df[col_name] == "", 'start_%s' % col_name] = -2
    df.loc[df[col_name] == "", 'end_%s' % col_name] = -2

    df["mock_%s" % col_name] = " " + df[col_name] + " "
    a = df[df[col_name] != ""]["mock_%s" % col_name].values.astype(str)
    df.loc[(df[col_name] != ""), 'start_%s' % col_name] = find(b, a) + 1
    df.loc[(df['start_%s' % col_name] == 0), 'start_%s' % col_name] = -1
    print(df[(df['start_%s' % col_name] != -1) & (df['start_%s' % col_name] != -2)].shape)

    b = df[df['start_%s' % col_name] == -1].raw_address.values.astype(str)
    df["mock_%s" % col_name] = " " + df[col_name] + ","
    a = df[df['start_%s' % col_name] == -1]["mock_%s" % col_name].values.astype(str)
    df.loc[df['start_%s' % col_name] == -1, 'start_%s' % col_name] = find(b, a) + 1
    df.loc[(df['start_%s' % col_name] == 0), 'start_%s' % col_name] = -1
    print(df[(df['start_%s' % col_name] != -1) & (df['start_%s' % col_name] != -2)].shape)

    b = df[df['start_%s' % col_name] == -1].raw_address.values.astype(str)
    a = df[df['start_%s' % col_name] == -1][col_name].values.astype(str)
    df.loc[df['start_%s' % col_name] == -1, 'start_%s' % col_name] = find(b, a)
    print(df[(df['start_%s' % col_name] != -1) & (df['start_%s' % col_name] != -2)].shape)
    # print(df[(df['start_%s' % col_name] != -1) & (df['start_%s' % col_name] != -2)])
    # print(df[(df['start_%s' % col_name] != 0)])
    print("--------------")
    # asd
    # kembangan utara b,
    df["end_%s" % col_name] = df["start_%s" % col_name] + df[col_name].str.len()

#10      cikahuripan sd neg boj 02 klap boj, no 5 16877
def re_gen_entity_pos(col_name):
    b = df[df['start_%s' % col_name] == -1].hash_raw_address.values.astype(str)
    df["mock_%s" % col_name] = " " + df[col_name] + " "
    a = df[df['start_%s' % col_name] == -1]["mock_%s" % col_name].values.astype(str)
    df.loc[df['start_%s' % col_name] == -1, 'temp_start_%s' % col_name] = find(b, a) + 1
    df.loc[(df['temp_start_%s' % col_name] > 0), 'start_%s' % col_name] = df['temp_start_%s' % col_name]
    print(df[(df['start_%s' % col_name] != -1) & (df['start_%s' % col_name] != -2)].shape)

    b = df[df['start_%s' % col_name] == -1].hash_raw_address.values.astype(str)
    df["mock_%s" % col_name] = " " + df[col_name] + ","
    a = df[df['start_%s' % col_name] == -1]["mock_%s" % col_name].values.astype(str)
    df.loc[df['start_%s' % col_name] == -1, 'temp_start_%s' % col_name] = find(b, a) + 1
    df.loc[(df['temp_start_%s' % col_name] > 0), 'start_%s' % col_name] = df['temp_start_%s' % col_name]
    print(df[(df['start_%s' % col_name] != -1) & (df['start_%s' % col_name] != -2)].shape)

    b = df[df['start_%s' % col_name] == -1].hash_raw_address.values.astype(str)
    a = df[df['start_%s' % col_name] == -1][col_name].values.astype(str)
    df.loc[df['start_%s' % col_name] == -1, 'start_%s' % col_name] = find(b, a)
    print(df[(df['start_%s' % col_name] != -1) & (df['start_%s' % col_name] != -2)].shape)
    check_hash = (df[(df['start_%s' % col_name] == -1)][["POI", "hash_raw_address"]])
    check_hash.to_csv("check_hash.csv")
    print("--------------") # unmatch: 32671 -> 21035
    # asd
    # kembangan utara b,
    df["end_%s" % col_name] = df["start_%s" % col_name] + df[col_name].str.len()

    # df.loc[(df['start_%s' % col_name] == -1), 'mock_%s' % col_name] = " " + df[col_name] + " "
    # a = df["mock_%s" % col_name].values.astype(str)
    # df["start_%s" % col_name] = find(b, a) + 1
    #
    # df.loc[(df['start_%s' % col_name] == -1), 'mock2_%s' % col_name] = " " + df[col_name] + ","
    # a = df["mock2_%s" % col_name].values.astype(str)
    # df["start2_%s" % col_name] = find(b, a) + 1
    #
    # a = df[col_name].values.astype(str)
    # df.loc[(df['start_%s' % col_name] == -1), 'mock2_%s' % col_name]["cur_start_%s" % col_name] = find(b, a)  # + 1
    #
    # # kembangan utara b,
    # df.loc[(df['start_%s' % col_name] == -1) & (df[col_name] != ""), 'start_%s' % col_name] = df["start2_%s" % col_name]
    # df.loc[(df['start_%s' % col_name] == -1) & (df[col_name] != ""), 'start_%s' % col_name] = df["cur_start_%s" % col_name]
    # df["end_%s" % col_name] = df["start_%s" % col_name] + df[col_name].str.len()
    #
    # df.loc[df[col_name] == "", 'start_%s' % col_name] = -2
    # df.loc[df[col_name] == "", 'end_%s' % col_name] = -2


gen_entity_pos("street")
re_gen_entity_pos("street")
gen_entity_pos("POI")
re_gen_entity_pos("POI")
df["start_street"] = df["start_street"].astype(int)
df["end_street"] = df["end_street"].astype(int)
df["start_POI"] = df["start_POI"].astype(int)
df["end_POI"] = df["end_POI"].astype(int)

# todo word tokenize
# STREET_NAMES = list(set(df["street"]))
# print(STREET_NAMES)
# df.loc[df['start_street'] == 0, 'start_street'] = df["raw_address"].str.split(r"\+|=", expand=True)


def intersect_street_POI(col):
    mock = " " + row[col] + " "
    start = raw_address[end:].find(mock)
    if start == -1:
        mock = " " + row[col] + ","
        start = raw_address[end:].find(mock)
        if start == -1:
            new_start = raw_address[end:].find(row[col])
            if new_start != -1:
                return new_start, new_start + len(row[col])
    return False


ner_def = []
for index, row in df.iterrows():
    raw_address = row['raw_address']
    entities = []
    start = row["start_%s" % train_en]
    end = row['end_%s' % train_en]

    if raw_address[start:end] != row[train_en]:
        raw_address = row['hash_raw_address']
        if raw_address[start:end] != row[train_en] and (start > -1):
            print(start, end, row)
            raise(Exception("BUG!"))

    # todo train STREET
    if train_en == "street":
        if row["street"] and start != -1:
            # start_poi = row['start_POI']
            # end_poi = row['end_POI']
            # if row["POI"] and start_poi != -1:
            #     if set(range(start, end+1)).intersection(set(range(start_poi, end_poi+1))):
            #         if intersect_street_POI("street"):
            #             start, end = intersect_street_POI("street")
            entities.append((start, end, "LOCATION"))
    else:
        if row["POI"] and start != -1:
            entities.append((start, end, "POI"))
    # todo rule-based -> ? (testing)
    # if row['end_street'] < (len(raw_address)):
    #     if raw_address[row['end_street']] != " ":
    #         raw_address = raw_address[:row['end_street']] + " " + raw_address[row['end_street']:]
    # if row['start_street'] > 0:
    #     if raw_address[row['start_street']-1] != " ":
    #         raw_address = raw_address[:row['start_street']] + " " + raw_address[row['start_street']:]
    #         start += 1
    #         end += 1
    if entities:
        ner = {
            "entities": entities
        }
        ner_def.append((raw_address, ner))


train_val_per = int(len(ner_def) * 0.15)

with open(train_ner_filename, 'w', encoding='utf-8') as f:
    TRAIN_DATA = ner_def[:-train_val_per]
    json.dump(TRAIN_DATA, f)

with open(val_ner_filename, 'w', encoding='utf-8') as f:
    TEST_DATA = ner_def[-train_val_per:]
    json.dump(TEST_DATA, f)
