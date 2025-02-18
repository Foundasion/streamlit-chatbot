# Streamlit Chatbot

A lightweight, modular chatbot interface built with Streamlit that connects to Claude for natural language interactions.

## Features

- Clean, intuitive chat interface
- Real-time message streaming
- Session-based chat history
- Easy to extend with different LLM providers
- Responsive design with sidebar controls

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd streamlit_chatbot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the project root with your API key:
```
ANTHROPIC_API_KEY=your-api-key-here
```

4. Run the application:
```bash
streamlit run app.py
```

The app will be available at `http://localhost:8501`

## Project Structure

- `app.py`: Main Streamlit application with chat interface
- `llm.py`: LLM provider abstraction layer
- `requirements.txt`: Project dependencies

## Architecture

The application uses a modular design with the following components:

1. **Frontend**: Built with Streamlit's native chat components for a responsive and intuitive interface
2. **LLM Integration**: Abstracted through the `LLMProvider` class, making it easy to switch between different LLM providers
3. **Session Management**: Uses Streamlit's session state to maintain chat history during user sessions

## Extending

To add support for a different LLM provider:

1. Create a new class that inherits from `LLMProvider` in `llm.py`
2. Implement the required methods: `_initialize_model()` and `get_response()`
3. Update the `get_llm_provider()` factory function to return your new provider

## Roadmap & Future Improvements

### Persistent Chat History
- PostgreSQL/MongoDB integration for chat storage
- User session management and authentication
- Chat history search and filtering capabilities
- Export/import conversation functionality

### MCP Tool Integration
- Slack integration for team collaboration
  - Send/receive messages
  - Channel monitoring
  - Thread management
- Email integration for notifications
  - Send email summaries
  - Process email inquiries
  - Attachment handling
- Google Docs integration
  - Document processing and analysis
  - Content generation
  - Collaborative editing
- Custom MCP servers for each integration
  - Modular server architecture
  - Secure credential management
  - Rate limiting and error handling

### Vector Database Integration
- Pinecone setup for semantic search
  - Document embedding and retrieval
  - Similar conversation finding
  - Knowledge base integration
- Chat history vectorization
  - Contextual conversation search
  - Pattern recognition
  - User behavior analysis
- Enhanced context management
  - Dynamic context window
  - Relevance scoring
  - Memory optimization

## Development Timeline

### Phase 1 (Current): Basic Chatbot ✓
- Streamlit interface with native chat components
- Claude integration with abstraction layer
- Session-based chat history
- Basic error handling and user feedback

### Phase 2: Persistence & Search
- Database integration for permanent storage
- Vector database setup for semantic search
- Enhanced chat history management
- User authentication system

### Phase 3: MCP Integration
- Tool server implementation
- External service connections
- Enhanced context handling
- Advanced error recovery

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT
