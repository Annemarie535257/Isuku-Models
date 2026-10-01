import streamlit as st

from streamlit_utils import (
    display_category,
    predict,
    predict_with_embedding,
)


st.set_page_config(
    page_title="Isuku | Model Comparison",
    page_icon="🧪",
    layout="wide",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@700;800&display=swap');
    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
    [data-testid="stAppViewContainer"] { background: radial-gradient(circle at 90% 5%, #eef8f0 0, transparent 30%), #f7faf8; }
    [data-testid="stSidebar"] { background: linear-gradient(165deg, #073b2d, #082c28); }
    [data-testid="stSidebar"] * { color: #eef8f1; }
    h1, h2, h3 { color: #102b31; font-family: Manrope, sans-serif; }
    h1 { font-size: 2rem !important; letter-spacing: -1px; }
    .intro { color: #627681; font-size: 14px; line-height: 1.5; margin-bottom: 20px; }
    .result { border: 1px solid #e0ebe5; border-top: 4px solid #087f3f; border-radius: 9px; background: white; padding: 18px; min-height: 145px; }
    .result.embedding { border-top-color: #287da8; }
    .eyebrow { color: #668078; font-size: 10px; font-weight: 700; letter-spacing: 1.2px; }
    .result h2 { margin: 8px 0 5px; font-size: 21px; }
    .result p { color: #627681; font-size: 12px; margin: 0; }
    .stButton > button { border-radius: 7px; font-weight: 600; }
    .stButton > button[kind="primary"] { background: #087f3f; border-color: #087f3f; color: white; }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("<h2 style='color:white'>🌿 Isuku</h2>", unsafe_allow_html=True)
    st.caption("Model evaluation")
    st.page_link("streamlit_app.py", label="🏠  Household")
    st.page_link("pages/1_Admin_Dashboard.py", label="📊  Admin")
    st.page_link("pages/2_Model_Comparison.py", label="🧪  Compare models")

st.title("Compare complaint models")
st.markdown(
    '<p class="intro">Enter one complaint to see how the TF-IDF model and the GloVe embedding model classify the same text.</p>',
    unsafe_allow_html=True,
)

description = st.text_area(
    "Complaint description",
    placeholder="Example: The communal bin is full and overflowing.",
    height=130,
)

if st.button("Compare models", type="primary", use_container_width=False):
    if not description.strip():
        st.warning("Enter a complaint description first.")
    else:
        try:
            tfidf_prediction, tfidf_confidence = predict(description.strip())
            embedding_prediction, embedding_confidence = predict_with_embedding(description.strip())
            left, right = st.columns(2)
            with left:
                confidence = f"Confidence: {tfidf_confidence}%" if tfidf_confidence is not None else "Confidence unavailable"
                st.markdown(
                    f'<div class="result"><div class="eyebrow">TF-IDF MODEL</div>'
                    f'<h2>{display_category(tfidf_prediction)}</h2><p>{confidence}</p></div>',
                    unsafe_allow_html=True,
                )
            with right:
                confidence = f"Confidence: {embedding_confidence}%" if embedding_confidence is not None else "Confidence unavailable"
                st.markdown(
                    f'<div class="result embedding"><div class="eyebrow">GLOVE EMBEDDING MODEL</div>'
                    f'<h2>{display_category(embedding_prediction)}</h2><p>{confidence}</p></div>',
                    unsafe_allow_html=True,
                )
            if tfidf_prediction == embedding_prediction:
                st.success("Both models returned the same category.")
            else:
                st.info("The models returned different categories. This is useful for reviewing borderline complaints.")
        except Exception as error:
            st.error(f"Could not compare the models: {error}")