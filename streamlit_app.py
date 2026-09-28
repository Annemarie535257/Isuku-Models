import streamlit as st

from streamlit_utils import display_category, save_complaint, save_uploads


st.set_page_config(
    page_title="Isuku | Report a Complaint",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@700;800&display=swap');
    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
    [data-testid="stAppViewContainer"] { background: radial-gradient(circle at 84% 12%, #edf8f0 0, transparent 28%), #f7faf8; }
    [data-testid="stSidebar"] { background: linear-gradient(165deg, #073b2d, #082c28); }
    [data-testid="stSidebar"] * { color: #eef8f1; }
    .brand { padding: 10px 3px 24px; border-bottom: 1px solid #ffffff20; color: #fff; }
    .brand b { display: block; font: 800 25px/1 Manrope, sans-serif; letter-spacing: -1px; }
    .brand span { color: #a7d8bd; font-size: 10px; }
    .sidebar-caption { color: #8bc5a4; font-size: 10px; letter-spacing: 1.5px; font-weight: 700; margin: 25px 0 8px; }
    h1, h2, h3 { color: #102b31; font-family: Manrope, sans-serif; }
    h1 { font-size: 2rem !important; letter-spacing: -1px; }
    .intro { color: #627681; font-size: 15px; line-height: 1.5; margin-bottom: 20px; }
    .section-card { background: rgba(255,255,255,.9); border: 1px solid #e3ece8; border-radius: 12px; padding: 20px; margin-bottom: 16px; box-shadow: 0 8px 24px #17412b08; }
    .step { display: flex; align-items: center; gap: 10px; margin: 0 0 14px; }
    .step-num { background: #087f3f; color: white; border-radius: 50%; display: grid; place-items: center; width: 27px; height: 27px; font-weight: 700; }
    .step h3 { margin: 0; font: 700 15px 'DM Sans', sans-serif; }
    .step p { margin: 2px 0 0; color: #627681; font-size: 11px; }
    .aside-card { border-radius: 12px; padding: 20px; margin-bottom: 16px; }
    .aside-card h3 { font: 700 16px 'DM Sans', sans-serif; margin: 0 0 8px; }
    .aside-card p { color: #607581; font-size: 12px; line-height: 1.5; margin: 0; }
    .hero-art { height: 135px; margin: -20px -20px 16px; border-radius: 12px 12px 0 0; background: linear-gradient(#eaf5fb,#d6efdf); position: relative; overflow: hidden; }
    .hero-art:before { content: '♻'; position: absolute; left: 35%; top: 25px; display: grid; place-items: center; width: 115px; height: 55px; border-radius: 7px; background: #07833e; color: white; font-size: 32px; box-shadow: 46px 17px 0 -10px #fff, 47px 28px 0 -7px #284b51; }
    .hero-art:after { content: '☁   ☁'; position: absolute; inset: 17px 22px auto; color: #cbe6ef; font-size: 27px; letter-spacing: 55px; }
    .tip { display: flex; gap: 9px; align-items: center; font-size: 12px; color: #31545b; margin: 12px 0; }
    .tip b { color: white; background: #087f3f; width: 17px; height: 17px; display: grid; place-items: center; border-radius: 50%; font-size: 10px; }
    .stButton > button { border-radius: 7px; border-color: #d7e4df; color: #102b31; font-weight: 600; }
    .stButton > button[kind="primary"] { background: #087f3f; border-color: #087f3f; color: white; }
    [data-testid="stFileUploader"] section { border: 1px dashed #bfcfca; background: #fcfefd; }
    .prediction-card { border: 1px solid #b9e3c5; border-left: 5px solid #087f3f; border-radius: 10px; padding: 15px 18px; background: #effaf1; margin: 8px 0 18px; }
    .prediction-card .eyebrow { color: #087f3f; font-size: 10px; letter-spacing: 1.2px; font-weight: 700; margin-bottom: 4px; }
    .prediction-card h2 { margin: 0; font: 800 20px Manrope, sans-serif; color: #123b2a; }
    .prediction-card p { margin: 5px 0 0; color: #4e6d5a; font-size: 12px; }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown('<div class="brand"><b>🌿 Isuku</b><span>Cleaner Communities<br>Greener Rwanda</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-caption">PAGES</div>', unsafe_allow_html=True)
    st.page_link("streamlit_app.py", label="🏠  Household")
    st.page_link("pages/1_Admin_Dashboard.py", label="📊  Admin")
    st.markdown("<br><small>Anne Marie<br>Household account</small>", unsafe_allow_html=True)

st.markdown("<div class='intro'><b style='color:#087f3f;letter-spacing:1.5px;font-size:10px'>HOUSEHOLD SERVICES</b></div>", unsafe_allow_html=True)
st.title("Submit a complaint")
st.markdown('<p class="intro">Report issues related to waste collection or recycling in your area.<br> Your report helps us keep our communities clean and healthy.</p>', unsafe_allow_html=True)

with st.form("complaint_form", clear_on_submit=False):
    st.markdown('<div class="section-card"><div class="step"><span class="step-num">1</span><div><h3>Describe the issue</h3><p>Explain what happened. Our model will classify your complaint automatically.</p></div></div>', unsafe_allow_html=True)
    description = st.text_area("Description", placeholder="Describe your complaint here... (e.g. the waste truck did not come this week)", max_chars=500, height=115, label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

    left, right = st.columns(2)
    with left:
        st.markdown('<div class="section-card"><div class="step"><span class="step-num">2</span><div><h3>Add photos</h3><p>You can upload up to 3 photos.</p></div></div>', unsafe_allow_html=True)
        photos = st.file_uploader("Upload photos", type=["png", "jpg", "jpeg"], accept_multiple_files=True, label_visibility="collapsed")
        st.caption("PNG or JPG up to 5MB each")
        st.markdown('</div>', unsafe_allow_html=True)
    with right:
        st.markdown('<div class="section-card"><div class="step"><span class="step-num">3</span><div><h3>Location</h3><p>Confirm the location of the issue.</p></div></div>', unsafe_allow_html=True)
        location = st.selectbox("Location", ["Kigali, Nyarugenge", "Kigali, Gasabo", "Kigali, Kicukiro"], label_visibility="collapsed")
        st.info("📍 Location will be saved with your complaint")
        st.markdown('</div>', unsafe_allow_html=True)

    submitted = st.form_submit_button("➤  Submit Complaint", type="primary")

if submitted:
    if not description.strip():
        st.error("Please describe what happened before submitting.")
    else:
        try:
            selected_photos = (photos or [])[:3]
            photo_names = save_uploads(selected_photos)
            complaint_id, predicted_category, confidence = save_complaint(None, description.strip(), location, photo_names)
            st.session_state["last_prediction"] = {
                "complaint_id": complaint_id,
                "predicted_category": predicted_category,
                "confidence": confidence,
            }
            st.success(f"Complaint #{complaint_id} submitted successfully. It is now available on the admin dashboard.")
        except Exception as error:
            st.error(f"Could not submit complaint: {error}")

if "last_prediction" in st.session_state:
    result = st.session_state["last_prediction"]
    confidence_text = f"Model confidence: {result['confidence']}%" if result["confidence"] is not None else "Model confidence was not available."
    st.markdown(
        f'<div class="prediction-card"><div class="eyebrow">AI CLASSIFICATION · COMPLAINT #{result["complaint_id"]}</div>'
        f'<h2>{display_category(result["predicted_category"])}</h2>'
        f'<p>Predicted from your complaint description · {confidence_text}</p></div>',
        unsafe_allow_html=True,
    )

with st.sidebar:
    st.markdown('<div class="sidebar-caption">NEED HELP?</div>', unsafe_allow_html=True)
    st.markdown("📞 **+250 788 123 456**\n\nAvailable Mon - Sat, 8:00 AM - 5:00 PM")
