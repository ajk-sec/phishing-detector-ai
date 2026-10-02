# ============================================================
# PHISHING EMAIL DETECTOR — Professional Cyber Dashboard
# Screenshot-optimized version
# ============================================================

import streamlit as st
import pickle
import re
import time
import random
from pathlib import Path

# ------------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------------
st.set_page_config(
    page_title="Phishing Email Detector | CyberSec",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------------------------------------
# CUSTOM CSS — Dark Cyber Theme (Bigger + Tighter)
# ------------------------------------------------------------
st.markdown("""
<style>
    /* ---- Global ---- */
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0d1220 100%);
    }
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background-image: 
            linear-gradient(rgba(0, 217, 255, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 217, 255, 0.03) 1px, transparent 1px);
        background-size: 40px 40px;
        pointer-events: none;
        z-index: 0;
    }
    html, body, [class*="css"] {
        color: #e0e6f0;
        font-family: 'Inter', -apple-system, sans-serif;
        font-size: 16px;
    }
    
    /* ---- Reduce main container padding ---- */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 1rem !important;
        max-width: 1400px !important;
    }
    
    /* ---- Headings ---- */
    h1, h2, h3 {
        color: #00d9ff !important;
        text-shadow: 0 0 20px rgba(0, 217, 255, 0.3);
    }
    
    .hero-title {
        font-size: 3.5rem !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #00d9ff 0%, #7b5cff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: none !important;
        margin-bottom: 0.4rem !important;
        animation: fadeIn 0.8s ease-in;
        line-height: 1.1 !important;
    }
    .hero-subtitle {
        color: #8b9bb4 !important;
        font-size: 1.25rem;
        margin-bottom: 1.5rem;
        animation: fadeIn 1s ease-in;
    }
    
    /* ---- Badges (BIGGER) ---- */
    .badge {
        display: inline-block;
        padding: 0.6rem 1.2rem;
        margin: 0.3rem 0.5rem 0.3rem 0;
        border-radius: 24px;
        font-size: 1rem;
        font-weight: 600;
        animation: fadeIn 1.2s ease-in;
    }
    .badge-accuracy {
        background: rgba(0, 255, 136, 0.15);
        color: #00ff88;
        border: 1px solid rgba(0, 255, 136, 0.3);
    }
    .badge-model {
        background: rgba(0, 217, 255, 0.15);
        color: #00d9ff;
        border: 1px solid rgba(0, 217, 255, 0.3);
    }
    .badge-data {
        background: rgba(123, 92, 255, 0.15);
        color: #b8a5ff;
        border: 1px solid rgba(123, 92, 255, 0.3);
    }
    
    /* ---- Text area ---- */
    .stTextArea textarea {
        background-color: rgba(26, 31, 58, 0.7) !important;
        border: 1px solid rgba(0, 217, 255, 0.2) !important;
        color: #e0e6f0 !important;
        border-radius: 12px !important;
        font-size: 1rem !important;
        padding: 1rem !important;
        transition: all 0.3s ease !important;
    }
    .stTextArea textarea:focus {
        border-color: #00d9ff !important;
        box-shadow: 0 0 20px rgba(0, 217, 255, 0.2) !important;
    }
    
    /* ---- Buttons ---- */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #00d9ff 0%, #7b5cff 100%) !important;
        color: #0a0e27 !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.9rem 2rem !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 20px rgba(0, 217, 255, 0.3) !important;
    }
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 30px rgba(0, 217, 255, 0.5) !important;
    }
    .stButton > button[kind="secondary"] {
        background: rgba(255, 255, 255, 0.05) !important;
        color: #8b9bb4 !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        padding: 0.9rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button[kind="secondary"]:hover {
        background: rgba(255, 45, 85, 0.15) !important;
        color: #ff6b8a !important;
        border-color: rgba(255, 45, 85, 0.4) !important;
    }
    
    /* ---- Sidebar demo buttons ---- */
    [data-testid="stSidebar"] .stButton > button {
        background: linear-gradient(135deg, rgba(0, 217, 255, 0.15) 0%, rgba(123, 92, 255, 0.15) 100%) !important;
        color: #00d9ff !important;
        border: 1px solid rgba(0, 217, 255, 0.3) !important;
        border-radius: 10px !important;
        padding: 0.7rem 1rem !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        text-align: left !important;
        transition: all 0.25s ease !important;
        margin-bottom: 0.4rem !important;
    }
    [data-testid="stSidebar"] .stButton > button:hover {
        background: linear-gradient(135deg, rgba(0, 217, 255, 0.3) 0%, rgba(123, 92, 255, 0.3) 100%) !important;
        border-color: #00d9ff !important;
        color: #ffffff !important;
        transform: translateX(4px) !important;
        box-shadow: 0 4px 15px rgba(0, 217, 255, 0.3) !important;
    }
    
    /* ---- Result cards ---- */
    .result-card {
        padding: 2.5rem 2rem;
        border-radius: 16px;
        text-align: center;
        animation: slideIn 0.5s ease-out;
        margin-top: 1rem;
    }
    .result-phishing {
        background: linear-gradient(135deg, rgba(255, 45, 85, 0.15) 0%, rgba(255, 45, 85, 0.05) 100%);
        border: 2px solid rgba(255, 45, 85, 0.4);
        box-shadow: 0 0 40px rgba(255, 45, 85, 0.2);
    }
    .result-safe {
        background: linear-gradient(135deg, rgba(0, 255, 136, 0.15) 0%, rgba(0, 255, 136, 0.05) 100%);
        border: 2px solid rgba(0, 255, 136, 0.4);
        box-shadow: 0 0 40px rgba(0, 255, 136, 0.2);
    }
    .result-icon {
        font-size: 4.5rem;
        margin-bottom: 1rem;
        display: block;
        line-height: 1;
    }
    .result-title {
        font-size: 2rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
    .result-title-phishing { color: #ff2d55; }
    .result-title-safe { color: #00ff88; }
    .result-confidence {
        font-size: 3rem;
        font-weight: 800;
        margin: 1rem 0;
        color: #e0e6f0;
    }
    .result-message {
        font-size: 1.05rem;
        margin-top: 1rem;
        font-weight: 500;
    }
    .confidence-bar {
        width: 100%;
        height: 14px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 7px;
        overflow: hidden;
        margin: 1rem 0;
    }
    .confidence-fill {
        height: 100%;
        border-radius: 7px;
        animation: fillBar 1s ease-out;
    }
    .confidence-fill-phishing {
        background: linear-gradient(90deg, #ff2d55 0%, #ff6b8a 100%);
    }
    .confidence-fill-safe {
        background: linear-gradient(90deg, #00ff88 0%, #00d9ff 100%);
    }
    
    /* ---- Sidebar ---- */
    [data-testid="stSidebar"] {
        background: rgba(10, 14, 39, 0.95);
        border-right: 1px solid rgba(0, 217, 255, 0.15);
    }
    [data-testid="stSidebar"] .block-container {
        padding-top: 1.5rem !important;
    }
    
    /* ---- Info / hint boxes ---- */
    .info-box {
        padding: 1.2rem;
        background: rgba(26, 31, 58, 0.6);
        border-left: 4px solid #00d9ff;
        border-radius: 8px;
        margin-bottom: 1rem;
        font-size: 1.05rem;
    }
    .hint-box {
        padding: 1rem 1.2rem;
        background: rgba(0, 217, 255, 0.08);
        border-left: 4px solid #00d9ff;
        border-radius: 8px;
        margin-bottom: 1rem;
        color: #a5c8e0;
        font-size: 1rem;
    }
    .demo-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        background: rgba(255, 193, 7, 0.15);
        border: 1px solid rgba(255, 193, 7, 0.3);
        border-radius: 8px;
        color: #ffc107;
        font-size: 0.95rem;
        font-weight: 600;
        margin-bottom: 0.8rem;
    }
    
    /* ---- Model badge ---- */
    .model-badge {
        background: linear-gradient(135deg, rgba(0, 217, 255, 0.1) 0%, rgba(123, 92, 255, 0.1) 100%);
        border: 1px solid rgba(0, 217, 255, 0.25);
        border-radius: 12px;
        padding: 1.2rem 1rem;
        margin-bottom: 1rem;
        text-align: center;
    }
    .model-badge .accuracy {
        font-size: 2.2rem;
        font-weight: 800;
        color: #00ff88;
        margin: 0;
        line-height: 1.1;
    }
    .model-badge .label {
        font-size: 0.8rem;
        color: #8b9bb4;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.3rem;
    }
    .model-badge .algorithm {
        font-size: 0.95rem;
        color: #00d9ff;
        margin-top: 0.5rem;
        margin-bottom: 0;
    }
    
    /* ---- Streamlit expander in sidebar ---- */
    [data-testid="stSidebar"] [data-testid="stExpander"] {
        background: rgba(26, 31, 58, 0.5);
        border: 1px solid rgba(0, 217, 255, 0.15);
        border-radius: 10px;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes slideIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes fillBar {
        from { width: 0%; }
    }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# Load model
# ------------------------------------------------------------
@st.cache_resource
def load_model():
    model_path = Path(__file__).parent.parent / "data" / "phishing_model_max.pkl"
    if not model_path.exists():
        return None, None, None
    with open(model_path, "rb") as f:
        bundle = pickle.load(f)
    return bundle["model"], bundle["vectorizer"], bundle.get("accuracy", 0.9897)

# ------------------------------------------------------------
# Text cleaning
# ------------------------------------------------------------
def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'http\S+|www\.\S+', ' urltoken ', text)
    text = re.sub(r'\S+@\S+', ' emailtoken ', text)
    text = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', ' phonetoken ', text)
    text = re.sub(r'\b\d{4,}\b', ' numbertoken ', text)
    text = re.sub(r'[^a-z\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# ------------------------------------------------------------
# Load
# ------------------------------------------------------------
model, vectorizer, model_accuracy = load_model()

# ------------------------------------------------------------
# Example emails
# ------------------------------------------------------------
examples = {
    "phish1": """Dear Team,

I need you to process an urgent wire transfer immediately. This is part of a confidential acquisition we've been working on. Please do not discuss this with anyone else on the team.

I'm currently in meetings and can't take calls. Reply to confirm you've received this.

- CEO""",
    "phish2": """URGENT: Your password has expired!

Click here to reset it immediately or your account will be locked: http://secure-reset-link.com/verify

This action is required within 24 hours.

IT Security Team""",
    "phish3": """Congratulations! You've been selected as our lucky winner for a $1,000 Amazon gift card.

Claim your prize now by clicking this link: http://amazon-rewards-claim.com/winner

Hurry, this offer expires in 24 hours!

- Amazon Rewards Team""",
    "safe1": """Hey,

Are we still meeting for coffee tomorrow at 3pm? Let me know if that time works for you.

Thanks!""",
    "safe2": """Hi,

Please find the Q3 report attached. Let me know your thoughts when you get a chance.

Best regards,
Sarah""",
    "safe3": """Team,

Reminder: The quarterly review meeting is on Friday at 2 PM in the main conference room. Please bring your updated project status reports.

Thanks,
Management"""
}

# ------------------------------------------------------------
# SIDEBAR
# ------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🛡️ Cyber Security Toolkit")
    st.markdown("---")
    
    st.markdown(f"""
    <div class="model-badge">
        <p class="label">🎯 Model Accuracy</p>
        <p class="accuracy">{model_accuracy * 100:.2f}%</p>
        <p class="algorithm">🤖 Linear SVM</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("📊 Model Details"):
        st.markdown("""
        **Algorithm:** Linear SVM  
        **Training emails:** `82,486`  
        **Features:** `20,000 TF-IDF`  
        **Vectorizer:** TF-IDF (1-3 grams)  
        **Text cleaning:** Custom regex pipeline
        """)
    
    st.markdown("---")
    st.markdown("#### 🎯 Sample Emails")
    st.caption("Optional — click any to test:")
    
    st.markdown("**🚨 Phishing Samples:**")
    ex_phish1 = st.button("▶ CEO Fraud Attack", use_container_width=True)
    ex_phish2 = st.button("▶ Password Reset Scam", use_container_width=True)
    ex_phish3 = st.button("▶ Prize Winner Scam", use_container_width=True)
    
    st.markdown("**✅ Safe Samples:**")
    ex_safe1 = st.button("▶ Meeting Reminder", use_container_width=True)
    ex_safe2 = st.button("▶ Report Follow-up", use_container_width=True)
    ex_safe3 = st.button("▶ Team Meeting Note", use_container_width=True)
    
    st.markdown("---")
    random_btn = st.button("🎲 Load Random Sample", use_container_width=True)
    
    st.markdown("---")
    st.markdown("#### 🔗 Links")
    st.markdown("[📁 GitHub Repo](https://github.com/ajk-sec/phishing-detector-ai)")

# ------------------------------------------------------------
# SESSION STATE
# ------------------------------------------------------------
if "email_input" not in st.session_state:
    st.session_state.email_input = ""
if "demo_loaded" not in st.session_state:
    st.session_state.demo_loaded = False
if "clear_triggered" not in st.session_state:
    st.session_state.clear_triggered = False

if st.session_state.clear_triggered:
    st.session_state.email_input = ""
    st.session_state.demo_loaded = False
    st.session_state.clear_triggered = False

if ex_phish1:
    st.session_state.email_input = examples["phish1"]
    st.session_state.demo_loaded = True
elif ex_phish2:
    st.session_state.email_input = examples["phish2"]
    st.session_state.demo_loaded = True
elif ex_phish3:
    st.session_state.email_input = examples["phish3"]
    st.session_state.demo_loaded = True
elif ex_safe1:
    st.session_state.email_input = examples["safe1"]
    st.session_state.demo_loaded = True
elif ex_safe2:
    st.session_state.email_input = examples["safe2"]
    st.session_state.demo_loaded = True
elif ex_safe3:
    st.session_state.email_input = examples["safe3"]
    st.session_state.demo_loaded = True
elif random_btn:
    random_key = random.choice(list(examples.keys()))
    st.session_state.email_input = examples[random_key]
    st.session_state.demo_loaded = True

# ------------------------------------------------------------
# HERO
# ------------------------------------------------------------
st.markdown('<h1 class="hero-title">🛡️ Phishing Email Detector</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="hero-subtitle">Paste <strong>any</strong> email. The AI will tell you if it\'s a phishing attempt or a safe message.</p>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f'<span class="badge badge-accuracy">🎯 {model_accuracy * 100:.2f}% Accuracy</span>', unsafe_allow_html=True)
with col2:
    st.markdown('<span class="badge badge-model">🤖 Linear SVM</span>', unsafe_allow_html=True)
with col3:
    st.markdown('<span class="badge badge-data">📚 82,486 Emails</span>', unsafe_allow_html=True)
with col4:
    st.markdown('<span class="badge badge-accuracy">⚡ Real-Time</span>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

if model is None:
    st.error("⚠️ **Model not found!** Run `python src/detector_kaggle.py` to train the model.")
    st.stop()

# ------------------------------------------------------------
# Two-column layout
# ------------------------------------------------------------
col_input, col_result = st.columns([1, 1], gap="medium")

with col_input:
    st.markdown("### 📧 Paste Your Email")
    
    if st.session_state.demo_loaded:
        st.markdown(
            '<div class="demo-badge">📝 Demo email loaded — click Clear or start typing to use your own</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown("""
        <div class="hint-box">
            💡 <strong>Don't know if an email is safe?</strong><br>
            That's what this tool tells you. Just paste the email below.
        </div>
        """, unsafe_allow_html=True)
    
    email_text = st.text_area(
        "Email content",
        value=st.session_state.email_input,
        height=240,
        placeholder="Paste any email here — from your inbox, a suspicious message, or anything you want to check.\n\nYou don't need to know if it's phishing — the AI will tell you.",
        label_visibility="collapsed",
        key="email_area"
    )
    
    if st.session_state.demo_loaded and email_text != st.session_state.email_input:
        if email_text.strip() and not any(email_text.strip() == ex.strip() for ex in examples.values()):
            st.session_state.demo_loaded = False
            st.session_state.email_input = email_text
    
    btn_col1, btn_col2 = st.columns([3, 1])
    with btn_col1:
        analyze = st.button("🔍 Analyze Email", use_container_width=True, type="primary")
    with btn_col2:
        if st.button("✖ Clear", use_container_width=True, type="secondary"):
            st.session_state.clear_triggered = True
            st.rerun()

with col_result:
    st.markdown("### 🎯 Analysis Result")
    
    if analyze and email_text.strip():
        with st.spinner("Analyzing..."):
            time.sleep(0.4)
            cleaned = clean_text(email_text)
            features = vectorizer.transform([cleaned])
            prediction = model.predict(features)[0]
            probability = model.predict_proba(features)[0]
            confidence = max(probability) * 100
            
            if prediction == 1:
                st.markdown(f"""
                <div class="result-card result-phishing">
                    <span class="result-icon">🚨</span>
                    <div class="result-title result-title-phishing">PHISHING DETECTED</div>
                    <div class="result-confidence">{confidence:.1f}%</div>
                    <div class="confidence-bar">
                        <div class="confidence-fill confidence-fill-phishing" style="width: {confidence}%;"></div>
                    </div>
                    <p class="result-message" style="color: #ff8ca6;">
                        ⚠️ This email shows strong phishing indicators.<br>
                        Do not click links or share credentials.
                    </p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="result-card result-safe">
                    <span class="result-icon">✅</span>
                    <div class="result-title result-title-safe">EMAIL APPEARS SAFE</div>
                    <div class="result-confidence">{confidence:.1f}%</div>
                    <div class="confidence-bar">
                        <div class="confidence-fill confidence-fill-safe" style="width: {confidence}%;"></div>
                    </div>
                    <p class="result-message" style="color: #8effb7;">
                        ✅ No obvious phishing indicators detected.<br>
                        Stay vigilant — always verify unexpected requests.
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            with st.expander("🔬 Technical Details"):
                st.markdown(f"""
                - **Raw prediction:** `{prediction}` (1 = phishing, 0 = safe)
                - **Phishing probability:** `{probability[1] * 100:.2f}%`
                - **Safe probability:** `{probability[0] * 100:.2f}%`
                - **Cleaned text length:** `{len(cleaned)}` characters
                """)
    
    elif analyze:
        st.warning("⚠️ Please paste some email text first.")
    else:
        st.markdown("""
        <div class="info-box">
            <p style="margin: 0; color: #a5c8e0;">
                👈 <strong>Ready to check an email?</strong><br><br>
                1. Paste any email into the box on the left<br>
                2. Click <strong>🔍 Analyze Email</strong><br>
                3. The result will appear here<br><br>
                <em style="color: #8b9bb4; font-size: 0.9rem;">
                Don't have an email handy? Try the samples in the sidebar.
                </em>
            </p>
        </div>
        """, unsafe_allow_html=True)

# ------------------------------------------------------------
# FOOTER
# ------------------------------------------------------------
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.caption("⚠️ **Educational use only**")
with col2:
    st.caption("🛡️ **Defensive security research**")
with col3:
    st.caption("🔗 [github.com/ajk-sec](https://github.com/ajk-sec/phishing-detector-ai)")