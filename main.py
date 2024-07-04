import json
import time
import streamlit as st
from openai import OpenAI, RateLimitError
import docx 

def read_docx(file_path):
    doc = docx.Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

def extract_plaintext(input_string):
    # Найдем начальную позицию маркера "```plaintext"
    start_marker = "Текущий текст:"
    end_marker = "---"
    
    start_index = input_string.find(start_marker)
    if start_index == -1:
        return ""
    
    # Смещаем начальную позицию на длину маркера
    start_index += len(start_marker)
    
    # Найдем конечную позицию маркера "```"
    end_index = input_string.find(end_marker, start_index)
    if end_index == -1:
        return ""
    
    # Извлечем текст между маркерами и уберем лишние пробелы
    extracted_text = input_string[start_index:end_index].strip()
    return extracted_text

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("ChatGPT-like clone")

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-2024-05-13"

if "text" not in st.session_state:
    st.session_state["document"] = "Empty text"

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

    st.session_state.messages = st.session_state.messages[-3:]

    with st.chat_message("user"):
        st.markdown(prompt)

    messages = [
                {"role": "system", "content": combined_content},
                {"role": "user", "content": st.session_state["document"]},
                *[
                    {"role": message["role"], "content": message["content"]} for message in st.session_state.messages
                ]
    ]

    # save messages to json file with timestamp in the file name
    with open(f"logs/messages_{int(time.time())}.json", "w") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)
       
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        # TODO: error handler RateLimitError. Error code: 429
        try:
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                temperature=0.7,
                messages=messages,
                stream=True,
            )
            print("@stream", str(stream))
            response = st.write_stream(stream)
        except RateLimitError as e:
            st.write("RateLimitError. Error code: 429"+ "\n You assigned rate limit " + str(e.rate_limit) + "\n" + str(e))

    st.session_state["document"] = extract_plaintext(response)
    st.session_state.messages.append({"role": "assistant", "content": response}) 
    
    with st.sidebar:
        st.header("Document text")
        st.markdown(st.session_state["document"])
        text = st.text_area(
            label="xdxdlol",
            key="document",
            height=550,
            label_visibility='hidden'
        )

# Cделать обработку ошибки при достижении лимита токенов в минуту 
# RateLimitError: Error code: 429  поймать!!
# Как убрать постоянное обновление стейта, чтобы текст не выписывался каждый раз с нуля?
# Почему лагает левое окно, если его обновить вручную? исправить
# Забирать только markdown! Внести в код изменения
# Внести инструкцию обнуления


# Передача текста через историю
# Вывод только изменяемого раздела


#ПОЗЖЕ
# Добавить возможность пользователю добавлять свой документ?
# А как будет работать хранение всего документа?




