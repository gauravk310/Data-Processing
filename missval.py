import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np

def app():
    st.title("Missing Values")
    st.image('static/missingData.jpg',width=600)
    col1,col2 = st.columns(2)
    app = option_menu(
                menu_title="Missing Value Operations",
                options=['Drop','Fill'],
                icons=['table','table'],
                default_index=0,
                styles={
                    'container':{'padding':'5 !importnant','background-color':'dark'},
                    'icon':{'color':'white','font-size':'25px'},
                    'nav-link':{'color':'white','font-size':'20px','text-align':'center'},
                    'nav-link-selected':{'background-color':'#02ab21'}
                },orientation='horizontal'
            )
        
    df = pd.DataFrame({})
    try:
        df =  st.session_state.data['file']
    except Exception:
        st.warning("DataSet Not Found...!")
    # st.subheader('Missing Values')
    # miss = df.isnull().sum().to_dict()
    # st.table(miss)
    st.write(f"Shape Before Droping None Values : {df.shape}")
    miss = df.isnull().sum()
    miss = miss[miss > 0]
    miss_val = miss[miss > 0].index.to_list()
    st.write(miss)
    if app=='Drop':
        try:
            if st.button("Drop None Values"):
                df = df.dropna()
                df = df.reset_index(drop=True)
                st.session_state.data['file'] = df
                st.write(df)
                st.write(f"Shape After Droping None Values : {df.shape}")
                st.success("Data Saved Successfully...")
        except Exception:
            st.info("Data Drop Fail...")
    if app=='Fill':
        app = option_menu(
                menu_title="Feature Data Type",
                options=['Numerical','Categorical'],
                icons=['number','table'],
                default_index=0,
                orientation='horizontal'
            )
        if app == 'Numerical':    
            col1,col2 = st.columns(2)
            try:
                cols =col1.radio("Features",[x for x in miss_val if pd.api.types.is_numeric_dtype(df[x])],horizontal=True)
                cheak = col1.checkbox("SHOW DATA",value=False)
                if cheak:
                    col1.write(df[cols])
            except Exception:
                st.warning("No Data Found")
            method = col2.selectbox('Methos',['Mean','Median','Random'])
            if method=='Mean':
                try:
                    mean = round(df[cols].mean(),1)
                    col2.write(mean)
                except Exception:
                    st.info("No Missing Data Found ...!!!!")
                try:
                    if col2.button("Fill Data With Mean"):
                        df = df[cols].fillna(mean,inplace=True)
                        st.info("Values Filled Succesfully...")
                except Exception:
                    st.info("No Data Found ...")
            if method=='Median':
                try:
                    median = round(df[cols].median(),1)
                    col2.write(median)
                except Exception:
                    st.info("No Missing Data Found ...!!!!")
                try:
                    if col2.button("Fill Data With Mean"):
                        df = df[cols].fillna(median,inplace=True)
                        st.info("Values Filled Succesfully...")
                except Exception:
                    st.info("No Missing Data Found ...!!!!")

            if method=='Random':
                try:
                    non_miss_val = df[cols].dropna().values
                    random_values = np.random.choice(non_miss_val, df[cols].isnull().sum())
                    df.loc[df[cols].isnull(), cols] = random_values
                    st.write(non_miss_val)
                except Exception:
                    st.info("No Missing Data Found..!!!")
                
                try:
                    pass
                except Exception:
                    st.info("No Missing Data Found ...!!!!")
                try:
                    if col2.button("Fill Data With Most Your Value"):
                        # df[cols][df[cols].isnull()] = freq
                        df.loc[df[cols].isnull(), cols] = random_values
                        st.info("Values Filled Succesfully...")
                except Exception:
                    st.info("No Missing Data Avilable ...")

        if app=='Categorical':
            col1,col2 = st.columns(2)
            try:
                cols =col1.radio("Features",[x for x in miss_val if not pd.api.types.is_numeric_dtype(df[x])],horizontal=True)
                cheak = col1.checkbox("SHOW DATA",value=False)
                if cheak:
                    col1.write(df[cols])
            except Exception:
                st.warning("No Data Found")
            method = col2.selectbox('Methos',['Most-Recent','Value'])
            if method=='Most-Recent':
                try:
                    freq = df[cols].mode().iloc[0]
                    col2.write(freq)
                except Exception:
                    st.info("No Missing Data Found ...!!!!")
                try:
                    if col2.button("Fill Data With Most Frequent Value"):
                        df[cols].fillna(freq,inplace=True)
                        st.info("Values Filled Succesfully...")
                except Exception:
                    st.info("No Missing Data Avilable ...")

            if method=='Value':
                try:
                    freq = col2.text_input("Enter Your Value : ")
                    col2.write(freq)
                except Exception:
                    st.info("No Missing Data Found ...!!!!")
                try:
                    if col2.button("Fill Data With Most Your Value"):
                        df[cols].fillna(freq,inplace=True)
                        st.info("Values Filled Succesfully...")
                except Exception:
                    st.info("No Missing Data Avilable ...")
        try:
            if st.button("Save Dataset"):
                st.session_state.data['file'] = df
                st.write(miss)
                st.success("Data Saved Successfully...")
        except Exception:
            st.info("Data Already Saved ...")
             
                

