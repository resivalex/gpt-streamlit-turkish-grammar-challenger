import streamlit as st
import time
from extra_streamlit_components import CookieManager

from gpt_streamlit_turkish_grammar_challenger import (
    TurkishGrammarChallenger,
    TurkishGrammarTask,
)

cookie_manager = CookieManager()


INITIAL_MESSAGE = "create_first_task"


def get_bot_response(query):
    task = turkish_grammar_challenger.create_task()

    feedback = ""
    last_task: TurkishGrammarTask = st.session_state["last_task"]
    if query != INITIAL_MESSAGE and last_task:
        feedback = turkish_grammar_challenger.provide_feedback(last_task, query)

    st.session_state["last_task"] = task

    task = f"""{task["russian_translation"]}

1. {task["turkish_phrase"]}
2. {task["first_challenging_turkish_phrase"]}
3. {task["second_challenging_turkish_phrase"]}
"""

    if feedback:
        response = f"""{feedback}
        
---

{task}"""
    else:
        response = task

    return response


def initialize_session_state():
    if "initialized" not in st.session_state:
        st.session_state["initialized"] = True
        st.session_state["openai_api_key"] = ""
        st.session_state["vocabulary_topic"] = ""
        st.session_state["chat_history"] = []
        st.session_state["query"] = ""
        st.session_state["last_task"] = None


def ensure_vocabulary_topic():
    if st.session_state["vocabulary_topic"] == "":
        vocabulary_topic = st.text_input("Enter a vocabulary topic:")
        if vocabulary_topic:
            st.session_state["vocabulary_topic"] = vocabulary_topic
            st.session_state["query"] = INITIAL_MESSAGE
            time.sleep(0.1)  # Wait for rendering
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
        disabled=True,
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

    last_task: TurkishGrammarTask = st.session_state["last_task"]
    if not last_task:
        return None

    col1, col2, col3 = st.columns(3)
    selected_answer = None
    options = last_task["turkish_options"]
    with col1:
        if st.button("1", use_container_width=True):
            selected_answer = options[0]
    with col2:
        if st.button("2", use_container_width=True):
            selected_answer = options[1]
    with col3:
        if st.button("3", use_container_width=True):
            selected_answer = options[2]

    return selected_answer


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
        bot_response = get_bot_response(query=st.session_state["query"])
        st.session_state["chat_history"].append(
            {"author": "assistant", "content": bot_response}
        )
        st.session_state["query"] = ""
        st.rerun()


st.title("Turkish Grammar")

initialize_session_state()
ensure_openai_api_key()
ensure_vocabulary_topic()
turkish_grammar_challenger = TurkishGrammarChallenger(
    openai_api_key=st.session_state["openai_api_key"],
    vocabulary_topic=st.session_state["vocabulary_topic"],
)
render_chat_history()
user_message = render_chat_input()
user_answer = render_options()
if user_answer:
    user_message = user_answer
process_user_message(user_message)
process_query()
