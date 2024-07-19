
import streamlit as st
from streamlit_option_menu import option_menu
import seaborn as sb
import matplotlib.pylab as plt
import pandas as pd
import numpy as np
# from sklearn.decomposition import PCA
st.set_page_config(
    page_title="Data Processing & Feature Engineering"
)

def load_data():
    file = st.file_uploader('Upload Your Dataset')
    if file:
        st.success("Dataset Upload")
        df = pd.read_csv(file)
        df = pd.DataFrame(df)
        return df

def home():
    st.header("Data Engineering Tool")
    # st.image('static/home1.webp',width=800)
    # file = st.file_uploader('Upload Your Dataset')
    file = load_data()
    if file is not None:
        if 'data' not in st.session_state:
            st.session_state.data = {}
        # st.success("Dataset Upload")
        df = file
        st.session_state.data['file'] = df
        with st.container(border=True):
            st.subheader('1. Dataset')
            st.write(df)
        with st.container(border=True):
            st.subheader('2. Mathematical Discription')
            st.write(df.describe())
        with st.container(border=True):
            st.subheader('3. Missing Values')
            miss = df.isnull().sum().to_dict()
            st.table(miss)
        with st.container(border=True):
            st.subheader('4. Dataset Size')
            st.write(f"Shape Of DataSet : {df.shape}")
        with st.container(border=True):
            st.subheader('5. Duplicate Values')
            if df.duplicated().sum() == 0:
                st.success("There Are No Duplicate Freatures..!!!")
            else:
                st.warning("There Are Some Duplicate Freatures ...!!")
        with st.container(border=True):
            st.subheader('6. Corealtion Of Freatures')
            st.write(df.corr(numeric_only=True))
        
        with st.container(border=True):
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
        with st.container(border=True):
            st.subheader('8.Non -  Numerical Column :')
            try:
                cols =st.radio("Features",[x for x in df.columns if not pd.api.types.is_numeric_dtype(df[x])],horizontal=True)
                cola,colb = st.columns(2)
                cola.write(cols)  
                cola.write(df[cols])
                colb.subheader("Description : ")
                colb.write(df[cols].describe())
            except Exception:
                st.info("Non-Numberical Data Not Found...!")

def select_columns(dataframe, columns):
    try:
        selected_df = dataframe[columns]
        return selected_df
    except KeyError:
        print("Error: One or more columns are not found in the DataFrame.")
        return None

def clean():
    # st.header("Data Cleaning")
    # st.image("static/dataCleaning.png",width=800)
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
        with st.container(border=True):
            features = st.multiselect("Freature",cols,default=cols)
            st.write(df.shape)
        with st.container(border=True):
            df = select_columns(df,features)
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
        with st.container(border=True):
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


def analysis():
    st.header('Exploratory Data Analysis')
    # st.image('static/eda.jpg',width=700)
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
            with st.container(border=True):
                st.subheader('Count Plot')
                # col1,col2 = st.columns(2)
                col = st.radio("Features",[x for x in df.columns],horizontal=True)
            with st.container(border=True):
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
            with st.container(border=True):
                try:
                    fig, ax = plt.subplots()
                    sb.distplot(x=df[col], ax=ax,hist=hist)
                    st.pyplot(fig)  
                except Exception:
                    st.warning("Unsupported Format ...!!!")
    if app == 'Bivariant':
        method = st.selectbox("Select Method",['scatter-plot','bar-plot'])
        with st.container(border=True):
            x = st.radio("X-Axis",[x for x in df.columns],horizontal=True)
        with st.container(border=True):        
            y = st.radio("Y-Axis",[x for x in df.columns],horizontal=True)
        if method == 'scatter-plot':
            # col1,col2 = st.columns(2)
            st.subheader('Scatter Plot')
            with st.container(border=True):
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
            with st.container(border=True):
                fig, ax = plt.subplots()
                scatter = ax.bar(df[x], df[y])
                ax.set_xlabel(x)
                ax.set_ylabel(y)
                st.pyplot(fig)


def missval():
    st.title("Missing Values")
    # st.image('static/missingData.jpg',width=600)
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
    with st.container(border=True):
        st.write(miss)
    if app=='Drop':
        try:
            if st.button("Drop None Values"):
                df = df.dropna()
                df = df.reset_index(drop=True)
                st.session_state.data['file'] = df
                with st.container(border=True):
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
             

def save_dataset(df):
    try:
        st.session_state.data['file'] = df
        st.write(df)
        st.write(df.shape)
        st.success("Data Saved Successfully...")
    except Exception:
                st.info("Data Already Saved ...")

def outlier():
    st.title("Outlier Page")
    # st.image('static/outlier.jpg',width=700)
    with st.container(border=True):
        method = st.selectbox("Select Method ...",['Z-Score'],index=0)
        st.info("NOTE : This Method is Suggested to be used for Normaly Distributed Or Almost Normaly Distributed")
    df =pd.DataFrame({})
    try:
        df =  st.session_state.data['file']
    except Exception:
        st.warning("DataSet Not Found...!")
    if method=='Z-Score':
        with st.container(border=True):
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
            with st.container(border=True):
                st.write(df[(df[cols] > upper) |(df[cols] < lower )])
            st.subheader("Outlier Removal :")
            with st.container(border=True):
                meth = st.selectbox("Method ",['Trimming','Capping'])
            if meth == 'Trimming':
                if st.button("Trim"):
                    df = df[(df[cols] < upper) & (df[cols] > lower )]
                    df.reset_index(drop=True,inplace=True)
                    # st.write(df)
                    # st.write(df.shape)
                    # st.success("Data Trimmed Succesfully...")   
                with st.container(border=True):
                    save_dataset(df)
            if meth == 'Capping':
                if st.button("Cap"):
                    df[cols]=np.where(df[cols] > upper,upper,np.where(df[cols] < lower,lower,df[cols]))
                with st.container(border=True):
                    save_dataset(df)
            # if st.button("Z-Score"):
            #     st.write((df[cols] - df[cols].mean())/df[cols].std())
            
        except Exception:
             st.warning("No Dataset Found ...")


def encoding():
    st.title("Encoding Page")
    # st.image('static/ohe.png',width=700)
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
                col2.subheader("Data:")
                col2.write(df[col])
        else:
            st.warning("No non-numeric columns found.")
    except Exception as e:
        st.warning(f"No Data Found: {e}")
    with st.container(border=True):
        st.subheader("One Hot Encoding ...")
        st.write(df.shape)
    try:
        df_encoded = pd.get_dummies(df, columns=col,dtype=int)
        with st.container(border=True):
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

# def pca():
    # st.header('PCA')
    # df = pd.DataFrame({})
    # try:
    #     df =  st.session_state.data['file']
    # except Exception:
    #     st.warning("DataSet Not Found...!")
    # st.write(df)
    # y  = [x for x in df.columns]
    # n = st.number_input('Principle Component : ',max_value=len(y),value=len(y),step=1,min_value=1)
    # if st.button("Apply "):
    #     pca = PCA(n_components=n)
    #     x = pca.fit_transform(df)
    #     with st.container(border=True):
    #         st.subheader("PCA")
    #         st.write(x)
    #     with st.container(border=True):
    #         st.subheader("PCA Eigen-Vectors")
    #         st.write(pca.components_)
    #     with st.container(border=True):
    #         st.subheader("PCA Components [ Eigen-Values] : ")
    #         st.write(pca.explained_variance_ratio_)
    #         st.write(pca.get_covariance())
    # st.info("Page Is Under Construction ...!!!!!")
                
def about():
    st.title("About Us")
    with st.container(border=True):
        # st.subheader("Name : Gaurav Santosh Kadam")
        # st.text('''Hello Everyone,''')
        st.header("Data Preprocessing Tool")
        st.markdown('''
Our Data Preprocessing Tool is a comprehensive solution designed to streamline and enhance your data analysis workflow. This versatile tool is equipped with a variety of powerful features to ensure your data is clean, accurate, and ready for analysis. Key functionalities include:

- **Data Cleaning**: Automatically identify and correct or remove errors and inconsistencies in your dataset, ensuring high-quality data.
- **Missing Value Handling**: Efficiently manage and impute missing data to maintain the integrity of your dataset.
- **Outlier Detection and Elimination**: Utilize the z-score method to detect and remove outliers, ensuring your data's statistical validity.
- **Encoding Categorical Data**: Seamlessly convert categorical data into numerical format, enabling effective analysis and modeling.
- **Exploratory Data Analysis (EDA)**: Gain insights into your data with a suite of EDA tools, including visualizations and summary statistics, to better understand patterns and relationships within your dataset.

Empower your data analysis with our Data Preprocessing Tool, designed to save time and enhance the accuracy of your results.
  ''')
    with st.container(border=True):
        st.header("Advantages of the Data Preprocessing Tool")
        st.markdown(''' 
1. **Ease of Use**: User-friendly interface designed for both beginners and experienced data analysts.
2. **Comprehensive Cleaning**: Automatically detects and corrects data errors and inconsistencies.
3. **Efficient Missing Value Handling**: Simple and effective methods for detecting and imputing missing values.
4. **Outlier Management**: Utilizes the z-score method to identify and eliminate outliers, ensuring robust analysis.
5. **Categorical Data Encoding**: Seamlessly converts categorical variables into numerical format, facilitating various analytical methods.
6. **Exploratory Data Analysis (EDA)**: Provides essential EDA tools to help users understand data distributions and relationships through visualizations and summary statistics.
7. **Time-Saving**: Automates many repetitive preprocessing tasks, saving significant time and effort.
8. **Improved Data Quality**: Ensures higher data quality, leading to more accurate and reliable analysis results.
9. **Consistency**: Standardizes preprocessing steps, ensuring consistent results across different datasets.
10. **Accessibility**: Accessible to users with various levels of technical expertise, making data preprocessing more inclusive.
''')
    with st.container(border=True):
        st.header("Limitations of the Data Preprocessing Tool")
        st.markdown('''
1. **Limited File Formats**: Currently supports only CSV and Excel file formats for data upload.
2. **Fixed Outlier Detection Method**: Uses only the z-score method for outlier detection and elimination, which may not be suitable for all datasets.
3. **Basic Imputation Techniques**: Offers basic imputation methods for missing values, which may not be adequate for complex missing data patterns.
4. **Limited Encoding Options**: Provides standard encoding techniques for categorical data, which might not cover all encoding needs.
5. **Scalability Issues**: May experience performance issues with extremely large datasets.
6. **Customization Constraints**: Limited options for customizing the preprocessing steps to specific user requirements.
7. **No Integration with External Tools**: Lacks integration with other data analysis and machine learning tools.
8. **User Interface Limitations**: The current user interface may not support advanced interactions or visualizations.
9. **No Reverse Processing**: If you edit and save your data it cannot be undo.
10. **Lack of Advanced EDA Features**: Basic exploratory data analysis tools, without advanced statistical analysis or machine learning integration.
''')
    with st.container(border=True):
        st.header("Areas for Improvement")
        st.markdown("""
1. **Support for More File Formats**: Expanding file format compatibility to include JSON, XML, and other common data formats.
2. **Advanced Outlier Detection Methods**: Incorporating additional outlier detection techniques such as IQR, DBSCAN, and isolation forests.
3. **Expanded Encoding Options**: Including additional encoding techniques such as ordinal encoding, frequency encoding, and label encoding.
4. **Scalability Enhancements**: Improving performance to handle larger datasets efficiently.
5. **Customization Flexibility**: Allowing users to customize preprocessing steps to better meet their specific requirements.
6. **Integration with External Tools**: Enabling seamless integration with other data analysis and machine learning tools such as Pandas, Scikit-learn, TensorFlow, and PyTorch.
7. **Improved Error Handling**: Enhancing error handling and debugging features to assist users in troubleshooting issues.
8. **Advanced EDA Features**: Incorporating more advanced exploratory data analysis tools, including statistical tests, correlation analysis, and predictive modeling capabilities.
9. **Documentation and Tutorials**: Providing comprehensive documentation, tutorials, and examples to help users make the most of the tool's features.
""")
    
    # st.download_button('Download Dataset',df.to_csv())
    # st.link_button("LINKED-IN",url='https://www.linkedin.com/in/gaurav-kadam-093b75242/')
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
    home()
if app == 'Data-Cleaning':
    clean()
if app =='EDA':
    analysis()
if app =='Missing-Val':
    missval()
if app =='Outlier':
    outlier()
if app == 'Encoding':
    encoding()
# if app=='PCA':
#     pca()
if app =='About':
    about()
