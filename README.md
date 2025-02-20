# Streamlit Chatbot

A lightweight, modular chatbot interface built with Streamlit that connects to Claude for natural language interactions, featuring persistent storage and basic search capabilities.

## Features & Architecture

1. **Frontend**: 
   - Clean, intuitive chat interface with native Streamlit components ✓
   - Message streaming with real-time responses ✓
   - Message action buttons UI implementation ✓
   - Responsive sidebar for chat management ✓
   - Dialog-based operations (edit/delete/export) ✓
   - User profile management with avatars ✓
   - Markdown message formatting ✓
   - Long message handling ✓

2. **Database**: 
   - PostgreSQL for persistent chat history ✓
   - SQLAlchemy ORM for efficient operations ✓
   - Case-insensitive chat search ✓
   - User profile management [Needs Testing]
   - Automatic chat naming [Needs Testing]
   - Message turn tracking [Needs Testing]

3. **LLM Integration**: 
   - Claude integration with abstraction layer ✓
   - Context-aware responses ✓
   - Automatic chat naming after 2 messages [Needs Testing]
   - Chat name reassessment at 6 messages [Needs Testing]

## Testing Status

### Validated Features ✓
1. Dialog Interactions
   - Edit chat functionality
   - Delete chat confirmation
   - Profile editing dialog
   - Export chat dialog
   - Dialog transitions and styling

2. Chat Management
   - Automatic chat naming triggers
   - Chat name reassessment
   - Empty chat handling
   - Basic search functionality

3. UI Components
   - Sidebar scrolling behavior
   - Button interactions
   - Dialog layouts
   - Mobile responsiveness
   - Message formatting and display

4. State Management
   - Session persistence
   - Chat switching
   - Profile updates
   - User settings maintenance

### Validated Features ✓
1. UI Navigation
   - Chat selection highlighting with visual feedback
   - Smart New Chat management
     * Header placement for better accessibility
     * Empty chat validation
     * Helpful tooltips
   - Enhanced sidebar styling
     * Rainbow divider for visual hierarchy
     * Improved search bar appearance
     * Cleaner chat list presentation

### Completed Features ✓
1. Message Actions
   - Like/dislike system with state management
   - Message regeneration with version tracking
   - Copy functionality (in progress)
   - Visual feedback and indicators

### Needs Implementation
1. UI Enhancements
   - Frontend Styling
     * Improve overall appearance
     * Enhance visual hierarchy
     * Refine component layouts
   - Copy Feature
     * Fix clipboard integration
     * Add success indicators
     * Handle code blocks properly

2. Search Enhancements
   - Real-time filtering
   - Search term persistence
   - Inexact matching
   - Results feedback

## Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL 14
- Anthropic API key

### Setup

1. Create environment & install PostgreSQL:
```bash
# Create conda environment
conda create -n streamlit-chatbot python=3.11 -y
conda activate streamlit-chatbot

# Install and start PostgreSQL (macOS)
brew install postgresql@14
brew services start postgresql@14
createdb streamlit_chatbot
```

2. Install & configure:
```bash
# Clone and install
git clone <repository-url>
cd streamlit_chatbot
pip install -r requirements.txt

# Configure environment (.env file)
ANTHROPIC_API_KEY=your-api-key-here
DATABASE_URL=postgresql://localhost/streamlit_chatbot
PYTHONPATH=${PWD}
```

3. Run:
```bash
streamlit run app.py
```

Visit `http://localhost:8501` to use the app.

## Project Structure

```
streamlit_chatbot/
├── app.py                      # Main Streamlit application
├── llm.py                     # LLM provider abstraction
├── requirements.txt           # Project dependencies
├── database/                 # Database module
│   ├── __init__.py
│   ├── models.py             # SQLAlchemy models
│   └── database.py           # Database operations
├── ui/                      # UI components
│   ├── __init__.py
│   ├── components.py        # Reusable UI components
│   ├── state.py            # Session state management
│   └── styles.py           # Additional styling
├── static/                   # Static assets
│   └── styles.css            # Custom CSS
├── tests/                    # Test suite
│   └── test_database.py      # Database tests
└── docs/                    # Documentation
    ├── database.md          # Database implementation guide
    ├── implementation_plan.md # Detailed project roadmap (for POC)
    ├── strategic_vision.md   # Project vision and goals (long-term MVP and beyond)
    └── autodoc_tool.md      # Documentation tooling 
```

## Testing & Documentation

### Running Tests
```bash
# Set PYTHONPATH
export PYTHONPATH=${PWD}

# Run tests
python tests/test_database.py
```

### Documentation
- [Database Guide](docs/database.md): Detailed guide on database implementation, setup, and best practices

### Extending
To add support for a different LLM provider:
1. Create a new class that inherits from `LLMProvider` in `llm.py`
2. Implement the required methods: `_initialize_model()` and `get_response()`
3. Update the `get_llm_provider()` factory function

## Development Roadmap

### Phase 1 (Current): Basic Chatbot ✓
- Streamlit interface with chat components
- Claude integration with abstraction layer
- PostgreSQL database integration
- Basic chat search and user profiles

### Phase 2: Enhanced Search & Context
- Vector database integration (Pinecone)
  - Semantic search capabilities
  - Contextual conversation retrieval
  - Pattern recognition and analysis
- Advanced chat management
  - User authentication
  - Export/import functionality
  - Enhanced error handling

### Phase 3: Tool Integration
- External service connections
  - Slack for team collaboration
  - Email for notifications
  - Google Docs for content
- MCP server framework
  - Modular architecture
  - Secure credential handling
  - Advanced error recovery

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT
