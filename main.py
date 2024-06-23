import streamlit as st
from openai import OpenAI
# Set OpenAI API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-2024-05-13"

if "text" not in st.session_state:
    st.session_state["text"] = "Empty text"

with st.sidebar:
    st.header("Document text")
    text = st.text_area(
        label="xdxdlol",
        key="text",
        height=550,
        label_visibility='hidden'
        )

st.title("ChatGPT-like clone")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

system_message = "Ты полезный помощник. Твоя задача - составить документ на основе примера. Задавай вопросы по содержанию документа, чтобы максимально подробно, точно и структурировано написать документ. Документ должен быть приближен по структуре к примеру. Есть правило: 1 сообщение - 1 вопрос. Очень важно в конце каждого сообщения указывать текст, который есть на данный момент. Если я не достаточно точно ответил на вопрос - переспроси его."

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)
       
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            temperature=0.7,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "system", "content": 'Текущий текст: ' + st.session_state["text"]},
                *[
                    {"role": message["role"], "content": message["content"]} for message in st.session_state.messages
                ]
            ],
            stream=True,
        )
        response = st.write_stream(stream)

    st.session_state.messages.append({"role": "assistant", "content": response}) 

    st.session_state["text"] += response
    print(text)





