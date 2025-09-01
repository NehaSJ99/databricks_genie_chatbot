import streamlit as st
from genie_client import GenieConversation

st.set_page_config(page_title="Genie Chatbot", page_icon="🤖")
st.title("Genie Space Chatbot")

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
if "input_temp" not in st.session_state:
    st.session_state["input_temp"] = ""
if "genie_conversation" not in st.session_state:
    st.session_state["genie_conversation"] = GenieConversation()

user_input = st.text_input("You:", st.session_state["input_temp"], key="user_input")

if st.button("Send") and user_input:
    st.session_state["chat_history"].append({"role": "user", "content": user_input})
    reply = st.session_state["genie_conversation"].send_message(user_input)
    st.session_state["chat_history"].append({"role": "genie", "content": reply})
    st.session_state["input_temp"] = ""

for msg in st.session_state["chat_history"]:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**Genie:** {msg['content']}")
