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

st.header('Tumour Image Detection')

st.markdown('<h4>Upload image to detect for tumour.</h4>', unsafe_allow_html=True)

image_file = st.file_uploader("Upload Tumour Image in JPG/JPEG or PNG file.", ['.jpg', '.png'],
                                help='Please upload image that may indicate tumour.')
st.write('---')

if image_file is None:
    st.info('Please upload image file.')

else:
    image = image_file.read()
    col1, col2, col3 = st.columns([1,3,1])
    with col1:
        pass
    with col2:
        get_tumour_pred_result(image)
        st.write('---')
        st.markdown("<h4 style='text-align: center;text-decoration: underline;'>Uploaded image</h4>", unsafe_allow_html=True)
        st.image(image, use_column_width=True)
    with col3:
        pass
    
