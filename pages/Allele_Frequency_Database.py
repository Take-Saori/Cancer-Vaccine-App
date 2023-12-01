import streamlit as st
from allele_data_utils import allele_analysis as aa

if 'searched' not in st.session_state:
    st.session_state.searched = False

st.header('Allele Analysis')

col1, col2, col3 = st.columns([2,2,1])
allele_tuple = aa.get_all_allele()

with col1:
    allele_1 = st.selectbox(
    'Select Allele 1',
    allele_tuple)

with col2:
    allele_2 = st.selectbox(
    'Select Allele 2',
    allele_tuple)

with col3:
    st.markdown("<div style='padding-top: 22%;'></div>",
                              unsafe_allow_html=True)
    search = st.button('Search')

if search or st.session_state.searched:

    if allele_1 == allele_2:
        selected_alleles = allele_1
    else:
        selected_alleles = allele_1 + ', ' + allele_2

    fig = aa.update_choropleth(selected_alleles)
    st.plotly_chart(fig)