# ---------------------- TOGETHER API KEY -------------------------- #
# 5a532872525382e32ebc396c6cc682d3b8d8d5ea428ef9468404286bb1417f2c   #
# ------------------------------------------------------------------ #

from utils import *
import streamlit as st

with st.sidebar:
    together_api_key = st.text_input("Together.ai API Key", key="chatbot_api_key", type="password")
st.title("Goopers")

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "assistant",
            "content": "Hi, I am here to help you find the best influencer for your brand. Please, provide a detailed description of your brand!",
        }
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    influencer_description = retrieve_top_k_influencers_request(prompt, k = 1)[0]
    prompt = "Explain why the provided influencer is a strong match for the following brand:\n\n" + prompt
    
    msg = together_request(user_message=prompt,
                           api_key=together_api_key,
                           request_type='retrieve_top_k_influencers',
                           influencer_description_1=influencer_description,
                           )
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)