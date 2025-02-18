"""Additional styling for the Streamlit chatbot application."""

def inject_custom_css():
    """Inject custom CSS into the Streamlit app."""
    return """
        <style>
        /* Layout adjustments */
        .block-container {
            padding-top: 1rem;
            padding-bottom: 0rem;
        }
        header {
            height: 0;
            visibility: hidden;
        }
        [data-testid="stSidebar"] [data-testid="stSidebarNav"] {
            display: none;
        }
        
        /* Sidebar styling */
        section[data-testid="stSidebar"] > div {
            height: 100vh;
            display: flex;
            flex-direction: column;
        }
        
        section[data-testid="stSidebar"] .chat-list {
            flex: 1;
            overflow-y: auto;
            min-height: 0;
        }
        
        /* Message input styling */
        .stTextInput > div > div > input {
            caret-color: rgb(49, 51, 63);
        }

        /* Button hover effects */
        .stButton button:hover {
            border-color: rgb(49, 51, 63);
        }

        /* Chat message container */
        .chat-message-container {
            display: flex;
            margin: 1rem auto;
            padding: 0 1rem;
            max-width: 800px;
        }

        /* Timestamp styling */
        .message-timestamp {
            font-size: 0.8em;
            color: rgba(49, 51, 63, 0.6);
            margin-top: 0.2rem;
        }

        /* Loading animation */
        @keyframes pulse {
            0% { opacity: 0.4; }
            50% { opacity: 0.8; }
            100% { opacity: 0.4; }
        }

        .loading {
            animation: pulse 1.5s ease-in-out infinite;
        }
        
        /* Chat list container */
        .chat-list-container {
            padding: 0.5rem;
        }
        
        /* Chat list item */
        .chat-list-item {
            margin: 0.25rem 0;
            border-radius: 0.5rem;
            transition: all 0.2s;
            padding: 0.25rem;
        }
        
        .chat-list-item:hover {
            background-color: rgba(49, 51, 63, 0.05);
        }
        
        /* Selected chat */
        .chat-list-item.selected {
            background-color: rgba(49, 51, 63, 0.1);
        }
        
        /* Action buttons container */
        .chat-list-item .stHorizontalBlock {
            gap: 0.25rem !important;
        }
        
        /* Chat name and timestamp */
        .stButton [data-testid="stMarkdownContainer"] p {
            font-size: 0.9em;
            margin: 0;
            white-space: pre-line;
            line-height: 1.2;
        }
        
        /* Chat list buttons */
        .stButton button {
            padding: 0.5rem;
            min-height: 0;
            transition: all 0.2s;
        }
        
        /* Action buttons */
        .stButton button[kind="secondary"] {
            padding: 0.25rem;
            height: 2rem;
            min-height: 0;
            width: 2rem;
            border-radius: 0.5rem;
        }
        
        .stButton button[kind="secondary"]:hover {
            background-color: rgba(49, 51, 63, 0.1);
            border-color: transparent;
        }
        
        /* Profile section */
        .profile-section {
            margin-top: auto;
            padding: 1rem;
            border-top: 1px solid rgba(49, 51, 63, 0.2);
        }
        </style>
    """

def get_chat_message_styles():
    """Get styles for chat messages."""
    return {
        "user": {
            "margin": "1rem 0",
            "padding": "1rem",
            "border-radius": "0.5rem",
            "background-color": "#f0f2f6",
            "max-width": "80%",
            "margin-left": "auto",
        },
        "assistant": {
            "margin": "1rem 0",
            "padding": "1rem",
            "border-radius": "0.5rem",
            "background-color": "#e8f0fe",
            "max-width": "80%",
            "margin-right": "auto",
        }
    }
