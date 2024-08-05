from database.config import get_db_connection
from bson.objectid import ObjectId
from datetime import datetime, timezone

# Get database connection and access collections
db = get_db_connection()
users = db["users"]
conversations = db["conversations"]

def get_user(user_id):
    """
    Retrieves a user document from the database by user_id.
    
    Args:
        user_id (str): The ID of the user to retrieve
    
    Returns:
        dict: User document or None if not found
    """
    try:
        return users.find_one({"user_id": user_id})
    except Exception as e:
        print(f"Error retrieving user: {e}")
        raise

def create_user(user_id):
    """
    Creates a new user document in the database.
    
    Args:
        user_id (str): The ID of the new user
    
    Returns:
        dict: The newly created user document
    """
    try:
        user = {
            "user_id": user_id,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
            "conversations": []
        }
        users.insert_one(user)
        return user
    except Exception as e:
        print(f"Error creating user: {e}")
        raise

def update_user_conversations(user_id, conversations):
    """
    Updates the conversations field of a user document.
    
    Args:
        user_id (str): The ID of the user to update
        conversations (list): The updated list of conversations
    
    Raises:
        Exception: If the update operation fails
    """
    try:
        users.update_one({"user_id": user_id}, {"$set": {"conversations": conversations, "updated_at": datetime.now(timezone.utc)}})
    except Exception as e:
        print(f"Error updating user conversations: {e}")
        raise

def create_conversation(user_id):
    """
    Creates a new conversation document in the database.
    
    Args:
        user_id (str): The ID of the user who started the conversation
    
    Returns:
        ObjectId: The ID of the newly created conversation
    """
    try:
        conversation_id = ObjectId()
        conversation = {
            "_id": conversation_id,
            "user_id": user_id,
            "conversation_id": conversation_id,
            "messages": [],
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc)
        }
        conversations.insert_one(conversation)
        return conversation_id
    except Exception as e:
        print(f"Error creating conversation: {e}")
        raise

def get_conversation(conversation_id):
    """
    Retrieves a conversation document from the database by conversation_id.
    
    Args:
        conversation_id (ObjectId): The ID of the conversation to retrieve
    
    Returns:
        dict: Conversation document or None if not found
    """
    try:
        return conversations.find_one({"_id": conversation_id})
    except Exception as e:
        print(f"Error retrieving conversation: {e}")
        raise

def add_message_to_conversation(conversation_id, message):
    """
    Adds a message to a conversation document.
    
    Args:
        conversation_id (ObjectId): The ID of the conversation to update
        message (dict): The message to add
    
    Raises:
        Exception: If the update operation fails
    """
    try:
        conversations.update_one(
            {"_id": conversation_id},
            {"$push": {"messages": message}, "$set": {"updated_at": datetime.now(timezone.utc)}}
        )
    except Exception as e:
        print(f"Error adding message to conversation: {e}")
        raise
