import streamlit as st
import time


def get_bot_response(msg):
    time.sleep(3)
    return f"You said: {msg}"


if "initialized" not in st.session_state:
    st.session_state["initialized"] = True
    st.session_state["chat_history"] = []
    st.session_state["in_progress"] = False


st.title("Turkish Grammar Challenger")

user_message = st.chat_input(
    "Type your message here:",
    disabled=st.session_state["in_progress"],
    key="user_message",
    on_submit=lambda: st.session_state.update({"in_progress": True}),
)

for message in st.session_state["chat_history"]:
    with st.chat_message(message["author"]):
        st.markdown(message["content"], True)

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
