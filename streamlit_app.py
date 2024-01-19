import streamlit as st
import time


def get_bot_response(msg):
    time.sleep(3)
    return f"You said: {msg}"


if "initialized" not in st.session_state:
    st.session_state["initialized"] = True
    st.session_state["chat_history"] = []
    st.session_state["in_progress"] = False
    st.session_state["vocabulary_topic"] = ""

st.title("Turkish Grammar Challenger")

user_message = st.chat_input(
    "Type your message here:",
    disabled=st.session_state["in_progress"],
    key="user_message_chat_input",
    on_submit=lambda: st.session_state.update({"in_progress": True}),
)

for message in st.session_state["chat_history"]:
    with st.chat_message(message["author"]):
        st.markdown(message["content"], True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("1"):
        user_option = 1
with col2:
    if st.button("2"):
        user_option = 2
with col3:
    if st.button("3"):
        user_option = 3
with col4:
    if st.button("Change topic"):
        user_option = None

if user_message:
    st.session_state["chat_history"].append({"author": "user", "content": user_message})
    with st.chat_message("user"):
        st.markdown(user_message, True)

    with st.spinner(""):
        bot_response = get_bot_response(user_message)
        st.session_state["chat_history"].append(
            {"author": "assistant", "content": bot_response}
        )
        st.session_state["in_progress"] = False
        st.rerun()
