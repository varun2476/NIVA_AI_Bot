
import streamlit as st
from google import genai
import os
import time


st.set_page_config(
    page_title="NIVA AI Chatbot",
    page_icon="🤖",
    layout="centered"
)


st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}

h1 {
    text-align: center;
    color: #4F8BF9;
}

.stChatMessage {
    border-radius: 15px;
    padding: 10px;
}

.stButton>button {
    width: 100%;
    border-radius: 12px;
    background-color: #4F8BF9;
    color: white;
    font-weight: bold;
}

.stButton>button:hover {
    background-color: #2563eb;
}

footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

API_KEY = os.getenv("GENAI_API_KEY", "YOUR_API_KEY")

client = genai.Client(api_key="AQ.Ab8RN6L2myrrmHzQvTtC7cFtL6FhJ1PaRnLvn_8z9LHpJVqC7A")


with st.sidebar:
    st.title("🤖 NIVA AI")
    st.markdown("---")

    st.markdown("### ✨ Features")
    st.write("Gemini AI")
    st.write("✅ AI Assisstant")
    st.write("✅ Gemini Models")
    st.write("✅ Fast Responses")

    st.markdown("---")

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.metric("💬 Messages", len(st.session_state.get("messages", [])))


st.markdown(
    """
    <h1>🤖 NIVA AI Chatbot</h1>
    <p style='text-align:center;color:gray;font-size:18px;'>
    Your Intelligent AI Assistant
    </p>
    """,
    unsafe_allow_html=True,
)


if "messages" not in st.session_state:
    st.session_state.messages = []


if len(st.session_state.messages) == 0:
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown("""
### 👋 Welcome!

I'm **NIVA AI**.

You can ask me about:

- 💻 Programming
- 📚 Studies
- 🤖 Artificial Intelligence
- ✍️ Writing
- 🌎 General Knowledge

Start typing below 👇
""")


for msg in st.session_state.messages:
    avatar = "👤" if msg["role"] == "user" else "🤖"

    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])


if len(st.session_state.messages) == 0:
    st.markdown("### 💡 Suggested Questions")

col1, col2 = st.columns(2)

suggested_prompt = None

with col1:
    if st.button("💻 Explain Python OOP"):
        suggested_prompt = "Explain Python OOP"

    if st.button("📝 Write a Resume"):
        suggested_prompt = "Write a professional resume."

with col2:
    if st.button("🤖 Latest AI Trends"):
        suggested_prompt = "What are the latest AI trends?"

    if st.button("🗄️ Generate SQL Query"):
        suggested_prompt = "Generate an SQL query to fetch the top 10 highest-paid employees."


if suggested_prompt:
    prompt = suggested_prompt


user_input = st.chat_input("💬 Ask me anything...")

prompt = suggested_prompt or user_input

if prompt:

    # Display user message
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    MODELS = [
         "gemini-2.5-flash",
    "gemini-1.5-pro"
    ]

    bot_reply = ""

    with st.spinner("🤖 Thinking..."):
        for model in MODELS:
            try:
                response = client.models.generate_content(
                    model=model,
                    contents=prompt
                )
                bot_reply = response.text
                break
            except Exception as e:
                print(e)
                continue

    if not bot_reply:
        bot_reply = "⚠️ Sorry! The AI is currently busy. Please try again."

    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(bot_reply)

    st.session_state.messages.append(
        {"role": "assistant", "content": bot_reply}
    )


st.markdown("---")
st.caption("🚀 Built with ❤️ using Streamlit + Google Gemini")