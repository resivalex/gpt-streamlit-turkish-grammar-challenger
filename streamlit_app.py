import streamlit as st

# Initialize session state for chat history if not already done
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []


def send_message():
    user_message = st.session_state.user_input
    if user_message:
        st.session_state.chat_history.append(f"You: {user_message}")
        # Here we add a fake response
        st.session_state.chat_history.append("Bot: This is a fake response.")
        # Clear the input box after sending the message
        st.session_state.user_input = ""


# Title of the app
st.title("Simple Chat App")

# Text input for the user message
st.text_input("Type your message here:", key="user_input", on_change=send_message)

# Display chat history
for message in st.session_state.chat_history:
    st.text(message)
