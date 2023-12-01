import streamlit as st
from tumour_pred_utils import tumour_pred as tumour 

def get_tumour_pred_result(image_data):
    # Class 0 means pathologists labelled the image as no tumour
    # Class 1 means they suspect and labelled that there is a tumour
    prediction = tumour.predict_cancer(image_data)
    color = tumour.gradient_color(prediction[0][1], 0, 1)
    st.markdown(
    f"<h2 style='text-align:center;'>Probability of Tumour is:</h2>",
    unsafe_allow_html=True
    )
    st.markdown(
    f"<h2 style='text-align:center;color:{color};'>{prediction[0][1]*100:.2f}%</h2>",
    unsafe_allow_html=True
    )

st.header('Tumour Prediction')
st.write('*Ensembled stacked Neural Nets models trained on carcinoma, sarcoma, myeloma, leukemia, lymphoma, with a 90.6\% accuracy on unseen test data.*')
st.write('**\*Please be aware that the following model is not constitute as medical advice and serves solely as an indicator of the potential presence of a tumour. It\
            is strongly recommended to seek confirmation through the analysis of a qualified pathologist.**')

st.markdown('<h4>Upload image to detect for tumour.</h4>', unsafe_allow_html=True)

image_file = st.file_uploader("Upload Tumour Image in JPG/JPEG or PNG file.", ['.jpg', '.png'],
                                help='Please upload image that may indicate tumour.')
st.write('---')

if image_file is None:
    st.info('Please upload image file.')

else:
    image = image_file.read()

    get_tumour_pred_result(image)
    st.write('---')

    col1, col2 = st.columns(2)
    with col1:
        st.image(image, use_column_width=True)
        st.markdown("<h4 style='text-align: center;text-decoration: underline;'>Original image</h4>", unsafe_allow_html=True)
    with col2:
        pass
    
