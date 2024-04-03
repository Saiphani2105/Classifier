import streamlit as st
from configparser import ConfigParser
from classifierr import ChatBot

def main():
    # st.title('Classifier Chatbot')
    st.set_page_config(layout="wide", page_title="Classifier", page_icon="img.png")
    # Center align the title
    st.markdown("<h1 style='text-align: center;'>Classifier Chatbot</h1>", unsafe_allow_html=True)


    # Load API key from credentials.ini
    config = ConfigParser()
    config.read('credentials.ini')
    api_key = config['gemini_ai']['API_KEY']

    chatbot = ChatBot(api_key=api_key)
    chatbot.start_conversation()

    st.write("Welcome to the Classifier Chatbot. Type 'quit' to exit.")

    conversation = []  # Store user input and bot response pairs
    clear_chat = False

    user_input = st.text_input('YOU:', key='input')
    if st.button('Send'):
        if user_input.lower() == 'quit':
            st.write("Exiting ChatBot...")
            st.stop()
        elif user_input.lower() == 'clear chat':
            conversation.clear()
        else:
            conversation.append({'speaker': 'YOU', 'message': user_input})

            try:
                response = chatbot.send_prompt(user_input)
                conversation.append({'speaker': chatbot.CHATBOT_NAME, 'message': response})
            except Exception as e:
                st.error(f'ERROR: {e}')

    # Calculate the height of the text area dynamically based on the length of the conversation
    textarea_height = min(len(conversation) * 100, 500)
    st.text_area("Chat History", value='\n'.join([f"{entry['speaker']}: {entry['message']}" for entry in conversation]),height=textarea_height)

if __name__ == '__main__':
    main()
