import streamlit as st
from streamlit_option_menu import option_menu
import home,missval,encoding,analysis,outlier,about,clean

st.set_page_config(
    page_title="Data Processing & Feature Engineering"
)


class MultiApp:
    def __init__(self):
        self.apps = []
    
    def add_app(self,title,fun):
        self.apps.append({
            "title":title,
            'function':fun
        })
    def run(self):
        with st.sidebar:
            app = option_menu(
                menu_title="Data Processing",
                options=['Home','Data-Cleaning','Missing-Val','Outlier','Encoding','EDA','About'],
                icons=['house-fill','file-text','bar-chart','table','pie-chart','calendar','person'],
                menu_icon='graph-up',
                default_index=0,
                styles={
                    'container':{'padding':'5 !importnant','background-color':'black'},
                    'icon':{'color':'white','font-size':'25px'},
                    'nav-link':{'color':'white','font-size':'20px','text-align':'center'},
                    'nav-link-selected':{'background-color':'#02ab21'}
                }
            )
        if app =='Home':
            home.app()
        if app == 'Data-Cleaning':
            clean.app()
        if app =='EDA':
            analysis.app()
        if app =='Missing-Val':
            missval.app()
        if app =='Outlier':
            outlier.app()
        if app == 'Encoding':
            encoding.app()
        if app =='About':
            about.app()
        
app = MultiApp()
app.run()