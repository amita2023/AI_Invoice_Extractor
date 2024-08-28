import os
from dotenv import load_dotenv
import streamlit as st # type: ignore
from PIL import Image
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Google Gemini Pro Vision API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Gemini Pro Vision model
model = genai.GenerativeModel('gemini-pro-vision')


def get_gemini_response(input, image, prompt):
    try:
        response = model.generate_content([input, image[0], prompt])
        return response.text
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else: 
        raise FileNotFoundError("No file uploaded")

# Initialize Streamlit app
# Title of the app
st.set_page_config(page_title = "MultiLanguage Invoice Extractor")

# Subheader
st.header("MultiLanguage Invoice Extractor")

# Adding text
st.write("Hello, World! This is my first Streamlit app.")


# Adding a text input widget
input = st.text_input("Input Prompt:", key="input")
uploaded_file = st.file_uploader("Choose an image of the invoice....:", type=["jpg", "jpeg", "png"] )

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption= "Uploaded Image.", use_column_width =True)

submit = st.button("Tell me about invoice")

input_prompt="""

You are an expert in understanding invoices. We will upload a an image as invoice and 
you will have to answer any questions based on uploaded invoice image

"""

# If submit button is clicked
if submit:
    image_data = input_image_details(uploaded_file)
    response = get_gemini_response(input_prompt,image_data,input)
    st.subheader("The Response is")
    st.write(response)