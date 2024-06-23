import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("ChatGPT-like clone")

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-2024-05-13"

if "text" not in st.session_state:
    st.session_state["text"] = "Empty text"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# read system dataset
file = open("dataset.txt", "r")
dataset = file.read()

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)
       
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        print(st.session_state["text"])
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            temperature=0.5,
            messages=[
                {"role": "system", "content": dataset},
                {"role": "system", "content": 'Текущий текст: ' + st.session_state["text"]},
                *[
                    {"role": message["role"], "content": message["content"]} for message in st.session_state.messages
                ]
            ],
            stream=True,
        )
        response = st.write_stream(stream)

    st.session_state.messages.append({"role": "assistant", "content": response}) 

    index = response.find("Текущий текст:")
    if index != -1:
        st.session_state["text"] = response[index + 15:]
        # print(response[index + 15:])

    with st.sidebar:
        st.header("Document text")
        text = st.text_area(
            label="xdxdlol",
            key="text",
            height=550,
            label_visibility='hidden'
        )





