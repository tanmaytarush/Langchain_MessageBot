import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

# App Configurations
st.set_page_config(page_title="Stream Chatbot", page_icon = "*")
st.title("Stream Chatbot")

def get_response(user_query, chat_history):
    template = """
        Generate Responses for a Chat Based on:
        chat_history = {chat_history}
        user_query = {user_query}
    """

    prompt = ChatPromptTemplate.from_template(template)
    llm = ChatOpenAI()

    chain = prompt | llm | StrOutputParser()

    return chain.invoke({
        "user_query": user_query,
        "chat_history": chat_history,
    })


# Session State
if "chat_history" not in st.session_state:
    st.session_state.chat_history =[
        AIMessage(content = "Hello! How can I help you ?")
    ] 


# Conversation
for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.write(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.write(message.content)


# User Input
user_query = st.chat_input("Type Your Message Here ! ")

if user_query is not None and user_query!="":
    st.session_state.chat_history.append(HumanMessage(content=user_query))

    with st.chat_message("Human"):
        st.markdown(user_query)

    with st.chat_message("AI"):
        response = get_response(user_query, st.session_state.chat_history)
        st.write(response)

    st.session_state.chat_history.append(response)