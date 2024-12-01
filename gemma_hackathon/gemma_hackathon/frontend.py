import streamlit as st
import random
from main import perform_rag_query
# Set page configuration
st.set_page_config(page_title="AI Chatbot", page_icon=":robot:")

# Initialize session state for chat history if not exists
if "messages" not in st.session_state:
    st.session_state.messages = []

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
        response = perform_rag_query(
            "./gemma_hackathon/AllStatus.csv", st.session_state.messages[-1]["content"])
        st.write(response)
        st.session_state.messages.append(
            {"role": "assistant", "content": response})
