import streamlit as st
from streamlit_player import st_player

def render_consumer():

    st.markdown("<h2 style='text-align: center;\
                    text-decoration: underline;\
                    padding-bottom: 7%;'>About your Cancer</h2>",
                    unsafe_allow_html=True)
    st.write('Paragraph about your cancer')
    st.write('---')


    st.markdown("<h2 style='text-align: left;\
                    text-decoration: underline;\
                    padding-bottom: 7%;'>Self Care</h2>",
                    unsafe_allow_html=True)

    # Embed a youtube video
    url = "https://youtu.be/CmSKVW1v0xM"
    col1, col2 = st.columns([1,1])
    with col1:
        st.write('Paragraph about self-care')
    with col2:
        st.video(url)

    st.write('---')

    st.markdown("<h2 style='text-align: left;\
                    text-decoration: underline;\
                    padding-bottom: 7%;'>Resources</h2>",
                    unsafe_allow_html=True)
    
    # Placeholder references
    references = ['about ref', 'self care ref', 'resources ref']
    for i in range(len(references)):
        st.write(f'{i+1}. {references[i]}')