import streamlit as st
from IEDB_utils import IEDB_database_utils as iedb

st.header('IEDB Peptide Database')

peptide = st.text_input('Enter Peptide', '')

if peptide:
    peptide_data = iedb.get_peptide_data(peptide)

    st.write('---')
    st.header('Results:')

    for key, value in peptide_data.items():
        st.subheader(key)
        for item in value:
            st.write(item)