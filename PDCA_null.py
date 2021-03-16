import pandas as pd

train_file = "data/train.csv/train.csv"
test_file = "data/test.csv/test.csv"

pd.set_option('display.max_columns', 20)

cols = ["raw_address", "POI/street"]

df_train = pd.read_csv(train_file, usecols=cols)  # , nrows=5)

split_data = df_train["POI/street"].str.split("/", n=1, expand=True)
df_train["POI"] = split_data[0]
df_train["street"] = split_data[1]
# df_train.drop(columns =["POI/street"], inplace = True)

df_train['POI_in'] = df_train.apply(lambda x: x["POI"] != "", axis=1)
df_train['street_in'] = df_train.apply(lambda x: x["street"] != "", axis=1)


def myfunc(poi, street):
    if poi and street:
        output = 3
    elif not poi and street:
        output = 2
    elif poi and not street:
        output = 1
    else:
        output = 0
    return output


df_train['label'] = df_train.apply(lambda x: myfunc(x['POI_in'], x['street_in']), axis=1)

print(df_train)
print(df_train['POI_in'].value_counts())  # 253860/46140
print(df_train['street_in'].value_counts())  # 282613/17387

df_train.to_csv("check.csv")
