import streamlit as st
import pandas as pd
import numpy as np

def load_data():
    file = st.file_uploader('Upload Your Dataset')
    if file:
        st.success("Dataset Upload")
        df = pd.read_csv(file)
        df = pd.DataFrame(df)
        return df


def app():
    st.header("Data Engineering ")
    st.image('static/home1.webp',width=800)
    # file = st.file_uploader('Upload Your Dataset')
    file = load_data()
    if file is not None:
        if 'data' not in st.session_state:
            st.session_state.data = {}
        # st.success("Dataset Upload")
        df = file
        st.session_state.data['file'] = df
        st.subheader('1. Dataset')
        st.write(df)
        st.subheader('2. Mathematical Discription')
        st.write(df.describe())
        st.subheader('3. Missing Values')
        miss = df.isnull().sum().to_dict()
        st.table(miss)
        st.subheader('4. Dataset Size')
        st.write(f"Shape Of DataSet : {df.shape}")
        st.subheader('5. Duplicate Values')
        if df.duplicated().sum() == 0:
            st.success("There Are No Duplicate Freatures..!!!")
        else:
            st.warning("There Are Some Duplicate Freatures ...!!")
        st.subheader('6. Corealtion Of Freatures')
        st.write(df.corr(numeric_only=True))
        
        st.subheader('7. Numerical Column :')
        try:
            cols =st.radio("Features",[x for x in df.columns if pd.api.types.is_numeric_dtype(df[x])],horizontal=True)
            cola,colb = st.columns(2)
            cola.subheader(cols)  
            cola.write(df[cols])
            colb.subheader("Description : ")
            colb.write(df[cols].describe())
        except Exception:
            st.info("Numerical Columns Not Found...!")
        
        st.subheader('7.Non -  Numerical Column :')
        try:
            cols =st.radio("Features",[x for x in df.columns if not pd.api.types.is_numeric_dtype(df[x])],horizontal=True)
            cola,colb = st.columns(2)
            cola.write(cols)  
            cola.write(df[cols])
            colb.subheader("Description : ")
            colb.write(df[cols].describe())
        except Exception:
            st.info("Non-Numberical Data Not Found...!")


        
        
