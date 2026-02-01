import streamlit as st
import requests

API_URL = "http://localhost:8000"

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Agentic RAG Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "document_uploaded" not in st.session_state:
    st.session_state.document_uploaded = False

if "uploaded_filename" not in st.session_state:
    st.session_state.uploaded_filename = None

# --------------------------------------------------
# SIDEBAR – FILE UPLOAD
# --------------------------------------------------
with st.sidebar:
    st.title("📁 Knowledge Base")

    uploaded_file = st.file_uploader(
        "Upload a document",
        type=["pdf", "txt", "docx", "pptx", "md", "csv", "xlsx", "xls"],
    )

    if uploaded_file is not None:
        with st.spinner("Ingesting document..."):
            try:
                resp = requests.post(
                    f"{API_URL}/ingest",
                    files={"file": (uploaded_file.name, uploaded_file.getvalue())},
                    timeout=30
                )

                if resp.status_code == 200:
                    st.success("✅ Document ingested successfully")
                    st.session_state.document_uploaded = True
                    st.session_state.uploaded_filename = uploaded_file.name
                else:
                    st.error("❌ Failed to ingest document")

            except Exception:
                st.error("❌ Backend not reachable")

    if st.session_state.document_uploaded:
        st.divider()
        st.markdown("**Uploaded Document:**")
        st.markdown(f"📄 `{st.session_state.uploaded_filename}`")

    st.divider()

    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []
        st.experimental_rerun()

# --------------------------------------------------
# MAIN CHAT UI
# --------------------------------------------------
st.title("🤖 Agentic RAG Chatbot")
st.caption("Chat with your documents using an agent-powered RAG system")

# Render chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --------------------------------------------------
# CHAT INPUT
# --------------------------------------------------
if not st.session_state.document_uploaded:
    st.info("⬅️ Upload a document to start chatting")
    st.chat_input("Upload a document first", disabled=True)
else:
    user_input = st.chat_input("Ask something about your document...")

    if user_input:
        # User message
        st.session_state.messages.append(
            {"role": "user", "content": user_input}
        )

        with st.chat_message("user"):
            st.markdown(user_input)

        # Assistant message
        with st.chat_message("assistant"):
            with st.spinner("Agent is thinking..."):
                try:
                    resp = requests.post(
                        f"{API_URL}/query",
                        json={"question": user_input},
                        timeout=60
                    )

                    if resp.status_code == 200:
                        answer = resp.json().get("answer", "No answer found.")
                    else:
                        answer = "Something went wrong. Please try again."

                except Exception:
                    answer = "Backend not reachable."

                st.markdown(answer)

        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )

# --------------------------------------------------
# DOWNLOAD CHAT HISTORY
# --------------------------------------------------
if st.session_state.messages:
    chat_text = "\n\n".join(
        f"{m['role'].upper()}: {m['content']}"
        for m in st.session_state.messages
    )

    st.download_button(
        "⬇️ Download Chat History",
        chat_text,
        file_name="agentic_rag_chat.txt"
    )
