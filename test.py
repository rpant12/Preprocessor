import streamlit as st
import pandas as pd
import numpy as np

st.title('Agile Assessment Data Preprocessor')

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    # Can be used wherever a "file-like" object is accepted:
    data = pd.read_csv(uploaded_file, encoding='windows-1252')

applied = data.astype(str).apply(lambda x: x.str[0:20])

data2 = pd.DataFrame()
q1 = {
    "I fully understand m": 3,
    "I’m not clear how my": 0,
    "I have a basic under": 1,
    "My role is clearly d": 2
}

q2 = {
    "We don’t understand ": 0,
    "Our team is organize": 1,
    "We understand how to": 2,
    "Roles on our team ar": 3
}

q3 = {
    "Our team is organize": 0,
    "Our team has a mix o": 1,
    "Our team is persiste": 2,
    "Our team is stable, ": 3
}

q4 = {
    "Our team does not co": 0,
    "Our team accepts goa": 1,
    "We contribute to the": 2,
    "Our team aligns our ": 3
}

q5 = {
    "We have a list of wo": 0,
    "We have a backlog wi": 1,
    "We create and stack-": 2,
    "Our backlog has clea": 3
}

q6 = {
    "Our team meatings ar": 0,
    "Our team holds agile": 1,
    "Our team conducts re": 2,
    "Our team collectivel": 3
}

q7 = {
    "Our team does not us": 0,
    "Our team tracks basi": 1,
    "Our team tracks adva": 2,
    "Our team tracks deli": 3
}

q8 = {
    "Our team rarely coll": 0,
    "Our team collects cu": 1,
    "Our team regularly e": 2,
    "Our team uses struct": 3
}

q9 = {
    "Our team deploys lar": 0, 
    "Our team deploys inc": 1,
    "Our team deploys eve": 2, 
    "Our team deploys sma": 3
}

q10 = {
    "Our team doesn’t con": 0,
    "Our team conducts re": 1,
    "Our team identifies ": 2,
    "Continuous improveme": 3
}

q11 = {
    "Our team must escala": 0,
    "Our team escalates m": 1,
    "Our team is empowere": 2,
    "Our team makes decis": 3
}

q12 = {
    "I often feel overwor": 0,
    "I occasionally work ": 1,
    "I work at a sustaina": 2,
    "My personal purpose,": 3,
    "test test ": 0
}

data_trunc = pd.DataFrame()
data_trunc["Feel Role"] = applied['Which statement best describes how you feel about your role on your team?\xa0'].replace(q1)
data_trunc["Team Role"] = applied["\xa0Which statement best describes how your team members collectively perform their roles?\xa0"].replace(q2)
data_trunc["Team Composition"] = applied["Which statement best describes your team composition?\xa0"].replace(q3)
data_trunc["Team Goals"] = applied["Does your team set strategic, inspirational goals (e.g., using OKRs, SMART goals)?\xa0"].replace(q4)
data_trunc["Team Backlog"] = applied['How does your team manage the backlog?\xa0\xa0'].replace(q5)
data_trunc["Team Ceremonies"] = applied['How would you describe your team’s ceremonies?\xa0\xa0'].replace(q6)
data_trunc["Team Performance"] = applied['How do you measure team performance?\xa0'].replace(q7)
data_trunc["Customer Feedback"] = applied['How do you use customer feedback to improve value delivery?\xa0'].replace(q8)
data_trunc["Team Deploy"] = applied['Which statement best describes the deployment frequency for your team?\xa0'].replace(q9)
data_trunc["Team Improvement"] = applied['Which statement best describes your team?\xa01'].replace(q10) 
data_trunc["Decision Making"] = applied['Which statement best describes your team’s experience?\xa0'].replace(q11)
data_trunc["Work-Life Balance"] = applied['Which statement best describes how you feel about your work-life balance and job satisfaction?\xa0\xa0'].replace(q12)

data_trunc_t = data_trunc.transpose().reset_index(names = "Trait")
data_trunc_t["Average"] = (data_trunc_t[0] + data_trunc_t[1] + data_trunc_t[2] + data_trunc_t[3] + data_trunc_t[4] + data_trunc_t[5] + data_trunc_t[6]) / 7

def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')


csv = convert_df(data_trunc_t)


st.download_button("Download the pre-processed file", csv,  "processed.csv", "text/csv", key='download-csv')