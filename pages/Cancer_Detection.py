import streamlit as st

st.header('Cancer Image Detection')

image_file = st.file_uploader("Upload Cancer Image in JPG/JPEG or PNG file.", ['.jpg', '.png'],
                                help='Please upload image that may indicate cancer.')

if image_file is None:
    st.info('Please upload image file.')

