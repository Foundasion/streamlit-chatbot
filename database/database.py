import os
from datetime import datetime
from contextlib import contextmanager
from typing import Generator, Optional, List
from sqlalchemy import create_engine, select, and_
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.sql.expression import desc
from .models import Base, User, Chat, Message, MessageReaction

# Get database URL from environment variable
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://localhost/streamlit_chatbot')

# Create engine
engine = create_engine(DATABASE_URL)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initialize database, creating tables if they don't exist"""
    Base.metadata.create_all(bind=engine)

# Initialize database tables
init_db()

@contextmanager
def get_db() -> Generator[Session, None, None]:
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class DatabaseManager:
    @staticmethod
    def get_or_create_user(name: str, avatar_url: Optional[str] = None) -> User:
        """Get the first user or create one if none exists"""
        with get_db() as db:
            user = db.query(User).first()
            if not user:
                user = User(name=name, avatar_url=avatar_url)
                db.add(user)
                db.commit()
                db.refresh(user)
            return user

    @staticmethod
    def update_user(user_id: str, name: Optional[str] = None, avatar_url: Optional[str] = None) -> User:
        """Update user information"""
        with get_db() as db:
            user = db.query(User).filter(User.id == user_id).first()
            if user:
                if name is not None:
                    user.name = name
                if avatar_url is not None:
                    user.avatar_url = avatar_url
                db.commit()
                db.refresh(user)
            return user

    @staticmethod
    def get_chats(user_id: str, search: Optional[str] = None):
        """Get all chats for a user, optionally filtered by search term"""
        with get_db() as db:
            query = select(Chat).filter(Chat.user_id == user_id).order_by(desc(Chat.updated_at))
            if search:
                query = query.filter(Chat.name.ilike(f"%{search}%"))
            return db.execute(query).scalars().all()

    @staticmethod
    def get_chat(chat_id: str) -> Optional[Chat]:
        """Get a specific chat by ID"""
        with get_db() as db:
            return db.query(Chat).filter(Chat.id == chat_id).first()

    @staticmethod
    def create_chat(user_id: str, name: str) -> Chat:
        """Create a new chat"""
        with get_db() as db:
            chat = Chat(user_id=user_id, name=name)
            db.add(chat)
            db.commit()
            db.refresh(chat)
            return chat

    @staticmethod
    def update_chat(chat_id: str, name: Optional[str] = None, is_named_by_llm: Optional[bool] = None) -> Chat:
        """Update chat information"""
        with get_db() as db:
            chat = db.query(Chat).filter(Chat.id == chat_id).first()
            if chat:
                if name is not None:
                    chat.name = name
                if is_named_by_llm is not None:
                    chat.is_named_by_llm = is_named_by_llm
                db.commit()
                db.refresh(chat)
            return chat

    @staticmethod
    def delete_chat(chat_id: str):
        """Delete a chat and its messages"""
        with get_db() as db:
            # Delete messages first due to foreign key constraint
            db.query(Message).filter(Message.chat_id == chat_id).delete()
            db.query(Chat).filter(Chat.id == chat_id).delete()
            db.commit()

    @staticmethod
    def get_messages(chat_id: str, include_regenerated: bool = False):
        """Get messages for a chat, optionally including regenerated versions"""
        with get_db() as db:
            if include_regenerated:
                # Get all messages including regenerated ones
                return db.query(Message).filter(
                    Message.chat_id == chat_id
                ).order_by(Message.created_at).all()
            else:
                # Get only the latest version of each message
                # First, get all original messages (not regenerated from others)
                base_messages = db.query(Message).filter(
                    Message.chat_id == chat_id,
                    Message.original_message_id == None
                ).all()
                
                # For each regenerated message, get its latest version
                messages = []
                for msg in base_messages:
                    if msg.is_regenerated:
                        # Get the latest regeneration of this message
                        latest = db.query(Message).filter(
                            Message.original_message_id == msg.id
                        ).order_by(desc(Message.created_at)).first()
                        if latest:
                            messages.append(latest)
                        else:
                            messages.append(msg)
                    else:
                        messages.append(msg)
                
                # Sort by original creation time
                messages.sort(key=lambda m: m.created_at)
                return messages

    @staticmethod
    def add_message(chat_id: str, role: str, content: str, turn_number: int, original_message_id: Optional[str] = None) -> Message:
        """Add a new message to a chat"""
        with get_db() as db:
            # Create message with current timestamp
            now = datetime.utcnow()
            message = Message(
                chat_id=chat_id,
                role=role,
                content=content,
                turn_number=turn_number,
                created_at=now,
                original_message_id=original_message_id,
                is_regenerated=False
            )
            db.add(message)
            
            # Update chat's updated_at timestamp
            chat = db.query(Chat).filter(Chat.id == chat_id).first()
            if chat:
                chat.updated_at = now
            
            db.commit()
            db.refresh(message)
            return message

    @staticmethod
    def get_message(message_id: str) -> Optional[Message]:
        """Get a specific message by ID"""
        with get_db() as db:
            return db.query(Message).filter(Message.id == message_id).first()

    @staticmethod
    def mark_message_regenerated(message_id: str) -> Optional[Message]:
        """Mark a message as regenerated"""
        with get_db() as db:
            message = db.query(Message).filter(Message.id == message_id).first()
            if message:
                message.is_regenerated = True
                db.commit()
                db.refresh(message)
            return message

    @staticmethod
    def get_reaction(message_id: str, user_id: str) -> Optional[MessageReaction]:
        """Get a user's reaction to a specific message"""
        with get_db() as db:
            return db.query(MessageReaction).filter(
                and_(
                    MessageReaction.message_id == message_id,
                    MessageReaction.user_id == user_id
                )
            ).first()

    @staticmethod
    def add_or_update_reaction(message_id: str, user_id: str, reaction_type: str) -> MessageReaction:
        """Add or update a reaction to a message"""
        with get_db() as db:
            # Check for existing reaction
            reaction = db.query(MessageReaction).filter(
                and_(
                    MessageReaction.message_id == message_id,
                    MessageReaction.user_id == user_id
                )
            ).first()

            if reaction:
                # Update existing reaction
                if reaction.reaction_type != reaction_type:
                    reaction.reaction_type = reaction_type
                    reaction.created_at = datetime.utcnow()
            else:
                # Create new reaction
                reaction = MessageReaction(
                    message_id=message_id,
                    user_id=user_id,
                    reaction_type=reaction_type
                )
                db.add(reaction)

            db.commit()
            db.refresh(reaction)
            return reaction

    @staticmethod
    def remove_reaction(message_id: str, user_id: str):
        """Remove a user's reaction from a message"""
        with get_db() as db:
            db.query(MessageReaction).filter(
                and_(
                    MessageReaction.message_id == message_id,
                    MessageReaction.user_id == user_id
                )
            ).delete()
            db.commit()

    @staticmethod
    def get_last_assistant_message(chat_id: str) -> Optional[Message]:
        """Get the last assistant message in a chat"""
        with get_db() as db:
            return db.query(Message).filter(
                and_(
                    Message.chat_id == chat_id,
                    Message.role == "assistant"
                )
            ).order_by(desc(Message.created_at)).first()
