
from langchain_core.outputs import LLMResult
from chain.response_generator import get_response
from langchain_core.callbacks import StdOutCallbackHandler
from langchain.callbacks.streaming_stdout_final_only import FinalStreamingStdOutCallbackHandler
from typing import Any
from flask_socketio import send, emit
import time
from flask import Flask
from flask_socketio import SocketIO


# # set_llm_cache(InMemoryCache())
# content_checker = True
# start_stream = False
# check_colon = False

# class MyCallbackHandler(FinalStreamingStdOutCallbackHandler):
#      def on_llm_new_token(self, token: str, **kwargs: Any) -> Any:
#         """Run on new LLM token. Only available when streaming is enabled."""
#         global content_checker, start_stream, check_colon
#         self.content = ""
#         if content_checker:
#             self.content += token

#         if content_checker and "Final" in self.content:
#             check_colon = True
#             self.content = ""

#         if check_colon and ":" in self.content:
#             content_checker = False
#             start_stream = True
#             check_colon = False
#             self.content = ""
#             return
            
#         if start_stream:
#             send_ai_res(token)
#             # print(token)
#         # send_ai_res(token)

#      def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
#          content_checker = True
#          start_stream = False
         

class MyCallbackHandler(FinalStreamingStdOutCallbackHandler):
    def __init__(self):
        # Initialize instance variables instead of using global variables
        self.content_checker = True
        self.start_stream = False
        self.check_colon = False
        self.content = ""

    def on_llm_new_token(self, token: str, **kwargs: Any) -> Any:
        """Run on new LLM token. Only available when streaming is enabled."""
        if self.content_checker:
            self.content += token

        if self.content_checker and "Final" in self.content:
            self.check_colon = True
            self.content = ""

        if self.check_colon and ":" in self.content:
            self.content_checker = False
            self.start_stream = True
            self.check_colon = False
            self.content = ""
            return
            
        if self.start_stream:
            send_ai_res(token)
            # print(token)
        # send_ai_res(token)

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        # Reset instance variables at the end of the response
        self.content_checker = True
        self.start_stream = False
        self.content = ""
            


handler_1 = MyCallbackHandler()


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

def run_test_prompt(input_text):
    executor = get_response()
    executor.invoke({
            "input": input_text,
            "chat_history": [],
        },
        {"callbacks": [handler_1]},
    )

def send_ai_res(msg):
    emit('ai_res', msg, broadcast=False, ignore_queue=False)
    socketio.sleep(0)

@socketio.on('start_stream')
def handle_messagex(data):
    print('received message: ' + data)
    emit("message", "this is a message from the server")
    socketio.sleep(0)
    # run_test_prompt("What is Myopia?")

@socketio.on('send_message')
def handle_message(data):
    print('received message from client: ' + data)
    run_test_prompt(data)

socketio.run(app, port=5001)