import streamlit as st
import json
from bot import predict_class, get_response, recognize_entities
import random
import os
from PIL import Image
from io import BytesIO
import base64
import speech_recognition as sr
import PyAudio

# Load the intents from the intents.json file
with open('intents.json', 'r') as file:
    data = json.load(file)

def get_response(return_list, data_json):
    result = "Sorry, I don't have an answer to that question. Drag the sidebar to chat with one of our active Educational consultants."
    for intent in return_list:
        tag = intent['intent']
        for i in data_json['intents']:
            if i['tag'] == tag:
                result = random.choice(i['responses'])
                break
    return result

def main(intents):
    st.write("Enter your message:")
    message = st.text_input("", "")
    if st.button("Send"):
        return_list = predict_class(message)
        response = get_response(return_list, data_json=intents)
        st.text_area("GMC's Response:", response, height=200)
        #entities = recognize_entities(message)
        #st.write(f"Entities: {entities}")

# Open the logo image
logo_image = Image.open('logo1.png')

# Convert the image to a base64-encoded string
buffered = BytesIO()
logo_image.save(buffered, format="PNG")
logo_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

# Use the base64-encoded string in the img tag
st.markdown(
    f"""
    <div class="header">
        <img src="data:image/png;base64,{logo_base64}" alt="Logo" class="logo"/>
        <h1 class="title">GOMYC<span class="highlight">O</span>DE</h1>
        <a href="mailto:hello@gomycode.com?subject=Help%20and%20Support" target="_blank" class="support-link">Help/Support</a>
    </div>
    """,
    unsafe_allow_html=True
)
st.write("Made with love by - [Praise Ogooluwa Bakare](https://praiseogooluwa.github.io/)")
st.write("#### Welcome to GMC help and support! Type your message below:")

# Sidebar content
st.sidebar.markdown("# Technical Coding Information")
st.sidebar.markdown(
    """
    ## Programming Languages
    - Python
    - JavaScript
    - HTML/CSS
    - SQL
    """
)

st.sidebar.markdown("# Contact Our Educational Consultants")

# Consultant profile
consultant_image = Image.open('esther.jpg')

buffered = BytesIO()
consultant_image.save(buffered, format="JPEG")
consultant_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

# Consultant profile1
consultant_image1 = Image.open('dele.jpeg')

buffered = BytesIO()
consultant_image1.save(buffered, format="JPEG")
consultant_base164 = base64.b64encode(buffered.getvalue()).decode("utf-8")

# Consultant profile2
consultant_image2 = Image.open('tope.jpeg')

buffered = BytesIO()
consultant_image2.save(buffered, format="JPEG")
consultant_base264 = base64.b64encode(buffered.getvalue()).decode("utf-8")

# Consultant profile3
consultant_image3 = Image.open('praise.jpg')

buffered = BytesIO()
consultant_image3.save(buffered, format="JPEG")
consultant_base364 = base64.b64encode(buffered.getvalue()).decode("utf-8")

st.sidebar.markdown("### Meet Our Consultants")
st.sidebar.markdown(
    f"""
    <div class="consultant">
        <a href="https://wa.link/8b4aht" target="_blank">
            <img src="data:image/jpeg;base64,{consultant_base64}" alt="Esther Abiona" class="consultant-img">
        </a>
        <div>
            <strong>Esther Abiona</strong><br>
            <span class="status online"></span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
st.sidebar.markdown(
    f"""
    <div class="consultant">
        <a href="https://wa.link/kfpbnn" target="_blank">
            <img src="data:image/jpeg;base64,{consultant_base164}" alt="Dele Fayemi" class="consultant-img">
        </a>
        <div>
            <strong>Dele Fayemi</strong><br>
            <span class="status online"></span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
st.sidebar.markdown(
    f"""
    <div class="consultant">
        <a href="https://wa.link/d7gbl9" target="_blank">
            <img src="data:image/jpeg;base64,{consultant_base264}" alt="TemiTope Bamidele" class="consultant-img">
        </a>
        <div>
            <strong>Temitope Bamidele</strong><br>
            <span class="status online"></span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
st.sidebar.markdown(
    f"""
    <div class="consultant">
        <a href="https://wa.link/f7tm3h" target="_blank">
            <img src="data:image/jpeg;base64,{consultant_base364}" alt="Praise Ogooluwa" class="consultant-img">
        </a>
        <div>
            <strong>Praise Ogooluwa</strong><br>
            <span class="status offline"></span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown(
    """
    ## Leave a Message
    If you have any questions or need further assistance, feel free to <a href="https://wa.link/8b4aht" target="_blank">send a message via WhatsApp</a>.
    """,
    unsafe_allow_html=True
)

# Function to recognize speech and convert to text
def recognize_speech_from_mic(recognizer, microphone):
    with microphone as source:
        st.info("Adjusting for ambient noise, please wait...")
        recognizer.adjust_for_ambient_noise(source)
        st.info("Recording, speak now...")
        audio = recognizer.listen(source)
        st.info("Recognizing speech...")
        try:
            response = recognizer.recognize_google(audio)
        except sr.RequestError:
            response = "API unavailable"
        except sr.UnknownValueError:
            response = "Unable to recognize speech"
    return response

# Main app where user enters prompt and gets the response
user_input = st.text_area("You:", "", key="user_input")

# Add a microphone button
if st.button("🎤"):
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    user_input = recognize_speech_from_mic(recognizer, microphone)
    st.text_area("Recognized Text:", value=user_input, height=50, key="recognized_text")
    # Generate a response based on the recognized text
    return_list = predict_class(user_input)
    response = get_response(return_list, data_json=data)
    st.text_area("GMC's Response:", response, height=200)
generate_button = st.button("Generate Response")

# Chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if generate_button and user_input.strip() != "":
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    return_list = predict_class(user_input)
    response = get_response(return_list, data_json=data)
    st.session_state.chat_history.append({"role": "assistant", "content": response})

st.subheader("Chat History")
for message in st.session_state.chat_history:
    if message["role"] == "user":
        st.text_area("You:", value=message["content"], height=50, max_chars=200, key=f"user_history_{message['content']}", disabled=True)
    else:
        st.text_area("GMC:", value=message["content"], height=500, key=f"chatbot_history_{message['content']}")

# Additional styling to make the app visually appealing
st.markdown("""
    <style>
        body {
            font-family: 'Montserrat', sans-serif;
            background-color: #ffffff;
            color: #333;
        }
        .stApp {
            background-color: #f9f9f9;
        }
        .header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            background-color: #ffffff;
            border: 1px solid #e53935;
            box-shadow: 0 0 10px rgba(229, 57, 53, 0.5);
            padding: 10px;
            font-family: 'Times New Roman', serif;
        }
        .header .logo {
            width: 20%;
            max-width: 100px;
            float: left;
        }
        .header .title {
            color: black;
            margin: 0;
            font-family: 'Times New Roman', serif;
            font-size: 1.5em;
            flex-grow: 1;
            text-align: center;
        }
        .header .highlight {
            color: red;
        }
        .header .support-link {
            color: red;
            text-decoration: none;
            font-family: 'Times New Roman', serif;
            float: right;
            font-size: 1em;
        }
        .consultant {
            display: flex;
            align-items: center;
            margin-bottom: 10px;
        }
        .consultant .consultant-img {
            border-radius: 50%;
            margin-right: 10px;
            cursor: pointer;
            border: 1.5px solid red;
            width: 50px;
            height: 55px;
        }
        .status {
            display: inline-block;
            width: 10px;
            height: 10px;
            border-radius: 50%;
        }
        .status.online {
            background-color: green;
        }
        .status.offline {
            background-color: grey;
        }
        .stTextInput>div>div>textarea {
            background-color: #ffffff;
            color: #333;
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 10px;
        }
        .stButton button {
            background-color: #e53935;
            color: white;
            font-weight: bold;
            border-radius: 5px;
            border: none;
            padding: 10px 20px;
        }
        .stButton button:hover {
            background-color: #c62828;
        }
        .stTextArea>div>textarea {
            resize: none;
            background-color: #ffffff;
            color: #333;
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 10px;
        }
        .stTextArea>div>div>textarea {
            height: 100px;
        }
        .st-subheader {
            margin-top: 20px;
            font-size: 16px;
            color: #e53935;
        }
        .stMarkdown {
            color: #333;
        }

        /* Responsive styles */
        @media (max-width: 768px) {
            .header .logo {
                width: 15%;
                max-width: 75px;
            }
            .header .title {
                font-size: 1.2em;
            }
            .header .support-link {
                font-size: 0.9em;
            }
        }
        @media (max-width: 480px) {
            .header {
                flex-direction: column;
                text-align: center;
            }
            .header .logo {
                float: none;
                margin: 15px 3;
            }
            .header .logo, .header .support-link {
                float: none;
                margin: 10px 0;
            }
            .header .support-link {
                font-size: 1.5em;
            }
            .header .logo {
                width: 27%;  /* Increase the percentage to make the logo wider */
                max-width: 150px;  /* Increase the pixel value to make the logo larger */
                margin: 15px 0;
            }
            .header .title {
                font-size: 2.2em;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Run the main function
main(data)
