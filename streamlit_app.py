import streamlit as st
import time
from extra_streamlit_components import CookieManager

cookie_manager = CookieManager()


def get_bot_response(query, topic):
    time.sleep(3)
    return f"Topic: {topic}, You said: {query}"


def initialize_session_state():
    if "initialized" not in st.session_state:
        st.session_state["initialized"] = True
        st.session_state["openai_api_key"] = ""
        st.session_state["vocabulary_topic"] = ""
        st.session_state["chat_history"] = []
        st.session_state["query"] = ""


def ensure_vocabulary_topic():
    if st.session_state["vocabulary_topic"] == "":
        vocabulary_topic = st.text_input("Enter a vocabulary topic:")
        if vocabulary_topic:
            st.session_state["vocabulary_topic"] = vocabulary_topic
            st.rerun()
        else:
            st.stop()


def ensure_openai_api_key():
    cookie_openai_api_key = cookie_manager.get(cookie="openai_api_key")
    if not cookie_openai_api_key:
        openai_api_key = st.text_input("Enter OpenAI API key:", type="password")
        if openai_api_key:
            cookie_manager.set("openai_api_key", openai_api_key, expires_at=None)
            time.sleep(0.1)  # Wait for saving cookie
            st.rerun()
        else:
            st.stop()
    st.session_state["openai_api_key"] = cookie_openai_api_key


def render_chat_input():
    user_message = st.chat_input(
        "Write a message...",
        disabled=bool(st.session_state["query"]),
        key="user_message_chat_input",
    )

    return user_message


def render_chat_history():
    for message in st.session_state["chat_history"]:
        with st.chat_message(message["author"]):
            st.markdown(message["content"], True)


def render_options():
    if st.session_state["query"]:
        return None

    col1, col2, col3 = st.columns(3)

    user_option = None
    with col1:
        if st.button("1"):
            user_option = 1
    with col2:
        if st.button("2"):
            user_option = 2
    with col3:
        if st.button("3"):
            user_option = 3

    return user_option


def process_user_message(user_message):
    if not user_message:
        return

    st.session_state["chat_history"].append({"author": "user", "content": user_message})
    st.session_state["query"] = user_message
    time.sleep(0.1)  # Wait for rendering
    st.rerun()


def process_query():
    if not st.session_state["query"]:
        return

    with st.spinner("Thinking..."):
        bot_response = get_bot_response(
            query=st.session_state["query"],
            topic=st.session_state["vocabulary_topic"],
        )
        st.session_state["chat_history"].append(
            {"author": "assistant", "content": bot_response}
        )
        st.session_state["query"] = ""
        st.rerun()


st.title("Turkish Grammar Challenger")

initialize_session_state()
ensure_openai_api_key()
ensure_vocabulary_topic()
render_chat_history()
user_message = render_chat_input()
user_option = render_options()
if user_option:
    user_message = str(user_option)
process_user_message(user_message)
process_query()
