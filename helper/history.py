from database.config import get_db_connection
from langchain_core.messages import AIMessage, HumanMessage
from bson.objectid import ObjectId

def get_chat_history(conversation_id = ObjectId("66b0ac43fc50f13c7cbe785e"), max_pairs=5):
    """
    Retrieve and format chat history as a list of AIMessage and HumanMessage objects.

    Parameters:
    - conversation_id (str): The ID of the conversation to retrieve.
    - max_pairs (int): The maximum number of message pairs to return.

    Returns:
    - list: A list of AIMessage and HumanMessage objects.
    """

    try:
        db = get_db_connection()
        collection = db["conversations"]
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return []
    
    try:
        # Retrieve the conversation document
        conversation = collection.find_one({"conversation_id": conversation_id})
        # print(f"Conversation : {conversation}")
    except Exception as e:
        print(f"Error retrieving conversation: {e}")
        return []
    
     # Check if the conversation and messages exist
    if not conversation or 'messages' not in conversation:
        print("No conversation found or conversation has no messages.")
        return []
    
    messages = conversation['messages']
    total_messages = max_pairs * 2
    last_messages = messages[-total_messages:]
    
    chat_history = []

    # Separate user and agent messages and append them to chat_history
    for message in last_messages:
        if message['sender'] == 'user':
            chat_history.append(HumanMessage(content=message['content']))
        elif message['sender'] == 'agent':
            chat_history.append(AIMessage(content=message['content']))
    
    return chat_history