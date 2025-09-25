import streamlit as st
import base64
import requests

st.title("UN SDGs Content Generator")
st.subheader("Streamlit + Groq LLaMA Models")

GROQ_API_KEY = "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"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

sdg_themes = [
    "Climate Action", "Quality Education", "Gender Equality",
    "No Poverty", "Zero Hunger", "Clean Water and Sanitation"
]

st.header("Text Prompt-Based Generation")
selected_theme = st.selectbox("Select an SDG Theme", sdg_themes)
text_prompt = st.text_area("Enter your prompt for the selected SDG")

if st.button("Generate Text"):
    if text_prompt.strip():
        payload = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {"role": "system", "content": f"You are generating content for SDG theme: {selected_theme}."},
                {"role": "user", "content": text_prompt}
            ],
            "temperature": 0.7
        }

        response = requests.post(GROQ_API_URL, headers=headers, json=payload)

        if response.status_code == 200:
            output = response.json()['choices'][0]['message']['content']
            st.success("Generated Text:")
            st.write(output)
        else:
            st.error(f"Error {response.status_code}: {response.text}")
    else:
        st.warning("Please enter a text prompt.")

st.header("Image Prompt-Based Generation")

uploaded_image = st.file_uploader("Upload an image (Poster / Infographic) related to SDG", type=["jpg", "jpeg", "png"])

if uploaded_image:
    st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)
    image_description = st.text_area("Describe the image briefly for AI to generate a message")

    if st.button("Generate Image-Based Message"):
        if image_description.strip():
            payload = {
                "model": "meta-llama/llama-4-maverick-17b-128e-instruct",
                "messages": [
                    {"role": "system", "content": "You are generating a description/message for an SDG-related image."},
                    {"role": "user", "content": f"The image is described as: {image_description}"}
                ],
                "temperature": 0.7
            }

            response = requests.post(GROQ_API_URL, headers=headers, json=payload)

            if response.status_code == 200:
                output = response.json()['choices'][0]['message']['content']
                st.success("Generated Message:")
                st.write(output)
            else:
                st.error(f"Error {response.status_code}: {response.text}")
        else:
            st.warning("Please enter a short description of the image.")