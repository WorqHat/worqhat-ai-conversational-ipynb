import streamlit as st
import requests
import json

def send_files_and_question(files, question, training_data):
    url = 'https://api.worqhat.com/api/ai/content/v4'
    headers = {'Authorization': 'Bearer sk-caf41a358afe456286cd91f12c93199c'}
    data = {
        'question': question,
        'training_data': training_data,
        'model': 'aicon-v4-nano-160824',
        'stream_data': 'true'
    }
    files_to_send = [('files', (file.name, file, file.type)) for file in files]

    with requests.post(url, headers=headers, files=files_to_send, data=data, stream=True) as response:
        if response.status_code == 200:
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8')
                    json_data = json.loads(decoded_line)
                    content = json_data.get('content', '')
                    if content:
                        st.session_state.chat_history.append({'sender': 'Bot', 'message': content})
        else:
            return f"Error: {response.status_code}, {response.text}"

# Initialize session state to store chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# File uploader
uploaded_files = st.sidebar.file_uploader("Upload your files", type=["pdf", "png", "jpg"], accept_multiple_files=True)

# Chat interface
user_input = st.chat_input("Ask a question:", key="chat_input")
if user_input:
    # Append user question to chat history
    st.session_state.chat_history.append({'sender': 'User', 'message': user_input})

    # Process the question if files are uploaded
    if uploaded_files:
        send_files_and_question(uploaded_files, user_input, "You are Alex and you are one of the best Tour Guides. Answer everything while starting with your name.")
    else:
        st.session_state.chat_history.append({'sender': 'WorqHat', 'message': 'I am a financial analyst, please upload some financial data you want to talk about.'})

# Display chat history
for chat in st.session_state.chat_history:
    with st.chat_message(chat['sender']):
        st.write(chat['message'])