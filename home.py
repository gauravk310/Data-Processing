import streamlit as st
import pandas as pd

def load_data():
    file = st.file_uploader('Upload Your Dataset')
    if file:
        st.success("Dataset Upload")
        df = pd.read_csv(file)
        return df

def app():
    st.header("Data Engineering")
    st.image('static/home1.webp', width=800)

    if 'data' not in st.session_state:
        st.session_state.data = None

    if st.session_state.data is None:
        file = load_data()
        if file is not None:
            st.session_state.data = file
            st.success("Data loaded successfully!")

    if st.session_state.data is not None:
        df = st.session_state.data
        st.subheader('1. Dataset')
        st.write(df)

        st.subheader('2. Mathematical Description')
        st.write(df.describe())

        st.subheader('3. Missing Values')
        miss = df.isnull().sum().to_dict()
        st.table(miss)

        st.subheader('4. Dataset Size')
        st.write(f"Shape Of DataSet: {df.shape}")

        st.subheader('5. Duplicate Values')
        if df.duplicated().sum() == 0:
            st.success("There are no duplicate features!")
        else:
            st.warning("There are some duplicate features!")

        st.subheader('6. Correlation of Features')
        st.write(df.corr(numeric_only=True))

        st.subheader('7. Numerical Column:')
        try:
            cols = st.radio("Features", [x for x in df.columns if pd.api.types.is_numeric_dtype(df[x])], horizontal=True)
            cola, colb = st.columns(2)
            cola.subheader(cols)
            cola.write(df[cols])
            colb.subheader("Description:")
            colb.write(df[cols].describe())
        except Exception:
            st.info("Numerical columns not found!")

        st.subheader('8. Non-Numerical Column:')
        try:
            cols = st.radio("Features", [x for x in df.columns if not pd.api.types.is_numeric_dtype(df[x])], horizontal=True)
            cola, colb = st.columns(2)
            cola.write(cols)
            cola.write(df[cols])
            colb.subheader("Description:")
            colb.write(df[cols].describe())
        except Exception:
            st.info("Non-numerical data not found!")
