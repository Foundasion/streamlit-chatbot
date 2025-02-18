# Database Implementation

## Overview
The database layer implements a PostgreSQL-based persistence system with SQLAlchemy ORM. This provides a robust, scalable foundation for storing chat history, user data, and message content.

## Models

### User
```python
class User:
    id: UUID            # Unique identifier
    name: String        # User's display name
    avatar_url: String  # URL to user's avatar image
    created_at: DateTime
    updated_at: DateTime
```

### Chat
```python
class Chat:
    id: UUID            # Unique identifier
    user_id: UUID       # Reference to User
    name: String        # Chat name/title
    is_named_by_llm: Boolean  # Whether name was auto-generated
    created_at: DateTime
    updated_at: DateTime
```

### Message
```python
class Message:
    id: UUID            # Unique identifier
    chat_id: UUID       # Reference to Chat
    role: String        # 'user' or 'assistant'
    content: Text       # Message content
    turn_number: Integer # Message position in conversation
    created_at: DateTime
```

## Key Features

### UUID-based Identifiers
- All models use UUID primary keys
- Ensures uniqueness across distributed systems
- Prevents sequential ID enumeration

### Timestamp Management
- Automatic created_at tracking
- Updated_at timestamps for change tracking
- UTC timestamps for consistency

### Search Functionality
- Case-insensitive chat name search
- Partial matching support
- Ordered by most recently updated

### Data Integrity
- Foreign key constraints
- Cascading deletions
- Not-null constraints where appropriate

## Usage Examples

### User Management
```python
# Create/get user
user = DatabaseManager.get_or_create_user("John Doe")

# Update user
updated_user = DatabaseManager.update_user(
    user.id,
    name="John Smith",
    avatar_url="https://example.com/avatar.png"
)
```

### Chat Operations
```python
# Create chat
chat = DatabaseManager.create_chat(user.id, "Python Discussion")

# Search chats
python_chats = DatabaseManager.get_chats(user.id, search="python")

# Update chat
DatabaseManager.update_chat(
    chat.id,
    name="Advanced Python",
    is_named_by_llm=True
)
```

### Message Management
```python
# Add message
message = DatabaseManager.add_message(
    chat.id,
    "user",
    "Hello, world!",
    1
)

# Get chat history
messages = DatabaseManager.get_messages(chat.id)
```

## Data Storage & Access

### Physical Storage
PostgreSQL stores its data in the following location:
- macOS: `/opt/homebrew/var/postgresql@14`
- The database name is `streamlit_chatbot`

### Accessing Data

1. Command Line Interface:
```bash
# Connect to database
psql streamlit_chatbot

# Common commands:
\dt                     # List all tables
\d users               # Describe users table
\d chats               # Describe chats table
\d messages            # Describe messages table

# Example queries:
SELECT * FROM users;
SELECT * FROM chats ORDER BY updated_at DESC;
SELECT * FROM messages WHERE chat_id = '<chat-id>';
```

2. GUI Tools:
- pgAdmin 4: Official PostgreSQL GUI
- Postico (macOS): User-friendly PostgreSQL client
- DBeaver: Cross-platform database tool

3. Data Backup:
```bash
# Backup database
pg_dump streamlit_chatbot > backup.sql

# Restore database
psql streamlit_chatbot < backup.sql
```

4. Monitoring:
```sql
-- Active connections
SELECT * FROM pg_stat_activity;

-- Table sizes
SELECT pg_size_pretty(pg_total_relation_size('users'));
SELECT pg_size_pretty(pg_total_relation_size('chats'));
SELECT pg_size_pretty(pg_total_relation_size('messages'));

-- Database size
SELECT pg_size_pretty(pg_database_size('streamlit_chatbot'));
```

## Testing

The database implementation includes a comprehensive test suite in `tests/test_database.py`. The tests cover:

1. Database Connection
- Verifies database connectivity
- Checks table creation

2. Model Operations
- User CRUD operations
- Chat management
- Message handling
- Search functionality

3. Data Integrity
- Foreign key constraints
- Cascading deletions
- Timestamp management

To run the tests:
```bash
# Set PYTHONPATH
export PYTHONPATH=${PWD}

# Run tests
python tests/test_database.py
```

## Environment Setup

1. Install PostgreSQL 14:
```bash
brew install postgresql@14
brew services start postgresql@14
```

2. Create Database:
```bash
createdb streamlit_chatbot
```

3. Configure Environment:
Create a `.env` file with:
```
DATABASE_URL=postgresql://localhost/streamlit_chatbot
PYTHONPATH=${PWD}
```

4. Install Python Dependencies:
```bash
pip install -r requirements.txt
```

## Best Practices

1. Always use the DatabaseManager class for database operations
2. Ensure proper error handling for database operations
3. Use context managers for database sessions
4. Keep foreign key relationships consistent
5. Regularly backup important data
6. Monitor database size and performance
7. Use search functionality for efficient chat retrieval
8. Maintain UTC timestamps for consistency
