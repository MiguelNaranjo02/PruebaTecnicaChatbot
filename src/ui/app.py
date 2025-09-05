import streamlit as st
import requests
import uuid

st.set_page_config(page_title="Chatbot Browser Travel Solution", page_icon="💬")

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "history" not in st.session_state:
    st.session_state.history = []

st.title("💬 Chatbot Browser Travel Solution")
st.caption("Prueba Tecnica Browser Travel Solution")

# URL fija del backend (sin campo de texto)
api_url = "http://127.0.0.1:8000/chat"

chat_container = st.container()
with chat_container:
    for msg in st.session_state.history:
        if msg["role"] == "user":
            with st.chat_message("user"):
                st.write(msg["text"])
        else:
            with st.chat_message("assistant"):
                st.write(msg["text"])

prompt = st.chat_input("Escribe tu mensaje...")
if prompt:
    st.session_state.history.append({"role": "user", "text": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    try:
        r = requests.post(api_url, json={"session_id": st.session_state.session_id, "text": prompt})
        r.raise_for_status()
        data = r.json()
        reply = data["reply"]
        st.session_state.history.append({"role": "assistant", "text": reply})
        with st.chat_message("assistant"):
            st.write(reply)
        if data.get("handoff"):
            st.info("🔔 Se sugiere derivar a un agente humano.")
    except Exception as e:
        st.error(f"Error llamando al backend: {e}")

col1, col2 = st.columns(2)
if col1.button("Reiniciar conversación"):
    st.session_state.history = []
    st.rerun()
if col2.button("Ver historial"):
    st.code(str(st.session_state.history), language="json")
