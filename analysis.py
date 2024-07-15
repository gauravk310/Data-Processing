import streamlit as st
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
import seaborn as sb
import pandas as pd

def app():
    st.header('Exploratory Data Analysis')
    st.image('static/eda.jpg',width=700)
    df = pd.DataFrame({})
    try:
        df =  st.session_state.data['file']
    except Exception:
        st.warning("DataSet Not Found...!")
    
    app = option_menu(
                menu_title="Exploratory Data Analysis",
                options=['Univariant','Bivariant'],
                icons=['bar-chart','pie-chart'],
                default_index=0,
                styles={
                    'container':{'padding':'5 !importnant','background-color':'dark'},
                    'icon':{'color':'white','font-size':'25px'},
                    'nav-link':{'color':'white','font-size':'20px','text-align':'center'},
                    'nav-link-selected':{'background-color':'#02ab21'}
                },orientation='horizontal'
            )
    if app == 'Univariant':
        method = st.selectbox("Select Method",['count-plot','dist-plot'])
        if method == 'count-plot':
            st.subheader('Count Plot')
            # col1,col2 = st.columns(2)
            col = st.radio("Features",[x for x in df.columns],horizontal=True)
            try:
                fig, ax = plt.subplots()
                sb.countplot(x=col, data=df, ax=ax)
                st.pyplot(fig)
            except Exception:
                st.warning("Unsupported Format....!")
          
        if method == 'dist-plot':
            st.subheader('Distribution Plot')
            # col1,col2 = st.columns(2)
            col = st.radio("Features",[x for x in df.columns if pd.api.types.is_numeric_dtype(df[x])],horizontal=True)
            hist = st.checkbox("Hist",value=True)
            try:
                fig, ax = plt.subplots()
                sb.distplot(x=df[col], ax=ax,hist=hist)
                st.pyplot(fig)  
            except Exception:
                st.warning("Unsupported Format ...!!!")
    if app == 'Bivariant':
        method = st.selectbox("Select Method",['scatter-plot','bar-plot'])
        x = st.radio("X-Axis",[x for x in df.columns],horizontal=True)
        y = st.radio("Y-Axis",[x for x in df.columns],horizontal=True)
        if method == 'scatter-plot':
            # col1,col2 = st.columns(2)
            st.subheader('Scatter Plot')
            try:
                fig, ax = plt.subplots()
                scatter = ax.scatter(df[x], df[y], c=pd.Categorical(df[x]).codes, cmap='viridis')
                legend = ax.legend(*scatter.legend_elements(), title=x)
                ax.add_artist(legend)
                ax.set_xlabel(x)
                ax.set_ylabel(y)
                st.pyplot(fig)
            except Exception:
                st.warning("Unsupported Format .....!!!!")
        
        if method == 'bar-plot':
            # col1,col2 = st.columns(2)
            st.subheader('Bar Plot')
            fig, ax = plt.subplots()
            scatter = ax.bar(df[x], df[y])
            ax.set_xlabel(x)
            ax.set_ylabel(y)
            st.pyplot(fig)