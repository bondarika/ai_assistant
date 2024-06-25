import streamlit as st
from openai import OpenAI
import docx 

def read_docx(file_path):
    doc = docx.Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

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

# Read system dataset
with open("dataset.txt", "r") as file:
    dataset = file.read()

# Read tech specs document
tech_specs = read_docx("tech-specs.docx")

# Combine dataset and tech specs
combined_content = dataset + "\n" + tech_specs


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
                {"role": "system", "content": combined_content},
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


# добавить возмодность пользователю добавлять свой документ?
# как убрать постоянное обновление стейта, чтобы текст не выписывался каждый раз с нуля?
# почему лагает левое окно, если его обновить вручную?
# а как будет работать хранение всего документа?

# Забирать только ```plaintext! Внести в код изменения
# Внести инструкцию обнуления
