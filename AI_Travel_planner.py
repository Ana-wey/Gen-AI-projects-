import streamlit as st
import datetime

f = open("C:\\Users\\MSI\\Desktop\\internship_2025\\api-key\\key-genai1.txt")
key = f.read()

st.title('🛫 AI-Powered Travel Planner')

# logic 3

from langchain_core.output_parsers import StrOutputParser

output_parser = StrOutputParser()

# logic 1

from langchain_core.prompts import ChatPromptTemplate
chat_template = ChatPromptTemplate(
    messages= [ (
        'system',"""you are an helpful AI assistant who assist users in finding optimal travel options between a given source and destination for given date at that time,generate various travel choices such as cab, train, bus, and flights, along with their estimated costs  for the passengers  and time taken by each travel choices,facilities available on each traval choices,and represent the following information in a tabular format.

        """),
        ('human','Travel options from {source} and {destination} on {date}' )
        ],
        #partial_variables = {'Output_instruction':output_parser.get_format_instructions()}
)


# logic 2

from  langchain_google_genai import ChatGoogleGenerativeAI

chat_model = ChatGoogleGenerativeAI(api_key = key , model = 'gemini-2.0-flash-exp')

chain = chat_template | chat_model | output_parser


Source = st.text_input("🚘"+"Enter Source")  

Destination = st.text_input("🚘"+"Enter  Destination")

Date = st.date_input("🗓️ Date of Journey", value=None,min_value='today')

raw_input={'source':Source,'destination': Destination,'date' : Date,}

btn_click = st.button(" 🔍 "+" Search ")

if btn_click == True:
    #st.write("🗓️ Travel Date :", Date)
    response = chain.invoke(raw_input)
    st.write(response)


