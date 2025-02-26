import streamlit as st
import pandas as pd 
import numpy as np
import plotly.graph_objects as go
from PIL import Image

st.set_page_config(layout="wide")

st.title('Agile Assessment Data Preprocessor')


def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')

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

def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')


uploaded_file = st.file_uploader('Select your "Agile Assessment" csv file.')
if uploaded_file is not None:
    # Can be used wherever a "file-like" object is accepted:
    st.success('File successfully uploaded and processed.')
    data = pd.read_csv(uploaded_file, encoding='windows-1252')
    applied = data.astype(str).apply(lambda x: x.str[0:20]).drop(["Id", "Start time", "Completion time", "Email", "Name", 'Which best describes the function of your team?\xa0\xa0', 'What is your role level at Pacific Life?\xa0\xa0', 'How long have you been a member of your current team?\xa0\xa0', 'Have you completed formal agile training?', 'If yes, describe the type of training.\xa0', 'How long has your team been operating using agile practices?\xa0'], axis = 1)

    applied_func = applied.map(replacer)

    dct = dict()
    col_names = ["Role Sentiment", "Team Perform Role", "Team Composition", "Team Set Goals", "Team Backlog", "Team Ceremonies", "Team Performance", "Customer Feedback", "Team Deployment", "Team Retrospectives", "Team Experience", "Work Life Balance"]
    for i in range(len(applied_func.columns)):
        dct[applied_func.columns[i]] = col_names[i]

    applied_func = applied_func.rename(dct, axis = 1)

    data_trunc_t = applied_func.transpose().reset_index(names = "Trait")
    data_trunc_t["Average"] = data_trunc_t.drop("Trait", axis = 1).mean(axis = 1).round(2)

    def color(row):
        if row["Average"] >= 2:
            return "#343091"
        elif row["Average"] >= 1:
            return "#7577b8"
        else:
            return "#babad4"

    csv = convert_df(data_trunc_t)

    st.download_button("Download the pre-processed file", csv,  "processed.csv", "text/csv", key='download-csv')

    # data_trunc_t["Color"] = data_trunc_t.apply(color, axis = 1)

    proc = data_trunc_t.copy()

    import plotly.graph_objects as go

    image = Image.open("background.png")

    fig = go.Figure(data = [
        go.Bar(x = proc["Trait"], 
            y = proc["Average"],
            text = proc["Average"],
            marker_color = "white")
    ])
    fig.update_layout(
        yaxis_range=[0,3],
        autosize=False,
        width=1028,
        height=800,
        margin=dict(
            l=50,
            r=50,
            b=100,
            t=100,
        )
    )
    fig.add_layout_image(
            dict(
                source=image,
                xref="x",
                yref="y",
                x=-0.5,
                y=3,
                sizex=12,
                sizey=3,
                sizing="stretch",
                opacity=1,
                layer="below")
    )

    fig.update_traces(marker=dict(line=dict(width=5, color='DarkSlateGrey')))
   
    st.plotly_chart(fig)


else:
    st.warning("Please upload a file!")
