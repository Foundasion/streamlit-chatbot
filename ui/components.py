"""UI components for the Streamlit chatbot application."""

from datetime import datetime
from typing import Optional
import json
import streamlit as st
from database.database import DatabaseManager
from database.models import Message
from .state import SessionState

def render_sidebar():
    """Render the main sidebar container."""
    with st.sidebar:
        st.header("Chats", divider='rainbow')
        
        # Search bar
        render_search_bar()
        
        # Chat list
        render_chat_list()
        
        # Profile section
        render_profile_bar()

def render_search_bar():
    """Render the chat search functionality."""
    search_query = st.text_input(
        "", label_visibility="collapsed",
        value=SessionState.get_search_query(),
        placeholder="Search by chat name...",
        key="chat_search"
    )
    if search_query != SessionState.get_search_query():
        SessionState.set_search_query(search_query)

def has_empty_chat(user_id: str) -> Optional[str]:
    """Check for empty chats and return the first empty chat ID if found."""
    chats = DatabaseManager.get_chats(user_id)
    for chat in chats:
        if len(DatabaseManager.get_messages(str(chat.id))) == 0:
            return str(chat.id)
    return None

def export_chat(chat_id: str) -> dict:
    """Export chat data as JSON."""
    chat = DatabaseManager.get_chat(chat_id)
    messages = DatabaseManager.get_messages(chat_id)
    return {
        "chat": {
            "id": str(chat.id),
            "name": chat.name,
            "created_at": chat.created_at.isoformat(),
            "updated_at": chat.updated_at.isoformat(),
            "is_named_by_llm": chat.is_named_by_llm
        },
        "messages": [{
            "role": m.role,
            "content": m.content,
            "turn_number": m.turn_number,
            "created_at": m.created_at.isoformat()
        } for m in messages]
    }

@st.dialog("Edit Chat")
def edit_chat_dialog(chat_id: str, chat_name: str):
    """Dialog for editing chat name."""
    with st.form("edit_form"):
        new_name = st.text_input("Chat Name", value=chat_name)
        if st.form_submit_button("Save"):
            DatabaseManager.update_chat(chat_id, name=new_name)
            st.rerun()

@st.dialog("Export Chat")
def export_chat_dialog(chat_id: str, chat_name: str):
    """Dialog for exporting chat data."""
    chat_data = export_chat(chat_id)
    st.json(chat_data)
    st.download_button(
        "Download JSON",
        data=json.dumps(chat_data, indent=2),
        file_name=f"chat_{chat_name}_{datetime.now().strftime('%Y%m%d')}.json",
        mime="application/json"
    )

@st.dialog("Delete Chat")
def delete_chat_dialog(chat_id: str, chat_name: str):
    """Dialog for confirming chat deletion."""
    st.warning(f"Are you sure you want to delete '{chat_name}'?")
    cols = st.columns(2, gap='medium', vertical_alignment='center')
    with cols[0]:
        if st.button("Yes", use_container_width=True):
            DatabaseManager.delete_chat(chat_id)
            if SessionState.get_current_chat() == chat_id:
                SessionState.set_current_chat(None)
            st.rerun()
    with cols[1]:
        if st.button("No", use_container_width=True):
            st.rerun()

def render_chat_list():
    """Render the list of chat sessions."""
    user_info = SessionState.get_user_info()
    chats = DatabaseManager.get_chats(
        user_info["id"],
        search=SessionState.get_search_query()
    )
    
    for chat in chats:
        chat_id = str(chat.id)
        
        # Format timestamp
        timestamp = chat.updated_at.strftime("%I:%M %p")
        if chat.updated_at.date() != datetime.now().date():
            timestamp = chat.updated_at.strftime("%b %d, %I:%M %p")
        
        # Check if this is the current chat
        is_current_chat = chat_id == SessionState.get_current_chat()
        
        with st.container():
            cols = st.columns([4, 1, 1, 1])
            
            # Chat name and select button
            with cols[0]:
                button_style = "primary" if is_current_chat else "secondary"
                if st.button(f"{chat.name}", key=f"chat_{chat_id}", help=timestamp, use_container_width=True, type=button_style):
                    SessionState.set_current_chat(chat_id)
                    st.rerun()
            
            # Edit button
            with cols[1]:
                if st.button(":pencil2:", key=f"edit_{chat_id}", use_container_width=True):
                    edit_chat_dialog(chat_id, chat.name)
            
            # Export button
            with cols[2]:
                if st.button(":floppy_disk:", key=f"export_{chat_id}", use_container_width=True):
                    export_chat_dialog(chat_id, chat.name)
            
            # Delete button
            with cols[3]:
                if st.button(":wastebasket:", key=f"delete_{chat_id}", use_container_width=True):
                    delete_chat_dialog(chat_id, chat.name)

@st.dialog("Edit Profile")
def edit_profile_dialog(user_info: dict):
    """Dialog for editing user profile."""
    with st.form("edit_profile"):
        new_name = st.text_input("Name", value=user_info["name"])
        new_avatar = st.text_input("Avatar URL", value=user_info["avatar_url"] or "")
        if st.form_submit_button("Save"):
            SessionState.update_user_info(
                name=new_name,
                avatar_url=new_avatar if new_avatar else None
            )
            st.rerun()

def render_profile_bar():
    """Render the user profile section."""
    user_info = SessionState.get_user_info()
    
    st.divider()
    
    cols = st.columns([1, 4], vertical_alignment='center')
    
    # Avatar
    with cols[0]:
        if user_info["avatar_url"]:
            st.image(user_info["avatar_url"], width=100)
        else:
            st.markdown("👤")
    
    # User name and edit button
    with cols[1]:
        if st.button(f"{user_info['name']}", key="profile_button", use_container_width=True):
            edit_profile_dialog(user_info)

def handle_reaction(message_id: str, reaction_type: str):
    """Handle like/dislike reactions"""
    user_id = SessionState.get_user_info()["id"]
    
    # Get current reaction
    current_reaction = DatabaseManager.get_reaction(message_id, user_id)
    
    if current_reaction and current_reaction.reaction_type == reaction_type:
        # Remove reaction if clicking the same button again
        DatabaseManager.remove_reaction(message_id, user_id)
    else:
        # Add or update reaction
        DatabaseManager.add_or_update_reaction(message_id, user_id, reaction_type)
    
    st.rerun()

def handle_regeneration(message_id: str):
    """Handle message regeneration"""
    from llm import get_llm_provider
    
    message = DatabaseManager.get_message(message_id)
    if message and message.role == "assistant":
        # Mark current message as regenerated
        DatabaseManager.mark_message_regenerated(message_id)
        
        # Get the user's message that prompted this response
        messages = DatabaseManager.get_messages(message.chat_id)
        user_message = None
        context_messages = []
        
        # Build context from messages up to the user's message
        for msg in messages:
            if msg.id == message_id:
                break
            context_messages.append({
                "role": msg.role,
                "content": msg.content
            })
            if msg.role == "user":
                user_message = msg
        
        if user_message:
            # Create a placeholder for the new response
            placeholder = st.empty()
            response_text = []
            
            def update_response(chunk: str):
                response_text.append(chunk)
                placeholder.markdown("".join(response_text))
            
            # Get new response from LLM
            llm = get_llm_provider()
            llm.get_streaming_response(
                user_message.content,
                context=context_messages,
                callback=update_response
            )
            
            # Save new message
            DatabaseManager.add_message(
                chat_id=message.chat_id,
                role="assistant",
                content="".join(response_text),
                turn_number=message.turn_number,
                original_message_id=message_id
            )
            st.rerun()

def format_message(role: str, content: str) -> str:
    """Format a message for display."""
    if role == "user":
        return f"You: {content}"
    return f"Assistant: {content}"

def render_chat_messages(chat_id: str):
    """Render all messages in a chat with action buttons."""
    # Get only the latest version of each message
    messages = DatabaseManager.get_messages(chat_id, include_regenerated=False)
    
    # Find last assistant message
    last_assistant_message = DatabaseManager.get_last_assistant_message(chat_id)
    
    for message in messages:
        with st.chat_message(message.role):
            # Render message content
            st.markdown(message.content)
            
            # Add timestamp and actions in a row
            cols = st.columns([10, 1, 1, 1], vertical_alignment='center')
            
            # Timestamp with regeneration indicator
            timestamp = message.created_at.strftime("%I:%M %p")
            if message.created_at.date() != datetime.now().date():
                timestamp = message.created_at.strftime("%b %d, %I:%M %p")
            if message.original_message_id:
                timestamp += " (Regenerated :arrows_counterclockwise:)"
            cols[0].caption(timestamp)
            
            # Add action buttons for assistant messages
            if message.role == "assistant":
                is_last_assistant = last_assistant_message and message.id == last_assistant_message.id
                
                # Get current reaction
                reaction = DatabaseManager.get_reaction(message.id, SessionState.get_user_info()["id"])
                
                # Like button
                button_style = "primary" if reaction and reaction.reaction_type == "like" else "secondary"
                if cols[1].button("👍", key=f"like_{message.id}", type=button_style):
                    handle_reaction(message.id, "like")
                
                # Dislike button
                button_style = "primary" if reaction and reaction.reaction_type == "dislike" else "secondary"
                if cols[2].button("👎", key=f"dislike_{message.id}", type=button_style):
                    handle_reaction(message.id, "dislike")
                
                # Regenerate button
                if is_last_assistant:
                    if cols[3].button("🔄", key=f"regen_{message.id}"):
                        handle_regeneration(message.id)
                else:
                    cols[3].button("🔄", key=f"regen_{message.id}", disabled=True, 
                                help="Regeneration only available for the last assistant message")

def should_name_chat(messages, chat) -> bool:
    """Check if a chat should be named based on message count."""
    if not messages:
        return False
    
    message_count = len(messages)
    
    # Initial naming after 2 messages
    if not chat.is_named_by_llm and message_count >= 2:
        return True
    
    # Re-assess name after 6 messages
    if chat.is_named_by_llm and message_count >= 6:
        return True
    
    return False
