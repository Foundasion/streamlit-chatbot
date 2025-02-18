"""UI components for the Streamlit chatbot application."""

from datetime import datetime
from typing import Optional
import json
import streamlit as st
from database.database import DatabaseManager
from .state import SessionState

def render_sidebar():
    """Render the main sidebar container."""
    with st.sidebar:
        # Header with New Chat button
        col1, col2 = st.columns([3, 2])
        with col1:
            st.header("Chats")
        with col2:
            st.write("")  # Add spacing to align with header
            if st.button("✏️ New", key="new_chat", use_container_width=True):
                user_info = SessionState.get_user_info()
                empty_chat_id = has_empty_chat(user_info["id"])
                if empty_chat_id:
                    # Use existing empty chat
                    SessionState.set_current_chat(empty_chat_id)
                else:
                    # Create new chat only if no empty chats exist
                    chat = DatabaseManager.create_chat(user_info["id"], "New Chat")
                    SessionState.set_current_chat(str(chat.id))
                st.rerun()
        
        # Fixed search bar at top
        render_search_bar()
        
        # Scrollable chat list
        render_chat_list()
        
        # Fixed profile bar at bottom
        render_profile_bar()

def render_search_bar():
    """Render the chat search functionality."""
    search_query = st.text_input(
        "Search chats",
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

def render_chat_list():
    """Render the list of chat sessions."""
    # Get user's chats
    user_info = SessionState.get_user_info()
    chats = DatabaseManager.get_chats(
        user_info["id"],
        search=SessionState.get_search_query()
    )
    
    # Create scrollable container for chat list
    with st.container():
        st.markdown('<div class="chat-list-container">', unsafe_allow_html=True)
        for chat in chats:
            st.markdown('<div class="chat-list-item">', unsafe_allow_html=True)
            col1, col2, col3, col4 = st.columns([5, 1, 1, 1], gap='small')
            chat_id = str(chat.id)
            
            # Chat name and timestamp
            with col1:
                # Format timestamp
                timestamp = chat.updated_at.strftime("%I:%M %p")
                if chat.updated_at.date() != datetime.now().date():
                    timestamp = chat.updated_at.strftime("%b %d, %I:%M %p")
                
                # Display chat name with timestamp
                if st.button(
                    f"{chat.name}",
                    key=f"chat_{chat_id}",
                    use_container_width=True, help=f'{timestamp}',
                ):
                    SessionState.set_current_chat(chat_id)
                    st.rerun()
            
            # Edit button
            with col2:
                if st.button("✏️", key=f"edit_{chat_id}"):
                    with st.dialog(f"Edit Chat - {chat.name}", key=f"edit_dialog_{chat_id}"):
                        with st.form(key=f"edit_form_{chat_id}"):
                            new_name = st.text_input(
                                "Chat Name",
                                value=chat.name,
                                key=f"rename_{chat_id}"
                            )
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.form_submit_button("Save"):
                                    DatabaseManager.update_chat(chat_id, name=new_name)
                                    st.rerun()
                            with col2:
                                if st.form_submit_button("Cancel"):
                                    st.rerun()
            
            # Export button
            with col3:
                if st.button("📥", key=f"export_{chat_id}", help="Export chat"):
                    chat_data = export_chat(chat_id)
                    with st.dialog("Export Chat", key=f"export_dialog_{chat_id}"):
                        st.json(chat_data)
                        st.download_button(
                            "Download JSON",
                            data=json.dumps(chat_data, indent=2),
                            file_name=f"chat_{chat.name}_{chat.updated_at.strftime('%Y%m%d')}.json",
                            mime="application/json",
                            key=f"download_{chat_id}"
                        )
            
            # Delete button
            with col4:
                if st.button("🗑️", key=f"delete_{chat_id}"):
                    with st.dialog("Delete Chat", key=f"delete_dialog_{chat_id}"):
                        st.warning(f"Are you sure you want to delete '{chat.name}'?")
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("Yes", key=f"confirm_delete_{chat_id}"):
                                DatabaseManager.delete_chat(chat_id)
                                if SessionState.get_current_chat() == chat_id:
                                    SessionState.set_current_chat(None)
                                st.rerun()
                        with col2:
                            if st.button("No", key=f"cancel_delete_{chat_id}"):
                                st.rerun()
            
            # Close chat-list-item div
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Close chat-list-container div
        st.markdown('</div>', unsafe_allow_html=True)

def render_profile_bar():
    """Render the user profile section."""
    user_info = SessionState.get_user_info()
    
    # Create container with profile-section class
    with st.container():
        st.markdown('<div class="profile-section">', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 4])
        
        # Avatar
        with col1:
            if user_info["avatar_url"]:
                st.image(user_info["avatar_url"], width=40)
            else:
                st.markdown("👤")
        
        # User name as clickable button
        with col2:
            if st.button(f"{user_info['name']}", key="profile_button"):
                with st.dialog("Edit Profile", key="profile_dialog"):
                    with st.form("edit_profile"):
                        new_name = st.text_input(
                            "Name",
                            value=user_info["name"]
                        )
                        new_avatar = st.text_input(
                            "Avatar URL",
                            value=user_info["avatar_url"] or ""
                        )
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.form_submit_button("Save"):
                                SessionState.update_user_info(
                                    name=new_name,
                                    avatar_url=new_avatar if new_avatar else None
                                )
                                st.rerun()
                        with col2:
                            if st.form_submit_button("Cancel"):
                                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

def format_message(role: str, content: str) -> str:
    """Format a message for display."""
    if role == "user":
        return f"You: {content}"
    return f"Assistant: {content}"

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
