# Streamlit Chatbot

A lightweight, modular chatbot interface built with Streamlit that connects to Claude for natural language interactions, featuring persistent storage and basic search capabilities.

## Features & Architecture

1. **Frontend**: 
   - Clean, intuitive chat interface with Streamlit components
   - Real-time message streaming
   - Responsive sidebar for chat management
   - Custom CSS for enhanced styling

2. **Database**: 
   - PostgreSQL for persistent chat history
   - SQLAlchemy ORM for efficient operations
   - Case-insensitive chat search
   - User profile management

3. **LLM Integration**: 
   - Claude integration with abstraction layer
   - Easy to extend with different providers
   - Context-aware responses

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
