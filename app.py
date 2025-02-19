from typing import Optional
import streamlit as st

# Configure the page
st.set_page_config(
    page_title="AI Hub",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

from llm import get_llm_provider
from database.database import DatabaseManager
from ui.state import SessionState
from ui.components import render_sidebar, format_message, should_name_chat

# Initialize session state
SessionState.init_state()

st.title("AI Hub")

# Initialize LLM provider
llm = get_llm_provider()

def has_empty_chat(user_id: str) -> Optional[str]:
    """Check for empty chats and return the first empty chat ID if found."""
    chats = DatabaseManager.get_chats(user_id)
    for chat in chats:
        if len(DatabaseManager.get_messages(str(chat.id))) == 0:
            return str(chat.id)
    return None

# Get or create current chat
current_chat_id = SessionState.get_current_chat()
if not current_chat_id:
    user_info = SessionState.get_user_info()
    empty_chat_id = has_empty_chat(user_info["id"])
    
    if empty_chat_id:
        # Use existing empty chat
        current_chat_id = empty_chat_id
    else:
        # Create new chat only if no empty chats exist
        chat = DatabaseManager.create_chat(user_info["id"], "New Chat")
        current_chat_id = str(chat.id)
    
    SessionState.set_current_chat(current_chat_id)

# Get current chat
chat = DatabaseManager.get_chat(current_chat_id)
if chat:
    # Get chat messages
    messages = DatabaseManager.get_messages(current_chat_id)
    
    # Display messages
    for message in messages:
        with st.chat_message(message.role):
            st.markdown(message.content)
            if message.role != 'assistant':
                st.caption(f"{message.created_at.strftime('%I:%M %p')}")
            else:
                # Add timestamp and action buttons
                cols = st.columns([0.7, 0.045, 0.045, 0.045, 0.045])
                cols[0].caption(f"{message.created_at.strftime('%I:%M %p')}")
                cols[1].button("👍", key=f"like_{message.id}")
                cols[2].button("👎", key=f"dislike_{message.id}")
                cols[3].button("📋", key=f"copy_{message.id}")
                cols[4].button("🔄", key=f"regen_{message.id}")
    
    # Chat input
    if prompt := st.chat_input("What's on your mind?"):
        # Add user message
        turn_number = max([m.turn_number for m in messages]) + 1 if messages else 0
        user_message = DatabaseManager.add_message(
            current_chat_id,
            "user",
            prompt,
            turn_number
        )
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
            st.caption(f"{user_message.created_at.strftime('%I:%M %p')}")
        
        # Get and display assistant response
        with st.chat_message("assistant"):
            # Create placeholders for message and stop button
            stop_button_placeholder = st.empty()
            message_placeholder = st.empty()
            
            # Initialize response accumulator
            full_response = []
            
            # Initialize stop generation state
            if "stop_generation" not in st.session_state:
                st.session_state.stop_generation = False
            
            # Create stop button
            if stop_button_placeholder.button("Stop Generating", key="stop_button"):
                st.session_state.stop_generation = True
            
            def update_message(chunk: str):
                if not st.session_state.stop_generation:
                    full_response.append(chunk)
                    message_placeholder.markdown("".join(full_response))
            
            # Get streaming response from LLM
            llm.get_streaming_response(
                prompt,
                context=[{
                    "role": m.role,
                    "content": m.content
                } for m in messages],
                callback=update_message
            )
            
            # Remove stop button after generation
            stop_button_placeholder.empty()
            
            # Add assistant message to database
            response_text = "".join(full_response)
            if st.session_state.stop_generation:
                response_text += "\n\n*Generation stopped by user*"
                
            assistant_message = DatabaseManager.add_message(
                current_chat_id,
                "assistant",
                response_text,
                turn_number
            )
            
            # Update counters
            SessionState.increment_counters("assistant")
            
            # Check if chat should be named or renamed
            updated_chat = DatabaseManager.get_chat(current_chat_id)
            if should_name_chat(messages, updated_chat):
                # Get chat name from LLM
                chat_context = "\n".join([
                    f"{m.role}: {m.content}" for m in 
                    DatabaseManager.get_messages(current_chat_id)
                ])
                name_prompt = f"""Based on this conversation, suggest a short (2-5 words) name for the chat that captures its main topic or purpose. Only respond with the name, nothing else:

{chat_context}"""
                chat_name = llm.get_response(name_prompt, []).strip()
                
                # Update chat name
                DatabaseManager.update_chat(
                    current_chat_id,
                    name=chat_name,
                    is_named_by_llm=True
                )
            
            st.rerun()
else:
    st.info("Select a chat from the sidebar or create a new one to get started.")

# Render sidebar with chat list and profile
render_sidebar()
