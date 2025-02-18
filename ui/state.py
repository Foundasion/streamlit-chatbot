"""State management for the Streamlit chatbot application."""

from typing import Optional, Dict, Any
import streamlit as st
from database.database import DatabaseManager

class SessionState:
    """Manages application state across Streamlit reruns."""
    
    @staticmethod
    def init_state():
        """Initialize session state variables if they don't exist."""
        if "user_id" not in st.session_state:
            # Get or create default user
            user = DatabaseManager.get_or_create_user("User")
            st.session_state.user_id = str(user.id)
            st.session_state.user_name = user.name
            st.session_state.avatar_url = user.avatar_url

        if "current_chat_id" not in st.session_state:
            st.session_state.current_chat_id = None
            
        if "search_query" not in st.session_state:
            st.session_state.search_query = ""
            
        if "turn_counter" not in st.session_state:
            st.session_state.turn_counter = 0
            
        if "message_counter" not in st.session_state:
            st.session_state.message_counter = 0

    @staticmethod
    def get_current_chat() -> Optional[str]:
        """Get the current chat ID."""
        return st.session_state.current_chat_id

    @staticmethod
    def set_current_chat(chat_id: Optional[str]):
        """Set the current chat ID."""
        st.session_state.current_chat_id = chat_id
        # Reset counters when switching chats
        st.session_state.turn_counter = 0
        st.session_state.message_counter = 0

    @staticmethod
    def increment_counters(role: str):
        """Increment message and turn counters."""
        st.session_state.message_counter += 1
        if role == "assistant":
            st.session_state.turn_counter += 1

    @staticmethod
    def should_name_chat() -> bool:
        """Check if the chat should be named by LLM."""
        return (
            st.session_state.turn_counter >= 4 or 
            st.session_state.message_counter >= 8
        )

    @staticmethod
    def get_user_info() -> Dict[str, Any]:
        """Get current user information."""
        return {
            "id": st.session_state.user_id,
            "name": st.session_state.user_name,
            "avatar_url": st.session_state.avatar_url
        }

    @staticmethod
    def update_user_info(name: Optional[str] = None, avatar_url: Optional[str] = None):
        """Update user information."""
        if name or avatar_url:
            user = DatabaseManager.update_user(
                st.session_state.user_id,
                name=name,
                avatar_url=avatar_url
            )
            if user:
                if name:
                    st.session_state.user_name = name
                if avatar_url:
                    st.session_state.avatar_url = avatar_url

    @staticmethod
    def get_search_query() -> str:
        """Get current search query."""
        return st.session_state.search_query

    @staticmethod
    def set_search_query(query: str):
        """Set search query."""
        st.session_state.search_query = query
