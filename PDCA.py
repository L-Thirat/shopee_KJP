import pandas as pd

train_file = "data/train.csv/train.csv"
test_file = "data/test.csv/test.csv"

pd.set_option('display.max_columns', 20)

cols = ["raw_address", "POI/street"]

df_train = pd.read_csv(train_file, usecols=cols)#, nrows=5)

split_data = df_train["POI/street"].str.split("/", n=1, expand=True)
df_train["POI"] = split_data[0]
df_train["street"] = split_data[1]
# df_train.drop(columns =["POI/street"], inplace = True)

df_train['POI_in'] = df_train.apply(lambda x: x["POI"] in x["raw_address"], axis=1)
df_train['street_in'] = df_train.apply(lambda x: x["street"] in x["raw_address"], axis=1)
print(df_train)
print(df_train['POI_in'].value_counts())
print(df_train['street_in'].value_counts())
df_train.to_csv("check.csv")
