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

# todo word tokenize
STREET_NAMES = list(set(df["street"]))
print(STREET_NAMES)
