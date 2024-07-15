import streamlit as st
import pandas as pd
import numpy as np

def save_dataset(df):
    try:
        st.session_state.data['file'] = df
        st.write(df)
        st.write(df.shape)
        st.success("Data Saved Successfully...")
    except Exception:
                st.info("Data Already Saved ...")


def app():
    st.title("Outlier Page")
    st.image('static/outlier.jpg',width=700)
    method = st.selectbox("Select Method ...",['Z-Score'],index=0)
    df =pd.DataFrame({})
    try:
        df =  st.session_state.data['file']
    except Exception:
        st.warning("DataSet Not Found...!")
    if method=='Z-Score':
        st.info("NOTE : This Method is Suggested to be used for Normaly Distributed Or Almost Normaly Distributed")
        cols =st.radio("Features",[x for x in df.columns if pd.api.types.is_numeric_dtype(df[x])],horizontal=True)
        col1,col2 = st.columns(2)
        try:
            col2.write(df[cols].describe())
            col1.subheader("Boundary Values : ")
            upper = round(df[cols].mean() + 3*df[cols].std(),2)
            lower = round(df[cols].mean() - 3*df[cols].std(),2)
            col1.write(f"Upper Limit : {upper}")
            col1.write(f"Upper Limit : {lower}")
            st.subheader(" Detected Outlier")
            st.write(df[(df[cols] > upper) |(df[cols] < lower )])
            st.subheader("Outlier Removal :")
            meth = st.selectbox("Method ",['Trimming','Capping'])
            if meth == 'Trimming':
                if st.button("Trim"):
                    df = df[(df[cols] < upper) & (df[cols] > lower )]
                    df.reset_index(drop=True,inplace=True)
                    # st.write(df)
                    # st.write(df.shape)
                    # st.success("Data Trimmed Succesfully...")   
                save_dataset(df)
            if meth == 'Capping':
                if st.button("Cap"):
                    df[cols]=np.where(df[cols] > upper,upper,np.where(df[cols] < lower,lower,df[cols]))
                save_dataset(df)
            # if st.button("Z-Score"):
            #     st.write((df[cols] - df[cols].mean())/df[cols].std())
            
        except Exception:
             st.warning("No Dataset Found ...")
        
            