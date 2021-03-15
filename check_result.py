import pandas as pd

dir = "result/train_nul_entity__fulltrain/"
result_file = dir + "submit_poi.csv"
df = pd.read_csv(result_file)

df.loc[(df["predict"] == df["output"]), 'correct'] = True
df.loc[(df["predict"] != df["output"]), 'correct'] = False

print(df["correct"].value_counts()) #14781/7824 -> 19307/3159
asd
# todo colab write result
import json
import spacy


# Settings for google Collab
if True:
    spacy.require_gpu()
    gpu = spacy.prefer_gpu()
    print('GPU:', gpu)

val_ner_filename = "val_ner.json"
with open(val_ner_filename, "r", encoding='utf-8') as json_file:
    TEST_DATA = json.load(json_file)

modelfile = output_dir + "Final_model"
nlp2 = spacy.load(modelfile)

output_entity = []
output_pred = []
output_output = []

for test_text, entities in TEST_DATA:
  doc2 = nlp2(test_text)
  for ent in doc2.ents:
    predict = ent.label_
    text = ent.text
    print(ent)
  asd
  if entities['entities']:
    output = test_text[entities['entities'][0][0]: entities['entities'][0][1]]
  else:
    output = ""
  output_entity.append(predict)
  output_pred.append(text)
  output_output.append(output)


df = pd.DataFrame({'entity': output_entity,
                  'predict': output_pred,
                  'output': output_output})
df.to_csv("submit_poi.csv", index=False)