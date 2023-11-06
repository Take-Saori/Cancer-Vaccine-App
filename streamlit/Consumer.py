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

    st.write('---')

    with st.container():
            subcol1, subcol2, subcol3 = st.columns([2,1,1])
            with subcol1:
               st.markdown("<h5 style='padding-top: 2%; text-align: right;'>Download as: </h2>",
                           unsafe_allow_html=True)
            with subcol2:
               st.button('PDF')
            with subcol3:
               pass
