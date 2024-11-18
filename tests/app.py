from together_request import together_request
import streamlit as st

with st.sidebar:
    together_api_key = st.text_input("Together.ai API Key", key="chatbot_api_key", type="password")
st.title("Goopers")

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "assistant",
            "content": "Hi, I am here to help you summarize influencer profiles. Provide a description!",
        }
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    # if not together_api_key:
    #     together_api_key = "5a532872525382e32ebc396c6cc682d3b8d8d5ea428ef9468404286bb1417f2c"
    #     # st.info("Please add your Together.ai API key to continue.")
    #     # st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    msg = together_request(prompt, together_api_key)
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)