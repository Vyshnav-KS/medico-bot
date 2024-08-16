from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from fastapi.responses import HTMLResponse
from fastapi.exceptions import HTTPException
from typing import Optional
from pathlib import Path
from utility import verify_token
from chain.response_generator import create_gen
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from chain.response_generator import MyCallbackHandler

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# HTML serving endpoint
@app.get("/")
async def get():
    html_path = Path("chat.html")
    return HTMLResponse(html_path.read_text())

# Dependency to get and verify the token
async def get_current_user(token: Optional[str] = None):
    if token is None:
        raise HTTPException(status_code=400, detail="Token is required")
    user = verify_token(token)
    if user is None:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    return user

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, token: str):
    user = await get_current_user(token)
    await websocket.accept()
    print("From websocket")

    try:
        while True:
            # await asyncio.sleep(0.1)

            handler = MyCallbackHandler()

            query = await websocket.receive_text()
            await websocket.send_text(f"Query: {query}, ---user :{user['user_id']} ---")

            # Create a generator to stream tokens
            async for token in create_gen(query, [], handler):  # Pass empty chat history for now
                await websocket.send_text(token)
                # await asyncio.sleep(0.1)

            # Optional: Send a completion message
            await websocket.send_text("----TOKEN PRINTING COMPLETED----")

    except WebSocketDisconnect:
        print(f"Client disconnected: user_id {user['user_id']}")
    except Exception as e:
        print(f"Error occurred: {e}")




# from fastapi import FastAPI, Request
# from fastapi.responses import StreamingResponse
# from chain.response_generator import create_gen
# from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @app.get("/")
# async def get():
#     with open("app.html", "r") as file:
#         html_content = file.read()
#     return html_content

# async def stream_response(query: str):
#     response_generator = create_gen(query, chat_history=[])
#     async for token in response_generator:
#         yield token

# @app.post("/query")
# async def query(request: Request):
#     data = await request.json()
#     query = data.get("query", "")
#     if not query:
#         return {"error": "Query is required"}
    
#     return StreamingResponse(stream_response(query), media_type="text/plain")

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)


# from fastapi import FastAPI, WebSocket, WebSocketDisconnect
# from fastapi.middleware.cors import CORSMiddleware
# from typing import List

# app = FastAPI()

# # Allow CORS for local development. This allows requests from your frontend (e.g., http://127.0.0.1:5500).
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Replace with your frontend URL
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Class to manage active WebSocket connections
# class ConnectionManager:
#     def __init__(self):
#         self.active_connections: List[WebSocket] = []

#     # Method to connect a new WebSocket client
#     async def connect(self, websocket: WebSocket):
#         await websocket.accept()  # Accept the WebSocket connection
#         self.active_connections.append(websocket)  # Add to the list of active connections

#     # Method to disconnect a WebSocket client
#     def disconnect(self, websocket: WebSocket):
#         self.active_connections.remove(websocket)  # Remove from the list of active connections

#     # Method to send a personal message to a specific client
#     async def send_personal_message(self, message: str, websocket: WebSocket):
#         await websocket.send_text(message)  # Send message to the specific WebSocket connection

#     # Method to broadcast a message to all connected clients (not used in this example)
#     async def broadcast(self, message: str):
#         for connection in self.active_connections:
#             await connection.send_text(message)  # Send message to all active connections

# # Create an instance of ConnectionManager to handle connections
# manager = ConnectionManager()

# # Define the WebSocket endpoint that clients will connect to
# @app.websocket("/ws/{client_id}")
# async def websocket_endpoint(websocket: WebSocket, client_id: str):
#     await manager.connect(websocket)  # Connect the client
#     try:
#         while True:
#             data = await websocket.receive_text()  # Receive a message from the client
#             response = handle_user_query(data)  # Process the user's query
#             await manager.send_personal_message(f"AI: {response}", websocket)  # Send the response back to the client
#     except WebSocketDisconnect:
#         manager.disconnect(websocket)  # Handle client disconnect

# # Function to handle and process user queries (stubbed for now)
# def handle_user_query(query: str) -> str:
#     # Here you would integrate your AI model to process the query
#     return f"Processed query: {query}"

# # Run the FastAPI application using Uvicorn
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)





