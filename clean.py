import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

def select_columns(dataframe, columns):
    try:
        selected_df = dataframe[columns]
        return selected_df
    except KeyError:
        print("Error: One or more columns are not found in the DataFrame.")
        return None



def app():
    # st.header("Data Cleaning")
    st.image("static/dataCleaning.png",width=800)
    df = pd.DataFrame({})
    try:
        df =  st.session_state.data['file']
    except Exception:
        st.warning("DataSet Not Found...!")
    
    app = option_menu(
                menu_title="Data Cleaning",
                options=['Columns','Rows'],
                icons=['table','table'],
                default_index=0,
                styles={
                    'container':{'padding':'5 !importnant','background-color':'dark'},
                    'icon':{'color':'white','font-size':'25px'},
                    'nav-link':{'color':'white','font-size':'20px','text-align':'center'},
                    'nav-link-selected':{'background-color':'#02ab21'}
                },orientation='horizontal'
            )
    if app=='Columns':
        cols = [x for x in df.columns]
        features = st.multiselect("Freature",cols,default=cols)
        df = select_columns(df,features)
        st.write(df.shape)
        st.write(df)
        try:
            if st.button("Save Dataset"):
                st.session_state.data['file'] = df
                st.write(df)
                st.success("Data Saved Successfully...")
        except Exception:
            st.warning("Dataset Not Found ...")

    if app == 'Rows':    
        row = df.shape[0]
        st.write(df.shape)
        # st.write(df)
        st.write(df)
        index = st.multiselect("Select Index Of Row : ",options=[x for x in range(row)])
        try:
            if st.button("Save Dataset"):
                df1 = df.drop(index).reset_index(drop=True)
                st.session_state.data['file'] = df1
                st.write(df1.shape)
                st.write(df1)
                st.success("Data Saved Successfully...")
        except Exception:
            st.warning("No Dataset Found ...")

    