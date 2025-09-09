import streamlit as st
from genie_client import GenieConversation, get_generated_sql

st.set_page_config(page_title="Genie Chatbot")
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
    # Show generated SQL after getting a reply
    conversation_id = st.session_state["genie_conversation"].conversation_id
    message_id = st.session_state["genie_conversation"].last_message_id
    sql = get_generated_sql(conversation_id, message_id)
    if sql:
        st.markdown("**Generated SQL:**")
        st.code(sql, language="sql")

for msg in st.session_state["chat_history"]:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**Genie:** {msg['content']}")
