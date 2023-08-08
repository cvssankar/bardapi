import os
import streamlit as st
from streamlit_chat import message
from bardapi import Bard

# Set your API key as an environment variable
os.environ["_BARD_API_KEY"] = "ZghV7Rca_o2IZf9JY1EWmNcXnY3VGRzHp-tKAQ7Ct_mVcqYxFbPR3ddvfEkhdapPMnm6fw."

name = "main"

class ChatApp:
    def __init__(self):
        self.api = Bard()
        self.past_message = None
        self.generate = []
        st.session_state["past"] = []
        st.session_state["generate"] = []

    def get_response(self, prompt, is_question=False):
        try:
            response = self.api.get_answer(prompt)["content"]
        except KeyError:
            response = "Sorry, I didn't understand your prompt."

        return response

    def detect_emotion(self, text):
        from textblob import TextBlob

        analysis = TextBlob(text)
        emotion = analysis.sentiment.polarity

        if emotion > 0.5:
            return "positive"
        elif emotion < -0.5:
            return "negative"
        else:
            return "neutral"

    def user_input(self):
        # Use st.text_area instead of st.text_input for multi-line text input
        input_text = st.text_area("Enter Your Prompt:", height=200)
        if not input_text:
            return None

        # Store the previous message in memory
        self.past_message = input_text

        return input_text

    def run(self):
        user_text = self.user_input()

        if user_text:
            # Use st.spinner to show a loading indicator
            with st.spinner("SportsEdgePro is typing..."):
                output = self.get_response(user_text, self.detect_emotion(user_text))

            # Update the session state with the new message and response
            update_session_state(user_text, output)

            if st.session_state["generate"]:
                with st.container():
                    for i in range(len(st.session_state["generate"]) - 1, -1, -1):

                        # Use st.markdown instead of st.header for each message
                        # Add emojis or icons to indicate the sender of each message
                        st.markdown(f"### Message {i} {'' if i % 2 == 0 else ''}")
                        message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")
                        message(st.session_state["generate"][i], key=str(i))

    def on_button_clicked(self):
        # Clear the session state
        st.session_state["past"] = []
        st.session_state["generate"] = []

def update_session_state(user_text, output):
    st.session_state["past"].append(user_text)
    st.session_state["generate"].append(output)

def main():

    # Use st.title instead of st.header for the title of the app
    st.title("Enhanced Chat Application with Google Bard API - Bala Ganesh")

    # Use st.sidebar to display some settings or options for the chat app
    st.sidebar.title("Settings")
    tone = st.sidebar.selectbox("Tone of reply", ["Professional", "Humorous", "Conversational", "Casual", "Witty", "Sarcastic", "Excited", "Bold", "Dramatic", "Factual", "Informative", "Explanatory", "Masculine", "Feminine"])
    voice = st.sidebar.selectbox("Voice of playback", ["Male", "Female"])
    export = st.sidebar.button("Export chat")

    chat_app = ChatApp()
    chat_app.run()

if __name__ == "__main__":
    main()