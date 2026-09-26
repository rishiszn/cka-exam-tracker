"""
styles.py
All CSS for the spreadsheet-like look lives here, kept separate from
layout/logic in app.py.
"""

ROW_HEIGHT_PX = 34


def get_css() -> str:
    return f"""
<style>
/* ---------- page ---------- */
.block-container {{
    padding-top: 1rem;
    padding-bottom: 2rem;
    max-width: 1500px;
}}
body, .stApp {{
    background-color: #FFFFFF;
}}

/* ---------- header ---------- */
.cka-title-bar {{
    background-color: #1F6FD1;
    color: #FFFFFF;
    text-align: center;
    font-size: 30px;
    font-weight: 800;
    padding: 14px 0 6px 0;
    border: 1px solid #14477F;
    font-family: 'Segoe UI', Arial, sans-serif;
}}
.cka-subtitle-bar {{
    background-color: #4A4458;
    color: #FFFFFF;
    text-align: center;
    font-size: 15px;
    font-weight: 700;
    padding: 6px 0;
    border: 1px solid #14477F;
    border-top: none;
    font-family: 'Segoe UI', Arial, sans-serif;
    margin-bottom: 14px;
}}

/* ---------- spreadsheet table (Number / Category / Topic / Exam) ---------- */
table.cka-table {{
    border-collapse: collapse;
    width: 100%;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 13px;
    table-layout: fixed;
}}
table.cka-table th {{
    background-color: #D9D9D9;
    border: 1px solid #808080;
    padding: 4px 6px;
    text-align: center;
    font-weight: 700;
    height: {ROW_HEIGHT_PX}px;
}}
table.cka-table td {{
    border: 1px solid #808080;
    padding: 3px 6px;
    height: {ROW_HEIGHT_PX}px;
    vertical-align: middle;
    background-color: #FFFFFF;
    overflow: hidden;
    text-overflow: ellipsis;
}}
td.cka-rownum {{
    text-align: center;
    color: #444444;
    width: 34px;
}}
td.cka-topic {{
    text-align: left;
}}
td.cka-exam {{
    text-align: center;
    font-size: 12px;
    color: #333333;
    width: 90px;
}}
td.cka-category {{
    text-align: center;
    font-weight: 800;
    vertical-align: middle;
    width: 150px;
    font-size: 13px;
}}
td.cka-category .cka-cat-pct {{
    display: block;
    margin-top: 4px;
    font-size: 15px;
    font-weight: 800;
}}

/* ---------- status column header + spacer, aligned by row height ---------- */
.cka-status-header {{
    background-color: #D9D9D9;
    border: 1px solid #808080;
    border-left: none;
    text-align: center;
    font-weight: 700;
    height: {ROW_HEIGHT_PX}px;
    line-height: {ROW_HEIGHT_PX}px;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 13px;
}}
.cka-status-row {{
    border: 1px solid #808080;
    border-left: none;
    border-top: none;
    height: {ROW_HEIGHT_PX}px;
    display: flex;
    align-items: center;
    padding-left: 4px;
}}
.cka-status-row div[data-testid="stSelectbox"] {{
    width: 100%;
}}
.cka-status-row div[data-baseweb="select"] > div {{
    min-height: 26px;
    height: 26px;
    border: 1px solid #999999;
    border-radius: 2px;
}}

/* status text colors are applied inline per-select via a small colored
   dot + label rendered next to the widget in app.py */
.status-dot {{
    display: inline-block;
    width: 9px;
    height: 9px;
    border-radius: 50%;
    margin-right: 6px;
}}

/* ---------- progress summary ---------- */
.cka-metric-box {{
    border: 1px solid #B0B0B0;
    background-color: #F7F7F7;
    border-radius: 4px;
    padding: 10px 14px;
    text-align: center;
    font-family: 'Segoe UI', Arial, sans-serif;
}}
.cka-metric-value {{
    font-size: 26px;
    font-weight: 800;
    color: #1F6FD1;
}}
.cka-metric-label {{
    font-size: 12px;
    color: #555555;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}

/* ---------- bottom summary ---------- */
.cka-bottom-box {{
    border: 2px solid #808080;
    padding: 14px 18px;
    font-family: 'Segoe UI', Arial, sans-serif;
    background-color: #FFFFFF;
}}
.cka-bottom-question {{
    font-weight: 700;
    font-style: italic;
    color: #1F3864;
    font-size: 15px;
}}
.cka-bottom-answer {{
    font-weight: 800;
    font-size: 17px;
    margin-bottom: 10px;
}}

hr.cka-sep {{
    border: none;
    border-top: 1px solid #CCCCCC;
    margin: 18px 0;
}}
</style>
"""
