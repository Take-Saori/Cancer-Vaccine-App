import streamlit as st
import io
import pandas as pd
from Pan_BA_utils import Pan_BA_func_utils as pan_ba

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

if 'searched_ba' not in st.session_state:
    st.session_state.searched_ba = False

st.header('NetMHCPan BA 4.1')

st.write('Predicts binding of peptides to any MHC molecule of the known sequence using artificial neural networks (ANNs). The BA data covers\
170 MHC molecules from human (HLA-A, B, C, E), mouse (H-2), cattle (BoLA), primates (Patr, Mamu, Gogo), swine (SLA) and equine (Eqca).')

st.markdown('Pubmed ID: [PMID: 32406916](https://pubmed.ncbi.nlm.nih.gov/32406916/)')

col1, col2, col3 = st.columns([2,2,1])

with col1:
    protein_seq = st.text_input('Enter Protein Sequnces', '')
with col2:
    allele = st.text_input('Enter HLA Alleles', '')
with col3:
    st.markdown("<div style='padding-top: 22%;'></div>",
                              unsafe_allow_html=True)
    search = st.button('Search')

if search or st.session_state.searched_ba:
    st.write('---')
    st.session_state.searched = True

    st.markdown("<h2 style='text-align: center;\
                     text-decoration: underline;'>Binding Affinities from Cell Line</h2>",
                     unsafe_allow_html=True)

    df = pan_ba.get_result_df(protein_seq, allele)
    
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

    st.dataframe(df)

