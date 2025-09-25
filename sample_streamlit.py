import streamlit as st

st.set_page_config(page_title="Welcome App", layout="centered")
st.title(" Welcome to My Streamlit App!")
st.subheader("We're glad you're here!")
uploaded_image = st.file_uploader("Upload your image", type=["png", "jpg", "jpeg"])

if uploaded_image is not None:
    st.image(uploaded_image, caption="Your Uploaded Image", use_column_width=True)
else:
    st.info(" Please upload an image to display here.")
st.markdown("---")
st.caption("This is a basic Streamlit GUI to welcome users with their image.")
