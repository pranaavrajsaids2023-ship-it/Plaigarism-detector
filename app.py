import streamlit as st
import requests

# 1. Simple Custom CSS styling
st.markdown("""
<style>
    .reportview-container { background: #f5f7f8; }
    .verdict-box {
        padding: 15px;
        border-radius: 8px;
        color: white;
        font-weight: bold;
        margin-top: 15px;
        text-align: center;
    }
    .ai-bg { background-color: #e53e3e; }
    .human-bg { background-color: #38a169; }
</style>
""", unsafe_allow_html=True)

# 2. Simple Web Title Layout
st.markdown("<h2>🔍 Simple AI Text Checker</h2>", unsafe_allow_html=True)
st.write("Enter text below to check if it matches AI or Human writing structures.")

# 3. User Text Box Input
user_input = st.text_area("Your Paragraph:", height=150, placeholder="Paste text here...")

# 4. Processing Button
if st.button("Analyze Content", use_container_width=True):
    if not user_input.strip():
        st.warning("Please type or paste some text first.")
    else:
        with st.spinner("Checking..."):
            try:
                # Calls a free cloud API to avoid downloading large models locally
                url = "https://api-inference.huggingface.co/models/roberta-base-openai-detector"
                response = requests.post(url, json={"inputs": user_input}).json()
                
                # Extract the highest probability result
                prediction = max(response[0], key=lambda x: x['score'])
                is_ai = prediction['label'] == "Fake"
                confidence = prediction['score'] * 100
                
                # 5. Output results using simple HTML/CSS styles
                if is_ai:
                    st.markdown(f'<div class="verdict-box ai-bg">🤖 Verdict: AI Generated ({confidence:.1f}%)</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="verdict-box human-bg">✍️ Verdict: Human Written ({confidence:.1f}%)</div>', unsafe_allow_html=True)
                    
            except Exception:
                st.error("Engine busy. Please try clicking the button again in a moment!")