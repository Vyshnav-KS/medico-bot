from datetime import datetime, timezone
from bson.objectid import ObjectId
from database.db import get_user, create_user, update_user_conversations, create_conversation, get_conversation, add_message_to_conversation
from response_generator import get_response

def user_request(request_data):
    """
    Processes a user request by handling user queries and conversations.
    
    Args:
        request_data (dict): Contains user_id, user_query, and optionally conversation_id
    
    Returns:
        dict: Response including conversation_id and agent response
    """
    try:
        user_id = request_data['user_id']
        user_query = request_data['user_query']
        conversation_id = request_data.get('conversation_id')

        # Retrieve or create user
        user = get_user(user_id)
        if not user:
            user = create_user(user_id)

        # Handle conversation creation or retrieval
        if not conversation_id:
            conversation_id = create_conversation(user['_id'])
            user['conversations'].append({
                "conversation_id": conversation_id,
                "started_at": datetime.now(timezone.utc),
                "ended_at": None
            })
            update_user_conversations(user_id, user['conversations'])
            chat_history = []
        else:
            conversation = get_conversation(ObjectId(conversation_id))
            if not conversation:
                raise ValueError("Invalid conversation_id provided.")
            chat_history = conversation['messages']

        # Get response from agent
        response_content = get_response(user_query, chat_history)
        if response_content is None:
            raise ValueError("Failed to generate response.")

        # Prepare messages
        user_message = {
            "message_id": ObjectId(),
            "sender": "user",
            "content": user_query,
            "timestamp": datetime.now(timezone.utc)
        }
        agent_message = {
            "message_id": ObjectId(),
            "sender": "agent",
            "content": response_content.get("output"),
            "timestamp": datetime.now(timezone.utc)
        }

        # Update conversation with new messages
        add_message_to_conversation(conversation_id, user_message)
        add_message_to_conversation(conversation_id, agent_message)

        return {"conversation_id": str(conversation_id), "response": response_content}
    
    except Exception as e:
        print(f"Error processing user request: {e}")
        return {"error": str(e)}

# Example usage
if __name__ == "__main__":
    request_data = {
        "user_id": "12345",
        "user_query": "What measures are being taken to monitor and prevent the spread of bird-related coronaviruses?",
        "conversation_id": ObjectId("66b0ac43fc50f13c7cbe785e")  # Or use a real conversation ID if it's an ongoing chat
    }
    print(user_request(request_data))
