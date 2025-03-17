import streamlit as st
import uuid

st.title("📖 AI-Conversational Data Science Tutor")

### step - 1 : import chat model and configure API Key

f = open("C:\\Users\\MSI\\Desktop\\internship_2025\\api-key\\key-genai1.txt")
key = f.read()

# logic 2:

from langchain_google_genai import ChatGoogleGenerativeAI
chat_model = ChatGoogleGenerativeAI(api_key = key , model = 'gemini-1.5-pro')





### step - 2 : Create Chat Template

# logic 1 :
from langchain_core.prompts import ChatPromptTemplate , MessagesPlaceholder

chat_template = ChatPromptTemplate(
                messages=[("system" ,"""you are a helpful data science tutor which is tasked to resolve only the data science doubts of the user using simple language and diagrams,charts also."""),
                          MessagesPlaceholder(variable_name="chat_history" ),
                          ("human","{human_input}")]
)




### step - 3 : Create Output Parser

# Logic 3 :

from langchain_core.output_parsers import StrOutputParser
outout_parser = StrOutputParser()


### step - 4 : Initializing the memory

from langchain_community.chat_message_histories import SQLChatMessageHistory

def get_session_message_history_from_db(session_id):
    chat_message_history = SQLChatMessageHistory(
                                   session_id=session_id, 
                                   connection="sqlite:///C:\\Users\\MSI\Desktop\\internship_2025\\streamlit_practice\\Virtual_Env\\chats_data\\sqlite.db"
                               )
    return chat_message_history


### step - 5 : Built the Chain 


chain =  chat_template | chat_model | outout_parser



# Use RunnableWithMessageHistory to load 
from langchain_core.runnables.history import RunnableWithMessageHistory

conversation_chain = RunnableWithMessageHistory(
                        chain, 
                        get_session_message_history_from_db,
                        input_messages_key="human_input", 
                        history_messages_key="chat_history"
                    )

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(f"{message['content']}")

# React to user input

session_id = uuid.uuid1()

config = {"configurable": {"session_id": session_id}}


query = st.chat_input("Ask anything related to Data Science")
raw_input = {'human_input':query}

if query:
    # Display user message in chat message container
    if query.lower() in ['bye', 'quit', 'exit']:
        st.stop()
    response = conversation_chain.invoke(raw_input,config=config)
    
    with st.chat_message("user"):
        st.markdown(f"{query}")
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": query})

    with st.chat_message("assistant"):
        st.markdown(f"{response}")

    st.session_state.messages.append({"role": "assistant", "content": response})