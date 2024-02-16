import streamlit as st
import time
import datetime
from extra_streamlit_components import CookieManager

from gpt_streamlit_turkish_grammar_challenger import (
    TurkishGrammarChallenger,
    TurkishGrammarTask,
)


st.set_page_config(
    page_title="Турецкая грамматика",
    page_icon="./icon.png",
)


cookie_manager = CookieManager()


CREATE_TASK_TRIGGER = "create_first_task"
PREPARE_FEEDBACK_TRIGGER = "prepare_feedback"


def create_task():
    task = st.session_state["turkish_grammar_challenger"].create_task()
    st.session_state["last_task"] = task

    task = f"""{task["russian_translation"]}

1. {task["turkish_options"][0]}
2. {task["turkish_options"][1]}
3. {task["turkish_options"][2]}
"""

    return task


def prepare_feedback():
    last_task: TurkishGrammarTask = st.session_state["last_task"]
    feedback = st.session_state["turkish_grammar_challenger"].provide_feedback(
        task=last_task,
        user_answer=st.session_state["last_answer"],
    )

    return feedback


def initialize_session_state():
    if "initialized" not in st.session_state:
        st.session_state["initialized"] = True
        st.session_state["openai_api_key"] = ""
        st.session_state["vocabulary_topic"] = ""
        st.session_state["turkish_grammar_challenger"] = None
        st.session_state["chat_history"] = []
        st.session_state["query"] = ""
        st.session_state["last_task"] = None
        st.session_state["last_answer"] = None


def ensure_vocabulary_topic():
    if st.session_state["vocabulary_topic"] == "":
        vocabulary_topic = st.chat_input(
            "Введите тему составления фраз",
            key="vocabulary_topic_chat_input",
        )
        if vocabulary_topic:
            st.session_state["vocabulary_topic"] = vocabulary_topic
            st.session_state["query"] = CREATE_TASK_TRIGGER
            time.sleep(0.1)  # Wait for rendering
            st.rerun()
        else:
            st.stop()


def ensure_openai_api_key():
    cookie_openai_api_key = cookie_manager.get(cookie="openai_api_key")
    if not cookie_openai_api_key:
        openai_api_key = st.text_input("Enter OpenAI API key:", type="password")
        if openai_api_key:
            cookie_manager.set(
                "openai_api_key",
                openai_api_key,
                expires_at=datetime.datetime.now() + datetime.timedelta(days=365),
            )
            time.sleep(0.1)  # Wait for saving cookie
            st.rerun()
        else:
            st.stop()
    st.session_state["openai_api_key"] = cookie_openai_api_key


def render_disabled_chat_input():
    st.chat_input(
        "",
        disabled=True,
        key="user_message_chat_input",
    )


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
        if st.button("1", use_container_width=True, key="turkish_option_1"):
            selected_answer = options[0]
    with col2:
        if st.button("2", use_container_width=True, key="turkish_option_2"):
            selected_answer = options[1]
    with col3:
        if st.button("3", use_container_width=True, key="turkish_option_3"):
            selected_answer = options[2]

    return selected_answer


def process_user_message(user_message):
    if not user_message:
        return

    st.session_state["chat_history"].append({"author": "user", "content": user_message})
    st.session_state["query"] = PREPARE_FEEDBACK_TRIGGER
    st.session_state["last_answer"] = user_message
    time.sleep(0.1)  # Wait for rendering
    st.rerun()


def process_query():
    if not st.session_state["query"]:
        return

    query = st.session_state["query"]
    if query == CREATE_TASK_TRIGGER:
        with st.spinner("Подготовка задания..."):
            bot_response = create_task()
            st.session_state["chat_history"].append(
                {"author": "assistant", "content": bot_response}
            )
            st.session_state["query"] = ""
            st.rerun()
    if query == PREPARE_FEEDBACK_TRIGGER:
        with st.spinner("Проверка ответа..."):
            bot_response = prepare_feedback()
            st.session_state["chat_history"].append(
                {"author": "assistant", "content": bot_response}
            )
            st.session_state["query"] = CREATE_TASK_TRIGGER
            st.rerun()


st.title("Турецкая грамматика")

initialize_session_state()
ensure_openai_api_key()
ensure_vocabulary_topic()
if not st.session_state["turkish_grammar_challenger"]:
    st.session_state["turkish_grammar_challenger"] = TurkishGrammarChallenger(
        openai_api_key=st.session_state["openai_api_key"],
        vocabulary_topic=st.session_state["vocabulary_topic"],
    )
render_chat_history()
render_disabled_chat_input()
user_answer = render_options()
process_user_message(user_answer)
process_query()
