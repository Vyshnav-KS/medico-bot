from dotenv import load_dotenv
from chain.prompts.system_prompt import system_instruction
from langchain.agents import AgentExecutor, create_react_agent
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
# from langchain.memory import ChatMessageHistory
from langchain.callbacks.streaming_stdout_final_only import FinalStreamingStdOutCallbackHandler
from langchain.callbacks.streaming_aiter import AsyncIteratorCallbackHandler
from chain.tools.medical_tool import medical_tool
from chain.tools.general_tool import general_tool
from chain.tools.application_tool import application_tool
from langchain_community.cache import InMemoryCache
from langchain_openai import AzureChatOpenAI
from langchain.globals import set_llm_cache
from langsmith import traceable
from config.settings import settings
from langchain import hub
from langchain_core.runnables.history import RunnableWithMessageHistory
from helper.history import get_chat_history
from typing import Any, AsyncIterator, Literal, Union, cast
from langchain_core.outputs import LLMResult
import asyncio
from langchain_core. callbacks import StdOutCallbackHandler

# set_llm_cache(InMemoryCache())

class MyCallbackHandler(AsyncIteratorCallbackHandler):
    def __init__(self):
        # Initialize instance variables instead of using global variables
        self.content_checker = True
        self.start_stream = False
        self.check_colon = False
        self.content = ""
        self.done = asyncio.Event()
        self.queue = asyncio.Queue()

    # async def on_llm_new_token(self, token: str, **kwargs: Any) -> Any:
    #     """Run on new LLM token. Only available when streaming is enabled."""
    #     if self.content_checker:
    #         self.content += token

    #     if self.content_checker and "Final" in self.content:
    #         self.check_colon = True
    #         self.content = ""

    #     if self.check_colon and ":" in self.content:
    #         self.content_checker = False
    #         self.start_stream = True
    #         self.check_colon = False
    #         self.content = ""
    #         return
            
    #     if self.start_stream:
    #         await self.queue.put(token)
    #         # print("TOKEN: ", token)
    
    # async def aiter(self):
    #     """Async iterator to yield tokens."""
    #     while not self.done.is_set() or not self.queue.empty():
    #         token = await self.queue.get()
    #         # print(f"Yielding token: {token}")  # Debug log
    #         yield token
    #         print("Yielded : ", token)

    async def aiter(self) -> AsyncIterator[str]:
        while not self.queue.empty() or not self.done.is_set():
            # Wait for the next token in the queue,
            # but stop waiting if the done event is set
            # print("************* ", 1)
            done, other = await asyncio.wait(
                [
                    # NOTE: If you add other tasks here, update the code below,
                    # which assumes each set has exactly one task each
                    asyncio.ensure_future(self.queue.get()),
                    asyncio.ensure_future(self.done.wait()),
                ],
                return_when=asyncio.FIRST_COMPLETED,
            )
            # print("************* ", 2)

            # Cancel the other task
            if other:
                other.pop().cancel()
            # print("************* ", 3)

            # Extract the value of the first completed task
            token_or_done = cast(Union[str, Literal[True]], done.pop().result())
            # print("************* ", 4)

            # If the extracted value is the boolean True, the done event was set
            if token_or_done is True:
                break

            # print("************* ", 5)

            # Otherwise, the extracted value is a token, which we yield
            print("\n\n>>>>>>>>>>>>>>>>>>> \n", token_or_done, "\n\n")
            yield token_or_done

            # print("************* ", 6)
    
    
    async def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        # Reset instance variables at the end of the response
        self.content_checker = True
        self.start_stream = False
        self.check_colons = False
        self.content = ""
        self.done.set()

@traceable
async def get_response(input_text, chat_history, handler):

    load_dotenv()
    tools = [application_tool, medical_tool, general_tool]
    
    try:
        instructions = system_instruction
        base_prompt = hub.pull("langchain-ai/react-agent-template")
        # base_prompt = hub.pull("hwchase17/react")
        prompt = base_prompt.partial(instructions=instructions)

        model = AzureChatOpenAI(
            model=settings.azure_openai_settings.model,
            openai_api_type=settings.azure_openai_settings.openai_api_type,
            callbacks=[
                FinalStreamingStdOutCallbackHandler(
                    answer_prefix_tokens = [
                        "Final", "Answer"
                    ]
                )
            ],
            streaming=True
        )

        agent = create_react_agent(model, tools, prompt)
        agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            handle_parsing_errors=True,
            max_iterations=3,
            verbose=False,
            return_intermediate_steps=False,
            early_stopping_method="generate"
        )
        
        # print(f"User query: {user_query}\nChat history: {chat_history}\n")

        # return agent_executor
        response  = await agent_executor.ainvoke(
            {
                "input": input_text,
                "chat_history": chat_history,
            },
            {"callbacks": [handler]},
        )
        return response
        
    except Exception as e:
        print(e)

async def create_gen(query: str, chat_history: list, handler):
    task = asyncio.create_task(
        get_response(
            query,
            chat_history,
            handler
        )
    )
    print("Going to iterate over the handler")
    async for token in handler.aiter():
        # print("Token: ", token)
        # print(f"Yielding token: {token}")
        yield token
    print("\nAwaiting the Task")
    await task
    print("\nTask ended")


# async def main():
#     chat_history = []
#     user_query = "What is Myopia?"
#     async for token in create_gen(user_query, chat_history):
#         print(token)

# if __name__ == "__main__":
#     asyncio.run(main())