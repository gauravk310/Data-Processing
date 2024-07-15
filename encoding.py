import streamlit as st
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OrdinalEncoder

def app():
    st.title("Encoding Page")
    st.image('static/ohe.png',width=700)
    df = pd.DataFrame({})
    try:
        df =  st.session_state.data['file']
    except Exception:
        st.warning("DataSet Not Found...!")
    col1, col2 = st.columns(2)
    try:
        cols = [x for x in df.columns if not pd.api.types.is_numeric_dtype(df[x])]
        if cols:
            check = col1.checkbox("SHOW DATA", value=False)
            # count = col2.checkbox("Value Count ",value=False)
            col = col1.multiselect("Features", cols)
            # if count:   
            #     col2.subheader("Feature Value Count:")
            #     col2.write(df[cols].value_counts())
            if check:
                col1.subheader("Data:")
                col1.write(df[col])
        else:
            st.warning("No non-numeric columns found.")
    except Exception as e:
        st.warning(f"No Data Found: {e}")
    st.subheader("One Hot Encoding ...")
    st.write(df.shape)
    try:
        df_encoded = pd.get_dummies(df, columns=col,dtype=int)
        st.write(df_encoded)
        st.subheader("Categories:")
        cat = [x for x in df_encoded.columns.tolist() if x not in df.columns.to_list()]
        st.table(cat)
    except Exception:
        st.info("No Data Found ...")
    try:
        if st.button("Save Dataset"):
            st.session_state.data['file'] = df_encoded
            st.write(df_encoded)
            st.write(df_encoded.shape)
            st.success("Data Saved Successfully...")
    except Exception:
        st.info("Data Already Saved ...")

                
        


