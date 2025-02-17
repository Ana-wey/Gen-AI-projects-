import streamlit as st
import google.generativeai as genai

f = open("C:\\Users\\MSI\\Desktop\\internship_2025\\api-key\\key-genai1.txt")
key = f.read()

st.title('💬 Python Code Reviewer')

# Intialisting the model

system_prompt = """Analyze the submitted pyhton code and identify potential bugs, errors, or areas of improvement in a very simple manner and answer it in 2 to 3 points and  also generate the fixed code snippets and give sub title as fixed code snippets,if not python code politely reply and ask for python code only."""

genai.configure(api_key=key)

model = genai.GenerativeModel(model_name = 'models/gemini-2.0-flash-thinking-exp',
                             system_instruction = system_prompt)

user_input = st.text_area("Enter your code here:",value="",height=200)

btn_click = st.button("generate")

st.subheader('Code Review')

if btn_click == True:
    response = model.generate_content(user_input)
    st.write(response.text)


