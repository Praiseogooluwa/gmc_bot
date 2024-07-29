import streamlit as st
import json
from bot import predict_class, get_response, recognize_entities
import random
import os

# Load the intents from the intents.json file
with open('intents.json', 'r') as file:
    data = json.load(file)

def get_response(return_list, data_json):
    # Default response if no intent is recognized
    result = "Sorry, I don't have an answer to that question, Drag the sidebar to chat with one of our active Educational consultant."
    
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
        response = get_response(return_list, data_json=intents)  # Pass intents dictionary
        st.text_area("OG's Response:", response, height=200)
        # Perform entity recognition
        entities = recognize_entities(message)
        st.write(f"Entities: {entities}")

# Path to the logo
logo_path = 'GMC/logo.png'  # Ensure the correct path

# Verify that the logo file exists
if os.path.exists(logo_path):
    st.set_page_config(page_title="GMC HELP/SUPPORT | By Praise Ogooluwa", page_icon=logo_path, layout="wide")
else:
    st.set_page_config(page_title="GMC HELP/SUPPORT | By Praise Ogooluwa", layout="wide")


# Add a header with the logo and navbar
st.markdown(
    f"""
    <div style="display: flex; align-items: center; justify-content: space-between; background-color: #e53935; padding: 10px;">
        <img src="{logo_path}" alt="Logo" width="150" style="float:left;"/>
        <h1 style="color: black; margin: 0;">GOMYC<span style="color: red;">O</span>DE</h1>
        <a href="https://wa.link/8b4aht" target="_blank" style="color: white; text-decoration: none;">Help/Support</a>
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

st.sidebar.markdown("# Contact Our Educational Consultant")

# Consultant profile
consultant_image_path = 'GMC/esther.jpg'  # Path to consultant's image

if os.path.exists(consultant_image_path):
    consultant_image_url = consultant_image_path  # Adjust if necessary
else:
    consultant_image_url = "https://via.placeholder.com/100"  # Placeholder image if not found

st.sidebar.markdown("### Meet Our Consultant")
st.sidebar.markdown(
    f"""
    <div style="display: flex; align-items: center;">
        <a href="https://wa.link/8b4aht" target="_blank">
            <img src="{consultant_image_url}" alt="Esther Abiona" style="border-radius: 50%; margin-right: 10px; cursor: pointer;" width="50">
        </a>
        <div>
            <strong>Esther Abiona</strong><br>
            <span style="display: inline-block; width: 10px; height: 10px; border-radius: 50%; background-color: green;"></span>
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

# Main app where user enters prompt and gets the response
user_input = st.text_area("You:", "", key="user_input")
generate_button = st.button("Generate Response")

# Chat history
chat_history = []
if generate_button and user_input.strip() != "":
    chat_history.append({"role": "user", "content": user_input})
    return_list = predict_class(user_input)
    response = get_response(return_list, data_json=data)
    chat_history.append({"role": "assistant", "content": response})

st.subheader("Chat History")
for message in chat_history:
    if message["role"] == "user":
        st.text_area("You:", value=message["content"], height=50, max_chars=200, key=f"user_history_{message['content']}", disabled=True)
    else:
        st.text_area("OG:", value=message["content"], height=500, key=f"chatbot_history_{message['content']}")

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
        .stTextInput>div>div>textarea {
            background-color: #ffffff;
            color: #333;
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 10px;
        }
        .stButton button {
            background-color: #e53935; /* Red color */
            color: white;
            font-weight: bold;
            border-radius: 5px;
            border: none;
            padding: 10px 20px;
        }
        .stButton button:hover {
            background-color: #c62828; /* Darker red on hover */
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
            color: #e53935; /* Red color */
        }
        .stMarkdown {
            color: #333;
        }
    </style>
    """,
    unsafe_allow_html=True,)

# Run the main function
main(data)
