import streamlit as st
import random

# Set page configuration
st.set_page_config(page_title="AI Chatbot", page_icon=":robot:")

# Initialize session state for chat history if not exists
if "messages" not in st.session_state:
    st.session_state.messages = []
st.markdown(
    
    <style>
        .stChatMessage {
            margin: 10px 0;
        }
        .stChatMessage .stText {
            padding: 10px 15px;
            border-radius: 15px;
            display: inline-block;
            max-width: 70%;
        }
        .stChatMessage.user .stText {
            background-color: #e1f5fe;
            color: #01579b;
            text-align: left;
        }
        .stChatMessage.assistant .stText {
            background-color: #e8f5e9;
            color: #2e7d32;
            text-align: left;
        }
        .stChatInput {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            padding: 15px 10px;
            background: #ffffff;
            box-shadow: 0px -2px 10px rgba(0, 0, 0, 0.1);
            z-index: 1000;
        }
        .stPage {
            background-color: #f5f5f5;
            padding-bottom: 80px; /* Space for the input box */
        }
    </style>
    
    unsafe_allow_html=True,
)

# Page title and description
st.title("🤖 AI Chatbot")
st.write("Chat with an AI assistant powered by Streamlit")

# Function to generate a simple AI response


def generate_response(user_message):
    # This is a placeholder response generator
    responses = [
        "That's an interesting point!",
        "Tell me more about that.",
        "I'm not sure I fully understand. Could you elaborate?",
        "Interesting perspective.",
        "How does that make you feel?"
    ]
    return random.choice(responses)


# Chat input
if prompt := st.chat_input("Enter your message"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Generate and display AI response for the latest user message
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant"):
        response = generate_response(st.session_state.messages[-1]["content"])
        st.write(response)
        st.session_state.messages.append(
            {"role": "assistant", "content": response})
