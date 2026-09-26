"""
app.py
CKA Exam Progress Tracker — a Streamlit reproduction of the reference
Excel sheet. UI is generated entirely from data.CATEGORIES; no per-row
logic is hard-coded here.

Run with:  streamlit run app.py
"""

import io
import csv
import datetime

import streamlit as st

import data
import database
from styles import get_css

# --------------------------------------------------------------------------
# Page setup
# --------------------------------------------------------------------------
st.set_page_config(page_title="CKA Exam Tracker", layout="wide")
st.markdown(get_css(), unsafe_allow_html=True)

database.init_db()

# --------------------------------------------------------------------------
# State: load persisted progress once per session
# --------------------------------------------------------------------------
if "statuses" not in st.session_state:
    saved = database.load_progress()
    statuses = {}
    for cat in data.CATEGORIES:
        for topic in cat["topics"]:
            statuses[topic["id"]] = saved.get(topic["id"], data.DEFAULT_STATUS)
    st.session_state.statuses = statuses

if "confirm_reset" not in st.session_state:
    st.session_state.confirm_reset = False


def on_status_change(topic_id: int, topic_name: str):
    new_status = st.session_state[f"sel_{topic_id}"]
    st.session_state.statuses[topic_id] = new_status
    database.save_status(topic_id, topic_name, new_status)


# --------------------------------------------------------------------------
# Progress calculations
# --------------------------------------------------------------------------
def calculate_category_progress(category: dict, statuses: dict) -> float:
    topics = category["topics"]
    if not topics:
        return 0.0
    total = sum(data.STATUS_WEIGHT[statuses[t["id"]]] for t in topics)
    return total / len(topics)


def calculate_overall_progress(statuses: dict) -> float:
    all_topics = [t for c in data.CATEGORIES for t in c["topics"]]
    total = sum(data.STATUS_WEIGHT[statuses[t["id"]]] for t in all_topics)
    return total / len(all_topics)


def calculate_weighted_progress(statuses: dict) -> float:
    weighted_sum = 0.0
    for cat in data.CATEGORIES:
        cat_progress = calculate_category_progress(cat, statuses)
        weighted_sum += cat_progress * (cat["weight"] / 100)
    return weighted_sum


def status_counts(statuses: dict) -> dict:
    counts = {opt: 0 for opt in data.STATUS_OPTIONS}
    for s in statuses.values():
        counts[s] += 1
    return counts


# --------------------------------------------------------------------------
# CSV export / import
# --------------------------------------------------------------------------
def export_progress_csv(statuses: dict) -> bytes:
    last_updated = database.get_last_updated()
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["id", "category", "topic", "exam", "status", "last_updated"])
    for cat in data.CATEGORIES:
        for t in cat["topics"]:
            writer.writerow([
                t["id"], cat["name"], t["name"], t["exam"],
                statuses[t["id"]], last_updated.get(t["id"], ""),
            ])
    return buf.getvalue().encode("utf-8")


def import_progress_csv(uploaded_file):
    content = uploaded_file.read().decode("utf-8")
    reader = csv.DictReader(io.StringIO(content))
    entries = []
    valid_ids = {t["id"] for c in data.CATEGORIES for t in c["topics"]}
    for row in reader:
        try:
            tid = int(row["id"])
        except (KeyError, ValueError):
            continue
        status = row.get("status", "").strip()
        if tid in valid_ids and status in data.STATUS_OPTIONS:
            st.session_state.statuses[tid] = status
            entries.append({"id": tid, "name": row.get("topic", ""), "status": status})
    if entries:
        database.save_many(entries)
    return len(entries)


def reset_all():
    all_ids = [t["id"] for c in data.CATEGORIES for t in c["topics"]]
    for tid in all_ids:
        st.session_state.statuses[tid] = data.DEFAULT_STATUS
    database.reset_progress(all_ids, data.DEFAULT_STATUS)


# --------------------------------------------------------------------------
# Header
# --------------------------------------------------------------------------
st.markdown('<div class="cka-title-bar">CKA Exam Tracker</div>', unsafe_allow_html=True)
st.markdown('<div class="cka-subtitle-bar">Ultimate CKA</div>', unsafe_allow_html=True)

# --------------------------------------------------------------------------
# Sidebar: search, filters, reset, export/import
# --------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### Search & Filter")
    search_text = st.text_input("Search CKA topics...", "")
    status_filter = st.selectbox("Status filter", ["All"] + data.STATUS_OPTIONS)
    exam_filter = st.selectbox("Exam filter", ["All", "CKA", "CKA & CKAD"])

    st.markdown("---")
    st.markdown("### Progress data")

    csv_bytes = export_progress_csv(st.session_state.statuses)
    st.download_button(
        "Export Progress (CSV)",
        data=csv_bytes,
        file_name=f"cka_progress_{datetime.date.today().isoformat()}.csv",
        mime="text/csv",
        use_container_width=True,
    )

    uploaded = st.file_uploader("Import Progress (CSV)", type=["csv"])
    if uploaded is not None:
        n = import_progress_csv(uploaded)
        st.success(f"Imported {n} topic statuses.")

    st.markdown("---")
    if not st.session_state.confirm_reset:
        if st.button("Reset Progress", use_container_width=True):
            st.session_state.confirm_reset = True
            st.rerun()
    else:
        st.warning("This will reset ALL 40 topics to 'Yet to Start'. Are you sure?")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Yes, reset", use_container_width=True):
                reset_all()
                st.session_state.confirm_reset = False
                st.rerun()
        with c2:
            if st.button("Cancel", use_container_width=True):
                st.session_state.confirm_reset = False
                st.rerun()


def topic_matches_filters(topic: dict) -> bool:
    if search_text and search_text.lower() not in topic["name"].lower():
        return False
    if status_filter != "All" and st.session_state.statuses[topic["id"]] != status_filter:
        return False
    if exam_filter != "All" and topic["exam"] != exam_filter:
        return False
    return True


# --------------------------------------------------------------------------
# Top summary metrics
# --------------------------------------------------------------------------
overall_pct = calculate_overall_progress(st.session_state.statuses)
weighted_pct = calculate_weighted_progress(st.session_state.statuses)
counts = status_counts(st.session_state.statuses)

m1, m2, m3, m4, m5 = st.columns(5)
with m1:
    st.markdown(
        f'<div class="cka-metric-box"><div class="cka-metric-value">{weighted_pct:.0f}%</div>'
        f'<div class="cka-metric-label">CKA Exam Progress</div></div>',
        unsafe_allow_html=True,
    )
with m2:
    st.markdown(
        f'<div class="cka-metric-box"><div class="cka-metric-value">{overall_pct:.0f}%</div>'
        f'<div class="cka-metric-label">Overall Progress</div></div>',
        unsafe_allow_html=True,
    )
with m3:
    st.markdown(
        f'<div class="cka-metric-box"><div class="cka-metric-value" style="color:{data.STATUS_COLOR["Done"]}">'
        f'{counts["Done"]} / {data.TOTAL_TOPICS}</div><div class="cka-metric-label">Done</div></div>',
        unsafe_allow_html=True,
    )
with m4:
    st.markdown(
        f'<div class="cka-metric-box"><div class="cka-metric-value" style="color:{data.STATUS_COLOR["WIP"]}">'
        f'{counts["WIP"]} / {data.TOTAL_TOPICS}</div><div class="cka-metric-label">WIP</div></div>',
        unsafe_allow_html=True,
    )
with m5:
    st.markdown(
        f'<div class="cka-metric-box"><div class="cka-metric-value" style="color:{data.STATUS_COLOR["Yet to Start"]}">'
        f'{counts["Yet to Start"]} / {data.TOTAL_TOPICS}</div><div class="cka-metric-label">Yet to Start</div></div>',
        unsafe_allow_html=True,
    )

st.progress(overall_pct / 100)
st.markdown('<hr class="cka-sep"/>', unsafe_allow_html=True)


# --------------------------------------------------------------------------
# Category rendering: HTML table (#, Category, Topic, Exam, Status-text)
# + a slim adjacent column of real Streamlit dropdowns to change status.
# --------------------------------------------------------------------------
def build_category_table_html(category: dict, topics: list) -> str:
    color = category["color"]
    cat_pct = calculate_category_progress(category, st.session_state.statuses)
    rows_html = []
    for i, topic in enumerate(topics):
        status = st.session_state.statuses[topic["id"]]
        s_color = data.STATUS_COLOR[status]
        s_weight = "800" if data.STATUS_BOLD[status] else "600"
        cat_cell = ""
        if i == 0:
            cat_cell = (
                f'<td class="cka-category" rowspan="{len(topics)}" '
                f'style="color:{color};">{category["name"]}'
                f'<span class="cka-cat-pct" style="color:{color};">{category["weight"]}%'
                f' &middot; {cat_pct:.0f}% done</span></td>'
            )
        rows_html.append(
            f'<tr>'
            f'<td class="cka-rownum">{topic["id"]}</td>'
            f'{cat_cell}'
            f'<td class="cka-topic">{topic["name"]}</td>'
            f'<td class="cka-exam">{topic["exam"]}</td>'
            f'<td style="text-align:center; color:{s_color}; font-weight:{s_weight};">{status}</td>'
            f'</tr>'
        )
    header = (
        '<tr><th style="width:34px;">#</th><th style="width:150px;">Category</th>'
        '<th>Topic</th><th style="width:90px;">Exam</th><th style="width:100px;">Status</th></tr>'
    )
    return f'<table class="cka-table">{header}{"".join(rows_html)}</table>'


def render_category(category: dict):
    topics = [t for t in category["topics"] if topic_matches_filters(t)]
    st.markdown(
        f'<div style="font-weight:800; font-size:15px; color:{category["color"]}; margin:6px 0 4px 0;">'
        f'{category["id"]} &mdash; {category["name"]} '
        f'<span style="font-weight:600; font-size:12px;">(Weight {category["weight"]}%)</span></div>',
        unsafe_allow_html=True,
    )
    if not topics:
        st.caption("No topics match the current filters.")
        return

    col_table, col_edit = st.columns([5, 1])
    with col_table:
        st.markdown(build_category_table_html(category, topics), unsafe_allow_html=True)
    with col_edit:
        st.markdown('<div class="cka-status-header">Edit</div>', unsafe_allow_html=True)
        for topic in topics:
            tid = topic["id"]
            status = st.session_state.statuses[tid]
            st.markdown('<div class="cka-status-row">', unsafe_allow_html=True)
            st.selectbox(
                f"status_{tid}",
                options=data.STATUS_OPTIONS,
                index=data.STATUS_OPTIONS.index(status),
                key=f"sel_{tid}",
                label_visibility="collapsed",
                on_change=on_status_change,
                args=(tid, topic["name"]),
            )
            st.markdown('</div>', unsafe_allow_html=True)


# --------------------------------------------------------------------------
# Two-block spreadsheet layout
# --------------------------------------------------------------------------
left_col, right_col = st.columns(2)

with left_col:
    for cat_id in data.LEFT_CATEGORY_IDS:
        category = next(c for c in data.CATEGORIES if c["id"] == cat_id)
        render_category(category)
        st.markdown('<hr class="cka-sep"/>', unsafe_allow_html=True)

with right_col:
    for cat_id in data.RIGHT_CATEGORY_IDS:
        category = next(c for c in data.CATEGORIES if c["id"] == cat_id)
        render_category(category)
        st.markdown('<hr class="cka-sep"/>', unsafe_allow_html=True)


# --------------------------------------------------------------------------
# Bottom summary
# --------------------------------------------------------------------------
all_topics = [t for c in data.CATEGORIES for t in c["topics"]]
all_done = all(st.session_state.statuses[t["id"]] == "Done" for t in all_topics)
concepts_answer = "YES" if all_done else "Not Yet"
concepts_color = data.STATUS_COLOR["Done"] if all_done else data.STATUS_COLOR["WIP"]

readiness_label = data.get_readiness_label(weighted_pct)
if readiness_label == "Ready to get your CKA Cert!":
    readiness_color = data.STATUS_COLOR["Done"]
elif readiness_label in ("Nearly Ready", "Almost"):
    readiness_color = data.STATUS_COLOR["WIP"]
else:
    readiness_color = data.STATUS_COLOR["Yet to Start"]

st.markdown(
    f"""
    <div class="cka-bottom-box">
        <div class="cka-bottom-question">Done with - Concepts, Demos, and "Practice"?</div>
        <div class="cka-bottom-answer" style="color:{concepts_color};">{concepts_answer}</div>
        <div class="cka-bottom-question">Ready to get your CKA Cert?</div>
        <div class="cka-bottom-answer" style="color:{readiness_color};">{readiness_label}</div>
    </div>
    """,
    unsafe_allow_html=True,
)
