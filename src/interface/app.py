import streamlit as st
from src.ops_generation.data_generation import generate_response
import uuid

st.set_page_config(
    page_title="SingleView AI Assistant",
    page_icon="🤖",
    layout="centered"
)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())


st.title("🤖 SingleView AI Assistant")
st.caption("Your operational documentation assistant")

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
query = st.chat_input("Ask anything about SingleView...")

if query:

    # Display user message
    st.session_state.messages.append({
        "role": "user",
        "content": query
    })

    with st.chat_message("user"):
        st.markdown(query)

    # Generate assistant response
    with st.chat_message("assistant"):
        with st.spinner("Searching SingleView documentation..."):

            answer = generate_response(
                query=query,
                thread_id=st.session_state.thread_id
            )

            st.markdown(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })
with st.sidebar:
    st.title("Settings")

    if st.button("🗑️ Clear conversation"):
        st.session_state.messages = []
        st.session_state.thread_id = str(uuid.uuid4())
        st.rerun()