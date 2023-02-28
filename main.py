import pandas as pd
import streamlit as st
from functionforDownloadButtons import download_button
import requests
from streamlit_tags import st_tags
API_URL = "https://api-inference.huggingface.co/models/joeddav/xlm-roberta-large-xnli"

def _max_width_():
    max_width_str = f"max-width: 1800px;"
    st.markdown(
        f"""
    <style>
    .reportview-container .main .block-container{{
        {max_width_str}
    }}

    </style>    
    """,
        unsafe_allow_html=True,
    )

st.set_page_config(page_icon="images/icon.png", page_title="RNC Text Classification")
API_KEY = st.sidebar.text_input(
    "Enter your HuggingFace API key",
    help="Once you created you HuggingFace account, you can get your free API token in your settings page: https://huggingface.co/settings/tokens",
    type="password",
)
headers = {"Authorization": f"Bearer {API_KEY}"}
c2, c3 = st.columns([6, 1])

with c2:
    c31, c32 = st.columns([12, 2])
    with c31:
        st.caption("")
        st.title("Text Classifier")
    with c32:
        st.image(
            "images/logo.png",
            width=200,
        )

uploaded_file = st.file_uploader(
    " ",
    key="1",
    help="To activate 'wide mode', go to the hamburger menu > Settings > turn on 'wide mode'",
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    uploaded_file.seek(0)


    file_container = st.expander("Check your uploaded .csv")
    file_container.write(df)


else:
    st.info(
        f"""
            👆 Upload a .csv file first. Sample to try: [biostats.csv](https://people.sc.fsu.edu/~jburkardt/data/csv/biostats.csv)
            """
    )

    st.stop()
encode_list = []
def get_values(column_names, labels_from_st_tags ):
    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()


    label_lists = {}

    for element in labels_from_st_tags:
        label_lists[element] = []

    for index, row in df[column_names].items():
        output = query({
            "inputs": row,
            "parameters": {"candidate_labels": labels_from_st_tags},
        })

        for index_, value in enumerate(output['labels']):
            label_lists[value].append(output['scores'][index_])

    for vals in labels_from_st_tags:
        df[vals] = label_lists[vals]
    return



form = st.form(key="annotation")
with form:

    column_names = st.selectbox(
        "Column name:", list(df.columns)
    )

    labels_from_st_tags = st_tags(
        value=["account", "credit", "reporting"],
        maxtags=5,
        suggestions=["account", "credit", "reporting"],
        label="",
    )
    keywords_ = st.text_input("Enter keywords by using , !")

    submitted = st.form_submit_button(label="Submit")
result_df = pd.DataFrame()
if submitted:

    result = get_values(column_names, labels_from_st_tags)


c29, c30, c31 = st.columns([1, 1, 2])

with c29:

    CSVButton = download_button(
        df,
        "FlaggedFile.csv",
        "Download to CSV",
    )