import streamlit as st
from gooper import GooperModel


gooper = GooperModel()
CURRENT_VERSION = gooper.version

st.set_page_config(
    page_title=f"Gooper v{CURRENT_VERSION}",
    page_icon="🤖",
    menu_items={
        'Get Help': 'https://www.linkedin.com/in/giacomo-ciro/',
        'Report a bug': "https://www.linkedin.com/in/giacomo-ciro/",
        'About': "Find the best influencers for your brand by naturally talking with Gooper V1"
    }
)

st.title(f"Gooper v{CURRENT_VERSION}")
st.write(f"*No. of Influencers in current database:* `{gooper.get_influencer_count():,}`")

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
    
    msg = gooper.generate(userPrompt)
    
    # Save response
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)