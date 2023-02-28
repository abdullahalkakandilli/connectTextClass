import pandas as pd
import requests

API_URL = "https://api-inference.huggingface.co/models/joeddav/xlm-roberta-large-xnli"
headers = {"Authorization": "Bearer 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"}

df = pd.read_csv('testRenc.csv')
pd.set_option('display.max_columns', None)
def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()
candidate_labels_ = ["refund", "legal", "faq"]

output = query({
    "inputs": "Hi, I recently bought a device from your company but it is not working as advertised and I would like to get reimbursed!",
    "parameters": {"candidate_labels": candidate_labels_},
})



label_lists = {}

for element in candidate_labels_:
    label_lists[element] = []

for index, row in df['Reviews'].items():
    output = query({
        "inputs": row,
        "parameters": {"candidate_labels": candidate_labels_},
    })

    for index_, value in enumerate(output['labels']):
        label_lists[value].append(output['scores'][index_])

for vals in candidate_labels_:
    df[vals] = label_lists[vals]

print(df)





