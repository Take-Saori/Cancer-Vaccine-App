import streamlit as st

# random used for placeholder (temporary use) only, delete later
import random

st.header('Tumour Image Detection')

st.markdown('<h4>Upload image to detect for tumour.</h4>', unsafe_allow_html=True)

image_file = st.file_uploader("Upload Cancer Image in JPG/JPEG or PNG file.", ['.jpg', '.png'],
                                help='Please upload image that may indicate tumour.')
st.write('---')

if image_file is None:
    st.info('Please upload image file.')

else:
    image = image_file.read()
    st.markdown("<h4 style='text-align: center;'>Uploaded image</h4>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,3,1])
    with col1:
        pass
    with col2:
        st.image(image, use_column_width=True)
    with col3:
        pass

    st.write('---')

    # PLaceholder values below
    have_cancer = round(random.random())

    if have_cancer == 0:
        st.markdown(f"<h4 style='text-align: center;'>Probability of Tumour: 0%</h4>", unsafe_allow_html=True)

    else:
        cancer_prob = 80
        st.markdown(f"<h4 style='text-align: center;'>Probability of Tumour: {cancer_prob}</h4>", unsafe_allow_html=True)
        
