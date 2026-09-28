import html

import streamlit as st

from streamlit_utils import display_category, load_complaints

st.set_page_config(page_title="Isuku | Admin Dashboard", page_icon="📊", layout="wide")
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@700;800&display=swap');
    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
    [data-testid="stAppViewContainer"] { background: #f7faf8; }
    [data-testid="stSidebar"] { background: linear-gradient(165deg,#073b2d,#082c28); }
    [data-testid="stSidebar"] * { color: #eef8f1; }
    .brand { padding: 10px 3px 24px; border-bottom: 1px solid #ffffff20; color: #fff; }
    .brand b { display: block; font: 800 25px/1 Manrope, sans-serif; }
    .brand span { color: #a7d8bd; font-size: 10px; }
    .caption { color: #8bc5a4; font-size: 10px; letter-spacing: 1.5px; font-weight: 700; margin: 25px 0 8px; }
    h1, h2, h3 { color: #102b31; font-family: Manrope, sans-serif; }
    h1 { font-size: 2rem !important; letter-spacing: -1px; margin-bottom: 3px !important; }
    .dashboard-note { color: #627681; font-size: 13px; margin: 0 0 18px; }
    .top-rule { height: 1px; background: #e2ebe7; margin: 0 0 20px; }
    [data-testid="stMetric"] { min-height: 95px; background: white; border: 1px solid #e2ebe7; border-radius: 9px; padding: 13px; }
    [data-testid="stMetricLabel"] { color: #526b74; font-size: 10px; }
    [data-testid="stMetricValue"] { color: #102b31; font: 800 21px Manrope, sans-serif; }
    .metric-total { border-top: 3px solid #2da36a !important; }
    .metric-missed { border-top: 3px solid #60b982 !important; background: #f0fbf2 !important; }
    .metric-delayed { border-top: 3px solid #f0ae35 !important; background: #fff8e9 !important; }
    .metric-full { border-top: 3px solid #3a9cc5 !important; background: #eef8fc !important; }
    .metric-illegal { border-top: 3px solid #dc7182 !important; background: #fff0f3 !important; }
    .metric-recycling { border-top: 3px solid #9e6ce0 !important; background: #f7f0ff !important; }
    .metric-food { border-top: 3px solid #d99a35 !important; background: #fff8e8 !important; }
    .metric-icon { font-size: 18px; margin-bottom: 7px; }
    .section-bar { display: flex; justify-content: space-between; align-items: center; margin: 18px 0 8px; }
    .section-bar h2 { font: 800 15px Manrope, sans-serif; margin: 0; }
    .table-wrap { overflow-x: auto; border: 1px solid #e2ebe7; border-radius: 8px; background: white; }
    .complaint-table { width: 100%; min-width: 790px; border-collapse: collapse; font-size: 11px; color: #29434d; }
    .complaint-table th { background: #fbfdfc; color: #6d8189; font-size: 9px; letter-spacing: .4px; text-align: left; text-transform: uppercase; padding: 12px 9px; border-bottom: 1px solid #e5ecea; }
    .complaint-table td { padding: 11px 9px; border-bottom: 1px solid #edf2f0; vertical-align: middle; }
    .complaint-table tr:last-child td { border: 0; }
    .row-number { color: #80939a; width: 25px; }
    .date { color: #526b74; white-space: nowrap; font-size: 10px; }
    .description { max-width: 230px; color: #17353d; }
    .location { color: #6e8289; white-space: nowrap; }
    .badge { display: inline-block; border-radius: 12px; padding: 5px 8px; font-size: 9px; font-weight: 700; white-space: nowrap; }
    .missed { background: #dcf5e3; color: #16783e; }.delayed { background: #fff0d2; color: #a36600; }.full { background: #dff2fb; color: #14729a; }.illegal { background: #ffe2e8; color: #b44962; }.recycling { background: #eee0ff; color: #7742ae; }
    .status-new { background: #deefff; color: #2775b5; }.status-in-progress { background: #fff0c8; color: #a46b00; }.status-assigned { background: #eadfff; color: #7650b1; }.status-resolved { background: #dcf5e3; color: #16783e; }
    .empty-state { padding: 35px 20px; text-align: center; color: #698089; }
    .stButton > button { border-radius: 7px; border-color: #d7e4df; color: #102b31; font-weight: 600; }
    .stButton > button[kind="primary"] { background: #087f3f; border-color: #087f3f; color: white; }
    </style>
    """,
    unsafe_allow_html=True,
)

def badge_class(category):
    return {
        "missed_pickup": "missed",
        "delayed_pickup": "delayed",
        "full_bin": "full",
        "illegal_dumping": "illegal",
        "recycling_question": "recycling",
    }.get(category, "missed")

def status_class(status):
    return status.lower().replace(" ", "-")

def render_table(dataframe):
    rows = []
    for index, complaint in enumerate(dataframe.to_dict("records"), start=1):
        prediction = complaint["predicted_category"]
        label = html.escape(display_category(prediction))
        description = html.escape(complaint["description"])
        location = html.escape(complaint["location"])
        created_at = html.escape(complaint["created_at"].replace("T", " ")[:16])
        status = html.escape(complaint["status"])
        rows.append(
            f"<tr><td class='row-number'>{index}</td><td class='date'>{created_at}</td>"
            f"<td class='description'>{description}</td><td><span class='badge {badge_class(prediction)}'>{label}</span></td>"
            f"<td class='location'>{location}</td><td><span class='badge status-{status_class(status)}'>{status}</span></td>"
            f"<td class='row-number'>•••</td></tr>"
        )
    return """<div class="table-wrap"><table class="complaint-table"><thead><tr>
        <th>#</th><th>Date &amp; Time</th><th>Complaint Text</th><th>Model Prediction</th>
        <th>Location</th><th>Status</th><th>Actions</th></tr></thead><tbody>""" + "".join(rows) + "</tbody></table></div>"

with st.sidebar:
    st.markdown('<div class="brand"><b>🌿 Isuku</b><span>Admin Panel</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="caption">PAGES</div>', unsafe_allow_html=True)
    st.page_link("streamlit_app.py", label="🏠  Household")
    st.page_link("pages/1_Admin_Dashboard.py", label="📊  Admin")
    st.markdown("<br><small>Anne Marie<br>Administrator</small>", unsafe_allow_html=True)

top_left, top_right = st.columns([4, 1])
with top_left:
    st.text_input("Search", placeholder="Search complaints, locations, or households...", label_visibility="collapsed")
with top_right:
    st.button("🔔  Notifications", use_container_width=True)

st.title("Complaints Dashboard")
st.markdown('<p class="dashboard-note">All submitted complaints are automatically classified using our NLP model.</p>', unsafe_allow_html=True)
st.markdown('<div class="top-rule"></div>', unsafe_allow_html=True)

data = load_complaints()
total = len(data)
counts = data["predicted_category"].value_counts() if total else {}
metric_data = [
    ("▤", "Total Complaints", total, "metric-total"),
    ("▣", "Missed Pickup", counts.get("missed_pickup", 0), "metric-missed"),
    ("◷", "Delayed Pickup", counts.get("delayed_pickup", 0), "metric-delayed"),
    ("♜", "Full Bin", counts.get("full_bin", 0), "metric-full"),
    ("⌂", "Illegal Dumping", counts.get("illegal_dumping", 0), "metric-illegal"),
    ("♻", "Recycling Question", counts.get("recycling_question", 0), "metric-recycling"),
]
metric_columns = st.columns(6)
for column, (icon, label, value, style_class) in zip(metric_columns, metric_data):
    column.markdown(f'<div class="{style_class}"></div>', unsafe_allow_html=True)
    column.markdown(f'<div class="metric-icon">{icon}</div>', unsafe_allow_html=True)
    column.metric(label, value)

tab_recent, tab_category, tab_map = st.tabs(["Recent Complaints", "By Category", "Map View"])
with tab_recent:
    header_left, header_right = st.columns([5, 1])
    with header_left:
        st.markdown('<div class="section-bar"><h2>Recent Complaints</h2></div>', unsafe_allow_html=True)
    with header_right:
        if st.button("↻  Refresh", use_container_width=True):
            st.rerun()
    if data.empty:
        st.markdown('<div class="empty-state">No household complaints yet. Submit one from the household page and it will appear here automatically.</div>', unsafe_allow_html=True)
    else:
        st.markdown(render_table(data), unsafe_allow_html=True)
        st.caption(f"Showing all {total} submitted complaint{'s' if total != 1 else ''}")

with tab_category:
    if data.empty:
        st.info("Category analytics will appear after the first household submission.")
    else:
        category_summary = data["predicted_category"].map(display_category).value_counts().rename_axis("Category").reset_index(name="Complaints")
        st.bar_chart(category_summary.set_index("Category"))

with tab_map:
    if data.empty:
        st.info("Locations will appear after the first household submission.")
    else:
        st.dataframe(data[["location", "predicted_category", "status", "created_at"]], hide_index=True, use_container_width=True)
