import streamlit as st
from docx import Document
from openai import OpenAI

# Функция для чтения текста из DOCX файла
def read_docx(file_path):
    doc = Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return "\n".join(full_text)

# Настройки OpenAI (замените 'YOUR_API_KEY' на ваш ключ API)
openai.api_key = "YOUR_API_KEY"

# Путь к файлу DOCX
docx_file_path = "tech-specs.docx"

# Чтение содержимого файла DOCX
doc_text = read_docx(docx_file_path)

# Настройка клиента OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Интерфейс Streamlit
st.title("ChatGPT-like clone")

# Инициализация состояния приложения
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-2024-05-13"
if "text" not in st.session_state:
    st.session_state["text"] = "Empty text"
if "messages" not in st.session_state:
    st.session_state.messages = []

# Отображение истории сообщений
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Чтение системного датасета
with open("dataset.txt", "r") as file:
    dataset = file.read()

# Прием пользовательского ввода
if prompt := st.chat_input("What is up?"):
    # Добавление сообщения пользователя в историю чата
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Отображение ответа ассистента в контейнере сообщений чата
    with st.chat_message("assistant"):
        st.markdown("Loading...")

        # Формирование полного запроса к OpenAI API
        full_prompt = [
            {"role": "system", "content": dataset},
            {"role": "system", "content": 'Текущий текст: ' + st.session_state["text"]},
            {"role": "user", "content": prompt}
        ]

        # Добавление всех предыдущих сообщений в запрос
        for message in st.session_state.messages:
            full_prompt.append({"role": message["role"], "content": message["content"]})

        # Отправка запроса к OpenAI API
        stream = client.chat_completions.create(
            model=st.session_state["openai_model"],
            temperature=0.5,
            messages=full_prompt,
            stream=True,
        )

        # Получение ответа от OpenAI и отображение ассистента
        response = ""
        for chunk in stream:
            if 'content' in chunk.choices[0].delta:
                response += chunk.choices[0].delta.content

        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

        # Обновление текущего текста, исключая ответы ассистента
        response_lines = response.split("\n")
        new_text_lines = [line for line in response_lines if not line.startswith("Assistant:")]
        if new_text_lines:
            st.session_state["text"] = "\n".join(new_text_lines)