from database import DatabaseManager, init_db, get_db
from sqlalchemy import text

def test_db_connection():
    """Test database connection"""
    try:
        init_db()
        with get_db() as db:
            db.execute(text("SELECT 1"))
        print("✅ Database connection successful")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")

def test_models():
    """Test database models and table creation"""
    try:
        init_db()
        with get_db() as db:
            tables = db.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema='public'
            """)).scalars().all()
            expected = {'users', 'chats', 'messages'}
            actual = set(tables)
            assert expected.issubset(actual), f"Missing tables. Expected {expected}, got {actual}"
        print("✅ Database tables created successfully")
    except Exception as e:
        print(f"❌ Database tables creation failed: {e}")

def clean_database():
    """Clean up the database before testing"""
    try:
        with get_db() as db:
            db.execute(text("TRUNCATE users, chats, messages CASCADE"))
            db.commit()
        print("✅ Database cleaned")
    except Exception as e:
        print(f"❌ Database cleanup failed: {e}")

def test_user_operations():
    """Test user creation, retrieval, and update"""
    try:
        # Clean up first
        clean_database()
        
        # Test user creation
        user = DatabaseManager.get_or_create_user("Test User")
        assert user.name == "Test User", f"User name mismatch. Expected 'Test User', got '{user.name}'"
        
        # Test user retrieval
        same_user = DatabaseManager.get_or_create_user("Test User")
        assert same_user.id == user.id, "User retrieval failed - different user returned"
        
        # Test user update
        updated = DatabaseManager.update_user(
            str(user.id),
            name="Updated Name"
        )
        assert updated.name == "Updated Name", f"User update failed. Expected 'Updated Name', got '{updated.name}'"
        print("✅ User operations successful")
    except Exception as e:
        print(f"❌ User operations failed: {e}")

def test_chat_operations():
    """Test chat creation, retrieval, and update"""
    try:
        # Clean up first
        clean_database()
        
        # Create a user first
        user = DatabaseManager.get_or_create_user("Test User")
        
        # Test chat creation
        chat = DatabaseManager.create_chat(str(user.id), "Test Chat")
        assert chat.name == "Test Chat", f"Chat name mismatch. Expected 'Test Chat', got '{chat.name}'"
        
        # Test chat retrieval
        chats = DatabaseManager.get_chats(str(user.id))
        assert len(chats) == 1, f"Expected 1 chat, got {len(chats)}"
        assert chats[0].id == chat.id, "Chat retrieval failed - different chat returned"
        
        # Test chat update
        updated = DatabaseManager.update_chat(
            str(chat.id),
            name="Updated Chat",
            is_named_by_llm=True
        )
        assert updated.name == "Updated Chat", f"Chat update failed. Expected 'Updated Chat', got '{updated.name}'"
        assert updated.is_named_by_llm is True, "Chat LLM naming flag not updated"
        print("✅ Chat operations successful")
    except Exception as e:
        print(f"❌ Chat operations failed: {e}")

def test_message_operations():
    """Test message creation and retrieval"""
    try:
        # Clean up first
        clean_database()
        
        # Create user and chat first
        user = DatabaseManager.get_or_create_user("Test User")
        chat = DatabaseManager.create_chat(str(user.id), "Test Chat")
        
        # Test message creation
        message = DatabaseManager.add_message(
            str(chat.id),
            "user",
            "Hello, world!",
            1
        )
        assert message.content == "Hello, world!", f"Message content mismatch. Expected 'Hello, world!', got '{message.content}'"
        assert message.role == "user", f"Message role mismatch. Expected 'user', got '{message.role}'"
        assert message.turn_number == 1, f"Message turn number mismatch. Expected 1, got {message.turn_number}"
        
        # Test message retrieval
        messages = DatabaseManager.get_messages(str(chat.id))
        assert len(messages) == 1, f"Expected 1 message, got {len(messages)}"
        assert messages[0].id == message.id, "Message retrieval failed - different message returned"
        print("✅ Message operations successful")
    except Exception as e:
        print(f"❌ Message operations failed: {e}")

def test_chat_search():
    """Test chat search functionality"""
    try:
        # Clean up first
        clean_database()
        
        # Create user and multiple chats
        user = DatabaseManager.get_or_create_user("Test User")
        chat1 = DatabaseManager.create_chat(str(user.id), "Python Discussion")
        chat2 = DatabaseManager.create_chat(str(user.id), "JavaScript Help")
        chat3 = DatabaseManager.create_chat(str(user.id), "Python Projects")
        
        # Test exact match
        python_chats = DatabaseManager.get_chats(str(user.id), search="Python")
        assert len(python_chats) == 2, f"Expected 2 Python chats, got {len(python_chats)}"
        
        # Test case insensitive
        js_chats = DatabaseManager.get_chats(str(user.id), search="javascript")
        assert len(js_chats) == 1, f"Expected 1 JavaScript chat, got {len(js_chats)}"
        
        # Test partial match
        script_chats = DatabaseManager.get_chats(str(user.id), search="script")
        assert len(script_chats) == 1, f"Expected 1 chat with 'script', got {len(script_chats)}"
        
        # Test no match
        no_chats = DatabaseManager.get_chats(str(user.id), search="Ruby")
        assert len(no_chats) == 0, f"Expected 0 Ruby chats, got {len(no_chats)}"
        
        print("✅ Chat search successful")
    except Exception as e:
        print(f"❌ Chat search failed: {e}")

if __name__ == "__main__":
    print("\nRunning database tests...\n")
    test_db_connection()
    test_models()
    test_user_operations()
    test_chat_operations()
    test_message_operations()
    test_chat_search()
    print("\nTests completed.\n")
