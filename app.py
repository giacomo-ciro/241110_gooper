from utils import *
import streamlit as st

TOGETHER_API_KEY = "5a532872525382e32ebc396c6cc682d3b8d8d5ea428ef9468404286bb1417f2c"
client = Together(api_key = TOGETHER_API_KEY)

st.title("Gooper V1")
# st.write("*Disclaimer:* We currently have only 2 influencers in the database, one is a fitness influencer and the other is a mountain trekking influencer.")

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "assistant",
            "content": "Hi, I am here to help you find the best influencer for your brand. To begin, tell me something about your brand!",
        }
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if userPrompt := st.chat_input():
    
    # Save input
    st.session_state.messages.append({"role": "user", "content": userPrompt})
    st.chat_message("user").write(userPrompt)
    
    # Generate response
    msg = generate(client=client,
                   TASK_TYPE="rag",
                   userPrompt=userPrompt
                   )
    
    # Save response
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)