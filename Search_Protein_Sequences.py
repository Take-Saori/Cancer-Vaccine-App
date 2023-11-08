import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import io
import pickle
from Consumer import render_consumer

@st.cache_data
def convert_df(df):
   # IMPORTANT: Cache the conversion to prevent computation on every rerun
   return df.to_csv().encode('utf-8')

def download_excel(df):
    # Convert the DataFrame to an Excel writer object
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Sheet1', index=False)
    
    # Set up the download link
    output.seek(0)
    st.download_button(
        label="Excel",
        data=output,
        file_name='data.xlsx',  # You can change the file name here
        key='excel-download'
    )

def download_csv(df):
   # Convert df to csv file to prepare for download
   csv = convert_df(df)

   st.download_button(
         label="CSV",
         data=csv,
         file_name='data.csv',
         mime='text/csv',
      )


# --- USER AUTHENTICATION ---------------------------------------
names = ["John Smith", "Satoshi Nakamoto"]
usernames = ["jsmith", "snakamoto"]

# load hashed passwords
file_path = "authentication/hashed_pw.pkl"
with open(file_path, "rb") as file:
# with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

credentials = {"usernames":{}}
        
for uname,name,pwd in zip(usernames,names,hashed_passwords):
   user_dict = {"name": name, "password": pwd}
   credentials["usernames"].update({uname: user_dict})

authenticator = stauth.Authenticate(credentials, "researcher_access", "abcdef", cookie_expiry_days=30)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status == None:
    st.warning("Please enter your username and password")

#---------------------------------------------------------------


if authentication_status:
   st.sidebar.title(f'Welcome {name}')
   authenticator.logout('Logout', 'sidebar')

   st.header("Search Protein Sequences")
   st.markdown("<h4 style='padding-bottom: 5%;'>Select cancer type and upload protein sequences to search for possible compatible protein sequences.</h4>", unsafe_allow_html=True)

   with st.container():
      col1, col2, col3 = st.columns([1,3,1])

      with col1:
         st.markdown("<div style='padding-top: 10%;'></div>",
                              unsafe_allow_html=True)
         option = st.selectbox(
            "Select Cancer Type",
            ('---', 'Lung', 'Throat', 'idk'),
            placeholder="Select Cancer Type",
         )

      with col2:
         uploaded_file = st.file_uploader("Upload Protein Sequence csv file", ['.csv'],
                                          help='Please upload csv file with protein sequences.')
         if uploaded_file is not None:
            # To read file as bytes:
            bytes_data = uploaded_file.getvalue()

            #  # Can be used wherever a "file-like" object is accepted:
            #  dataframe = pd.read_csv(uploaded_file)
            #  st.write(dataframe)

      with col3:
         st.markdown("<div style='padding-top: 37%;'></div>",
                              unsafe_allow_html=True)
         search = st.button('Search')

   # Error prompts to direct user
   if option == '---':
      st.info('Please select an option for Cancer Type in the dropdown.')

   if uploaded_file is None:
      st.info('Please upload CSV file to search for protein sequence.')

   if uploaded_file is not None and not search:
      st.info('Please click \'Search\' to search for protein sequence.')

   
   # Once file is uploaded and search is clicked, 
   if uploaded_file is not None and search:
      tab1, tab2 = st.tabs(["Researcher View", "Consumer View"])

      with tab1:
         st.markdown("<h2 style='text-align: center;\
                     text-decoration: underline;\
                     padding-bottom: 7%;'> Consolidated possible protein binding</h2>",
                     unsafe_allow_html=True)

         # Placeholder csv file, remove later
         csv_filename = 'test_data.csv'
         df = pd.read_csv(csv_filename)

         col1, col2, col3 = st.columns([1,2,1])
         with col1:
            pass
         with col2:
            with st.container():
               subcol1, subcol2, subcol3 = st.columns([2,1,1])
               with subcol1:
                  st.markdown("<h5 style='padding-top: 2%;'>Download as: </h2>",
                              unsafe_allow_html=True)
               with subcol2:
                  download_csv(df)
               with subcol3:
                  download_excel(df)
         with col3:
            pass


         # I am assuming the csv file loaded have the following column names. Will change later.
         df = df.rename(columns={'protein_seq': 'Protein Sequence', 'score': 'Score'})
         st.table(df)


      with tab2:
         render_consumer()