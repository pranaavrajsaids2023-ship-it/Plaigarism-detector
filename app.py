import streamlit as st
import re
import math

# 1. Layout Configuration & Custom CSS Card Styling
st.set_page_config(page_title="AI Text Detector", page_icon="🔍", layout="centered")

st.markdown("""
<style>
    .main-card {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
        margin-bottom: 20px;
    }
    .verdict-box {
        padding: 15px;
        border-radius: 8px;
        color: white;
        font-weight: bold;
        text-align: center;
        font-size: 1.1rem;
        margin-top: 15px;
    }
    .ai-bg { background: linear-gradient(135deg, #ef4444, #dc2626); }
    .human-bg { background: linear-gradient(135deg, #10b981, #059669); }
</style>
""", unsafe_allow_html=True)

# 2. Header Elements
st.title("🔍 Statistical AI Text Detector")
st.write("Analyze text structure and word distribution patterns locally without heavy machine learning models.")

# 3. Input Dashboard Interface
st.markdown('<div class="main-card">', unsafe_allow_html=True)
user_input = st.text_area("Paste your paragraph below:", height=180, placeholder="Type or paste text here (minimum 2-3 sentences recommended)...", label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)

# 4. Heuristic Processing Engine
if st.button("Scan Text Structure", use_container_width=True):
    if not user_input.strip():
        st.warning("⚠️ Please enter some text to analyze.")
    else:
        # Isolate individual sentences cleanly
        sentences = [s.strip() for s in re.split(r'[.!?]+', user_input) if len(s.strip()) > 5]
        
        if not sentences:
            st.error("Please enter complete sentences for structural variance testing.")
        else:
            # Metric A: Sentence Length Standard Deviation (Pacing uniformity)
            lengths = [len(s.split()) for s in sentences]
            mean_length = sum(lengths) / len(lengths)
            variance = sum((x - mean_length) ** 2 for x in lengths) / len(lengths)
            std_dev = math.sqrt(variance)

            # Metric B: Common LLM Transition Keyword Tracker
            ai_buzzwords = ["delve", "tapestry", "furthermore", "testament", "in conclusion", "moreover", "crucial", "not only"]
            keyword_count = 0
            lower_text = user_input.lower()
            for word in ai_buzzwords:
                keyword_count += len(re.findall(r'\b' + re.escape(word) + r'\b', lower_text))

            # Metric C: Probability Compilation Matrix
            ai_points = 0
            if len(sentences) >= 2:
                if std_dev < 3.5:
                    ai_points += 45  # Extremely uniform sentences imply AI writing pacing
                elif std_dev < 6.0:
                    ai_points += 25
            
            ai_points += min(keyword_count * 20, 55)
            final_score = min(max(ai_points, 5), 95)

            # 5. Interface Output Presentation
            st.write("---")
            if final_score >= 50:
                st.markdown(f'<div class="verdict-box ai-bg">🤖 Verdict: Likely AI Generated ({final_score}%)</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="verdict-box human-bg">✍️ Verdict: Likely Human Written ({100 - final_score}%)</div>', unsafe_allow_html=True)

            # Interactive Metrics Summary
            st.write("### 📊 Text Metrics Breakdown")
            col1, col2, col3 = st.columns(3)
            col1.metric("Sentence Count", len(sentences))
            col2.metric("Pacing Style", "Uniform (AI)" if std_dev < 4 else "Varied (Human)")
            col3.metric("AI Buzzwords Found", f"{keyword_count} matches")