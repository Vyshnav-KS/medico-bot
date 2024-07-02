from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from chain.prompts.system_prompt import SYSTEM_PROMPT
from langchain.agents import initialize_agent, AgentExecutor
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from chain.tools import change_name_tool
# import streamlit as st


load_dotenv()
tools = [change_name_tool]

def get_response(user_query, chat_history, context):
    
    try:
        template = SYSTEM_PROMPT +  "Context : {context}, Chat history: {chat_history}, User question: {user_question}"

        prompt = ChatPromptTemplate.from_template(template)
        llm = ChatOpenAI(model='gpt-3.5-turbo')
        chain = prompt | llm | StrOutputParser()
        
        return chain.stream({
            "chat_history": chat_history,
            "user_question": user_query,
            "context": context
        })
    except Exception as e:
        print(e)
        return None

    # llm = ChatOpenAI(model='gpt-3.5-turbo')

    # conversational_agent = initialize_agent(
    #     agent="chat-conversational-react-description",
    #     tools=tools,
    #     llm=llm,
    #     verbose=True,
    #     max_iterations =3,
    #     early_stopping_method = "generate",
    #     memory=ConversationBufferWindowMemory(k=3, return_messages=True, memory_key='chat_history'),
    #     verbose=True,
    # )

    