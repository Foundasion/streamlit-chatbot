import streamlit as st
import asyncio
from llm import get_llm_provider

# Initialize session state for message history if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

# Configure the page
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="💬",
    layout="wide"
)

st.title("AI Chatbot")

# Initialize LLM provider
llm = get_llm_provider()

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
if prompt := st.chat_input("What's on your mind?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.write(prompt)
    
    # Display assistant response with loading indicator
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        with st.spinner("Thinking..."):
            # Get response from LLM
            response = asyncio.run(llm.get_response(
                prompt,
                context=st.session_state.messages[:-1]  # Exclude the latest message
            ))
            message_placeholder.write(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Add a sidebar with basic instructions
with st.sidebar:
    st.header("About")
    st.write("""
    This is a simple AI chatbot built with Streamlit.
    It uses Claude to generate responses to your messages.
    
    Your chat history is preserved during the session.
    """)
    
    # Add a clear chat button
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()
