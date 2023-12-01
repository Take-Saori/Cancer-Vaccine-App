import streamlit as st
import plotly.express as px
import pandas as pd
from allele_data_utils import allele_analysis as aa

if 'geo_searched' not in st.session_state:
    st.session_state.geo_searched = False

if 'filter_allele_searched' not in st.session_state:
    st.session_state.filter_allele_searched = False

st.header('Allele Frequency Database')
st.write('**The Allele Frequency Net Database (AFND)** was originally designed to provide a resource for the storage of frequency data on the\
        polymorphisms of several immune related genes, including the human leukocyte antigens (HLA) system, killer-cell immunoglobulin-like\
        receptors (KIR), major histocompatibility complex class I chain-related genes (MIC), and a number of cytokine gene polymorphisms.')

st.write('---')
col1, col2, col3 = st.columns(3)
col1.metric("Number of Unique studies", str(aa.get_unique_studies_num()))
col2.metric("Number of Regions (e.g. South East Asia, Western Europe)", str(aa.get_regions_num()))
col3.metric("Number of Countries", str(aa.get_countries_num()))
st.write('---')

st.subheader('Number of studies per Continent')
st.plotly_chart(aa.get_pop_per_continent_fig())
st.subheader('Number of studies per Region')
st.plotly_chart(aa.get_pop_per_region_fig())
st.subheader('Number of studies per Country')
st.write('(Only the top 20 countries are displayed.)')
st.plotly_chart(aa.get_pop_per_country_fig())
st.write('---')

st.subheader('Filters:')
col1, col2, col3, col4 = st.columns([2,2,2,1])
with col1:
    continent = st.selectbox(
        'Select Continent',
        aa.get_all_continent(),
        index=None,
        placeholder="---",
    )
with col2:
    region = st.selectbox(
        'Select Region',
        aa.get_all_region(),
        index=None,
        placeholder="---",
    )

with col3:
    country = st.selectbox(
        'Select Country',
        aa.get_all_country(),
        index=None,
        placeholder="---",
    )

with col4:
    st.markdown("<div style='padding-top: 33%;'></div>",
                              unsafe_allow_html=True)
    filter_allele_search = st.button('Search', key='filter_allele_search')

st.write('**Only 1 filter is allowed for each search.**')

filter_list = [continent, region, country]

if filter_list.count(None) == 3 and filter_allele_search: # nothing is selected
    st.warning('Please select a filter.')

elif filter_list.count(None) == 1 and filter_allele_search: # more than 1 filter is selected
    st.warning('Please select only 1 filter at a time.')

elif filter_list.count(None) == 2 and (filter_allele_search or st.session_state.filter_allele_searched):
    st.session_state.filter_allele_searched = True

    exp_pop_size_dict = aa.filter_and_analyze_with_expected_population_size(country, region, continent)
    
    if len(exp_pop_size_dict["Top 20 HLA Alleles by Expected Population Size"]) == 0:
        st.write("No HLA Alleles found")

    else:
        # Create a DataFrame with the sorted data
        data = pd.DataFrame({'Allele': exp_pop_size_dict["Top 20 HLA Alleles by Expected Population Size"].index, 'Value': exp_pop_size_dict["Top 20 HLA Alleles by Expected Population Size"].values})

        # Plot the bar chart using Plotly Express
        fig = px.bar(data, x='Allele', y='Value',
                    color_discrete_sequence=['blue'])
        st.plotly_chart(fig)

st.write('---')


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
    search = st.button('Search', key='two_allele_search')

if search or st.session_state.geo_searched:

    st.session_state.geo_searched = True

    if allele_1 == allele_2:
        selected_alleles = allele_1
    else:
        selected_alleles = allele_1 + ', ' + allele_2

    fig = aa.update_choropleth(selected_alleles)
    st.plotly_chart(fig)