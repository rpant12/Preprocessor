import streamlit as st # type: ignore
import pandas as pd # type: ignore
import numpy as np #type: ignore

st.title('Agile Assessment Data Preprocessor')

uploaded_file = st.file_uploader('Select your "Agile Assessment" csv file.')
if uploaded_file is not None:
    # Can be used wherever a "file-like" object is accepted:
    data = pd.read_csv(uploaded_file, encoding='windows-1252')

applied = data.astype(str).apply(lambda x: x.str[0:20]).drop(["Id", "Start time", "Completion time", "Email", "Name", 'Which best describes the function of your team?\xa0\xa0', 'What is your role level at Pacific Life?\xa0\xa0', 'How long have you been a member of your current team?\xa0\xa0', 'Have you completed formal agile training?', 'If yes, describe the type of training.\xa0', 'How long has your team been operating using agile practices?\xa0'], axis = 1)

def replacer(item):
    if "A)" in item:
        return 0
    elif "B)" in item: 
        return 1
    elif "C)" in item:
        return 2
    elif "D)" in item:
        return 3
    else:
        return item

applied_func = applied.map(replacer)

dct = dict()
col_names = ["Feel Role", "Team Perform Role", "Team Composition", "Team Set Goals", "Team Backlog", "Team Ceremonies", "Team Performance", "Customer Feedback", "Team Deployment", "Team Retrospectives", "Team Experience", "Job Satisfaction"]
for i in range(len(applied_func.columns)):
    dct[applied_func.columns[i]] = col_names[i]

applied_func = applied_func.rename(dct, axis = 1)

data_trunc_t = applied_func.transpose().reset_index(names = "Trait")
data_trunc_t["Average"] = data_trunc_t.drop("Trait", axis = 1).mean(axis = 1)

def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')


csv = convert_df(data_trunc_t)


st.download_button("Download the pre-processed file", csv,  "processed.csv", "text/csv", key='download-csv')
