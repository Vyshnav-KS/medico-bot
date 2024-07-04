from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate
from chain.prompts.system_prompt import SYSTEM_PROMPT
from langchain.agents import initialize_agent, AgentExecutor, create_react_agent
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from chain.tools import change_name_tool, change_background_tool
# import streamlit as st


load_dotenv()
tools = [change_name_tool, change_background_tool]

def get_response(user_query, chat_history, context):
    
    try:
        # template = SYSTEM_PROMPT +  "Context : {context}, Chat history: {chat_history}, User question: {user_question}"

        # prompt = ChatPromptTemplate.from_template(template)
        prompt = hub.pull("hwchase17/react-chat")
        model = ChatOpenAI(model='gpt-3.5-turbo')
        # chain = prompt | llm | StrOutputParser()

        agent = create_react_agent(model, tools, prompt)
        agent_executor = AgentExecutor(agent=agent, tools=tools)
        
        # return chain.invoke({
        #     "chat_history": chat_history,
        #     "user_question": user_query,
        #     "context": context
        # })
        print(f"User query: {user_query}")
        return agent_executor.invoke({
            "input": f"{SYSTEM_PROMPT}, User question: {user_query}, Context : {context}",
            "chat_history": chat_history,
            # "context": context
        })
    except Exception as e:
        print(e)
        return None

# def get_response(user_query, chat_history, context):

#     llm = ChatOpenAI(model='gpt-3.5-turbo')
#     PREFIX = """Answer the following questions as best you can. You have access to the following tools:"""
#     FORMAT_INSTRUCTIONS = """Use the following format:

#     Question: the input question you must answer
#     Context: the context you should use
#     Thought: you should always think about what to do
#     Action: the action to take, should be one of [{tool_names}]
#     Action Input: the input to the action
#     Observation: the result of the action
#     ... (this Thought/Action/Action Input/Observation can repeat N times)
#     Thought: I now know the final answer
#     Final Answer: the final answer to the original input question"""
#     SUFFIX = """Begin!

#     Question: {input}
#     Context: {context}
#     Thought:{agent_scratchpad}"""

#     conversational_agent = initialize_agent(
#         agent="chat-conversational-react-description",
#         tools=tools,
#         llm=llm,
#         max_iterations =3,
#         early_stopping_method = "generate",
#         memory=ConversationBufferWindowMemory(k=3, return_messages=True, memory_key='chat_history'),
#         verbose=True,
#         agent_kwargs={
#             'prefix':PREFIX,
#             'format_instructions':FORMAT_INSTRUCTIONS,
#             'suffix':SUFFIX
#         }
#     )

#     conversational_agent({
#         "chat_history": chat_history,
#         "user_question": user_query,
#         "context": context
#     })



    