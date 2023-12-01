import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import io
import pickle
import json
from binding_pred_utils import binding_predictor as b_pred

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
        file_name='protein_sequences.xlsx',  # You can change the file name here
        key='excel-download'
    )

def download_csv(df):
   # Convert df to csv file to prepare for download
   csv = convert_df(df)

   st.download_button(
         label="CSV",
         data=csv,
         file_name='protein_sequences.csv',
         mime='text/csv',
      )

if "display_prediction" not in st.session_state:
   st.session_state.display_prediction = False


# --- USER AUTHENTICATION ---------------------------------------

# Load the names and corresponding usernames from the json file
file_path = "authentication/user_dict.json"
with open(file_path, 'r') as fp:
    user_dict = json.load(fp)
    
names = user_dict['names']
usernames = user_dict['usernames']

# Load hashed passwords
file_path = "authentication/hashed_pw.pkl"
with open(file_path, "rb") as file:
    hashed_passwords = pickle.load(file)

credentials = {"usernames":{}}
        
for uname,name,pwd in zip(usernames,names,hashed_passwords):
   user_pwd_dict = {"name": name, "password": pwd}
   credentials["usernames"].update({uname: user_pwd_dict})

authenticator = stauth.Authenticate(credentials, "researcher_access", "abcdef", cookie_expiry_days=30)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status == None:
    st.warning("Please enter your username and password")

#---------------------------------------------------------------

# --- If login successful --------------------------------------
if authentication_status:
   st.sidebar.title(f'Welcome {name}')
   authenticator.logout('Logout', 'sidebar')

   st.header("MHC-I Binding Affinity Pipeline")
   st.write('The tools in this group take amino acid sequences and MHC alleles as input to predict the strength of the peptide : MHC interaction. To make comparisons between alleles\
            and methods more standardized, a percentile rank score is also returned where lower indicates stronger binding. The percentile rank is the fraction of peptides drawn\
            randomly from Uniprot that would bind as well as or better than the current peptide.')
   st.write('*Industry standard MHCFlurry, NetMHCPan & NetMHCPan-EL models are available. More models will be made available in the next release.\
            The IEDB currently recommends using the percentile rank as the metric for ranking binding predictions. A percentile rank of <= 1\% has been\
            demonstrated to cover 80\% of the immune response for many alleles.*')
   
   st.subheader('MHCFlurry')
   st.write('MHCflurry implements class I peptide/MHC binding affinity prediction. The current version provides pan-MHC I predictors supporting any MHC allele\
               of known sequence. MHCflurry also includes two expermental predictors, an "antigen processing" predictor that attempts to model MHC alleleindependent effects such as proteosomal cleavage and a "presentation" predictor that integrates processing predictions with binding affinity\
               predictions to give a composite "presentation score." Both models are trained on mass spec-identified MHC ligands.')
   
   st.write('---')

   st.markdown("<h4 style='padding-bottom: 5%;'>Upload Peptide list and Cell lines to search for possible compatible protein sequences.</h4>", unsafe_allow_html=True)

   with st.container():
      col1, col2, col3 = st.columns([3,3,1])

      with col1:
         peptides_df = st.file_uploader("Upload Peptide List excel sheet", ['.xlsx'],
                                          help='Please upload excel sheet with list of peptide.')
         if peptides_df is not None:
            # To read file as bytes:
            peptides_df = pd.read_excel(peptides_df, engine='openpyxl')

      with col2:
         cell_lines_df = st.file_uploader("Upload Cell Lines excel sheet", ['.xlsx'],
                                          help='Please upload excel sheet with list of Cell lines.')
         if cell_lines_df is not None:
            # To read file as bytes:
            cell_lines_df = pd.read_excel(cell_lines_df, engine='openpyxl')

      with col3:
         st.markdown("<div style='padding-top: 37%;'></div>",
                              unsafe_allow_html=True)
         search = st.button('Search')

   # Error prompts to direct user
   if peptides_df is None:
      st.info('Please upload Peptide List excel sheet.')

   if cell_lines_df is None:
      st.info('Please upload Cell Lines excel sheet.')

   if peptides_df is not None and cell_lines_df is not None and not search and st.session_state.display_prediction == False:
      st.info('Please click \'Search\' to search for protein sequence.')

   st.write('---')
   
   # Once file is uploaded and search is clicked, 
   if peptides_df is not None and cell_lines_df is not None:
      if search or st.session_state.display_prediction == True:

         with st.spinner('Predicting possible protein binding...'):
            prediction_df = b_pred.get_binding_prediction(peptides_df, cell_lines_df)
            prediction_df.sort_values(by='prediction_percentile', inplace=True)
            prediction_df.reset_index(drop=True, inplace=True)
            st.session_state.display_prediction = True

         st.markdown("<h2 style='text-align: center;\
                     text-decoration: underline;'>Consolidated possible protein binding</h2>",
                     unsafe_allow_html=True)
         st.markdown("<p style='text-align: center;\
                     padding-bottom: 5%;'>(Only top 100 sequences are shown. Please download the sequences to see the whole output.)</p>",
                     unsafe_allow_html=True)

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
                  download_csv(prediction_df)
               with subcol3:
                  download_excel(prediction_df)
         with col3:
            pass

         # I am assuming the csv file loaded have the following column names. Will change later.
         df = prediction_df.rename(columns={'peptide': 'Peptide',
                                          'allele': 'Allele',
                                          'prediction': 'Prediction',
                                          'prediction_low': 'Prediction Low',
                                          'prediction_high': 'Prediction High',
                                          'prediction_percentile': 'Prediction Percentile',
                                          })
         
         st.dataframe(df[:100])