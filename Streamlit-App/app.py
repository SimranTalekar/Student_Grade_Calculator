import html
from datetime import date

import streamlit as st

SCHOOL = "XYZ School of Engineering"
SUBJECTS = ["Mathematics", "Science", "Marathi", "Hindi", "English", "Social Studies"]

# (minimum percentage, grade, remark) - checked from the top down
GRADE_SCALE = [
    (90, "O", "Outstanding"),
    (80, "A+", "Excellent"),
    (70, "A", "Very good"),
    (60, "B+", "Good"),
    (50, "B", "Satisfactory"),
    (40, "C", "Pass"),
]

st.set_page_config(page_title="Student Grade Calculator", page_icon="🎓", layout="centered")

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&family=DM+Sans:wght@400;500;700&display=swap');

:root {
  --ink: #1B2559;
  --paper: #F4F6FB;
  --card: #FFFFFF;
  --line: #DCE1F0;
  --muted: #5B6488;
  --marigold: #F5A623;
  --pass: #0E8F6E;
  --fail: #C8433D;
}

html, body, .stApp, .stApp * { font-family: 'DM Sans', sans-serif; }
h1, h2, h3, .display { font-family: 'Bricolage Grotesque', sans-serif !important; }
.stApp { background: var(--paper); }
.block-container { max-width: 760px; padding-top: 2.4rem; padding-bottom: 4rem; }
#MainMenu, footer, header[data-testid="stHeader"] { visibility: hidden; }

.page-title { font-family: 'Bricolage Grotesque', sans-serif; font-weight: 800; font-size: 2.4rem;
  line-height: 1.1; color: var(--ink); margin: 0 0 .5rem 0; }
.page-sub { color: var(--muted); font-size: 1.02rem; margin-bottom: 1.6rem; max-width: 52ch; }

[data-testid="stForm"] { background: var(--card); border: 1px solid var(--line);
  border-radius: 14px; padding: 1.4rem 1.4rem 1.1rem 1.4rem; }
[data-testid="stForm"] label p { color: var(--ink); font-weight: 500; }
.form-heading { font-family: 'Bricolage Grotesque', sans-serif; font-weight: 700; color: var(--ink);
  font-size: 1.1rem; margin: .2rem 0 .6rem 0; }

.stFormSubmitButton button { background: var(--ink); color: #fff; border: 0; border-radius: 10px;
  font-weight: 700; padding: .65rem 1.6rem; transition: background .15s ease; }
.stFormSubmitButton button:hover { background: #2A3680; color: #fff; }
.stFormSubmitButton button:focus-visible { outline: 3px solid var(--marigold); outline-offset: 2px; }

/* ---- Report card ---- */
.report { background: var(--card); border: 1px solid var(--line); border-radius: 16px;
  overflow: hidden; margin-top: 2rem; box-shadow: 0 10px 30px rgba(27,37,89,.08); }
.report-head { background: var(--ink); color: #fff; padding: 1.3rem 1.6rem;
  border-bottom: 5px solid var(--marigold); display: flex; justify-content: space-between;
  align-items: flex-end; gap: 1rem; flex-wrap: wrap; }
.report-head .school { font-family: 'Bricolage Grotesque', sans-serif; font-weight: 700; font-size: 1.35rem; }
.report-head .doc { color: #C9D0F0; font-size: .95rem; }
.report-head .when { color: #C9D0F0; font-size: .9rem; }

.student { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem;
  padding: 1.2rem 1.6rem; border-bottom: 1px solid var(--line); }
.student .k { color: var(--muted); font-size: .85rem; }
.student .v { color: var(--ink); font-weight: 700; font-size: 1.05rem; word-break: break-word; }

.result { display: flex; align-items: center; gap: 1.6rem; padding: 1.5rem 1.6rem;
  border-bottom: 1px solid var(--line); flex-wrap: wrap; }
.badge { width: 112px; height: 112px; border-radius: 50%; display: flex; align-items: center;
  justify-content: center; font-family: 'Bricolage Grotesque', sans-serif; font-weight: 800;
  font-size: 3rem; color: #fff; flex-shrink: 0; }
.badge.pass { background: var(--pass); }
.badge.fail { background: var(--fail); }
.stats { display: flex; gap: 2rem; flex-wrap: wrap; }
.stat .k { color: var(--muted); font-size: .85rem; }
.stat .v { font-family: 'Bricolage Grotesque', sans-serif; font-weight: 700; font-size: 1.7rem; color: var(--ink); }
.verdict { font-weight: 700; }
.verdict.pass { color: var(--pass); }
.verdict.fail { color: var(--fail); }

.subjects { padding: 1.2rem 1.6rem 1.5rem 1.6rem; }
.row { display: grid; grid-template-columns: 130px 1fr 70px; gap: 1rem; align-items: center; padding: .45rem 0; }
.row .sub { color: var(--ink); font-weight: 500; }
.track { background: #E8ECF7; border-radius: 99px; height: 10px; overflow: hidden; }
.fill { height: 100%; border-radius: 99px; }
.fill.high { background: var(--pass); }
.fill.mid { background: var(--ink); }
.fill.low { background: var(--fail); }
.row .score { text-align: right; color: var(--ink); font-weight: 700; }
.row .score small { color: var(--muted); font-weight: 400; }

@media (max-width: 560px) {
  .student { grid-template-columns: 1fr; }
  .row { grid-template-columns: 100px 1fr 60px; }
  .page-title { font-size: 1.9rem; }
}
</style>
""",
    unsafe_allow_html=True,
)


def get_grade(percentage: float):
    """Return (grade, remark). Uses >= cutoffs so no percentage can fall between two grades."""
    for cutoff, grade, remark in GRADE_SCALE:
        if percentage >= cutoff:
            return grade, remark
    return "F", "Needs improvement"


def bar_class(mark: int) -> str:
    if mark >= 75:
        return "high"
    if mark >= 40:
        return "mid"
    return "low"


def render_report(r: dict) -> None:
    passed = r["grade"] != "F"
    state = "pass" if passed else "fail"
    rows = "".join(
        f'<div class="row"><span class="sub">{s}</span>'
        f'<div class="track"><div class="fill {bar_class(m)}" style="width:{m}%"></div></div>'
        f'<span class="score">{m}<small>/100</small></span></div>'
        for s, m in r["marks"].items()
    )
    card = (
        '<div class="report">'
        '<div class="report-head">'
        f'<div><div class="school">{SCHOOL}</div><div class="doc">Student report card</div></div>'
        f'<div class="when">{date.today():%d %b %Y}</div>'
        "</div>"
        '<div class="student">'
        f'<div><div class="k">Name</div><div class="v">{html.escape(r["name"])}</div></div>'
        f'<div><div class="k">Roll no.</div><div class="v">{r["roll"]}</div></div>'
        f'<div><div class="k">Branch</div><div class="v">{html.escape(r["branch"])}</div></div>'
        "</div>"
        '<div class="result">'
        f'<div class="badge {state}">{r["grade"]}</div>'
        '<div class="stats">'
        f'<div class="stat"><div class="k">Percentage</div><div class="v">{r["per"]:.2f}%</div></div>'
        f'<div class="stat"><div class="k">Total marks</div><div class="v">{r["total"]} / {len(r["marks"]) * 100}</div></div>'
        f'<div class="stat"><div class="k">Result</div><div class="v verdict {state}">{r["remark"]}</div></div>'
        "</div></div>"
        f'<div class="subjects">{rows}</div>'
        "</div>"
    )
    st.markdown(card, unsafe_allow_html=True)


def report_as_text(r: dict) -> str:
    lines = [
        f"{SCHOOL} - Student report card",
        "",
        f"Name    : {r['name']}",
        f"Roll no.: {r['roll']}",
        f"Branch  : {r['branch']}",
        "",
    ]
    lines += [f"{s:<15}: {m}/100" for s, m in r["marks"].items()]
    lines += [
        "",
        f"Total marks : {r['total']}/{len(r['marks']) * 100}",
        f"Percentage  : {r['per']:.2f}%",
        f"Grade       : {r['grade']} ({r['remark']})",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------- page
st.markdown('<div class="page-title">Student grade calculator</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="page-sub">Enter a student\'s details and marks out of 100 in six subjects. '
    "You get the total, percentage, grade and a printable report card.</div>",
    unsafe_allow_html=True,
)

with st.form("marks_form"):
    st.markdown('<div class="form-heading">Student details</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([2, 1, 1.4])
    name = c1.text_input("Name", placeholder="e.g. Aarav Patil")
    roll = c2.number_input("Roll no.", min_value=1, step=1, value=None, placeholder="e.g. 1024")
    branch = c3.text_input("Branch", placeholder="e.g. Computer")

    st.markdown('<div class="form-heading">Marks (out of 100)</div>', unsafe_allow_html=True)
    marks = {}
    cols = st.columns(3)
    for i, subject in enumerate(SUBJECTS):
        marks[subject] = cols[i % 3].number_input(
            subject, min_value=0, max_value=100, step=1, value=None, placeholder="0 - 100"
        )

    submitted = st.form_submit_button("Generate report card")

if submitted:
    missing = (
        not name.strip()
        or roll is None
        or not branch.strip()
        or any(m is None for m in marks.values())
    )
    if missing:
        st.session_state.pop("result", None)
        st.error("Fill in the name, roll no., branch and all six marks to generate the report card.")
    else:
        marks = {s: int(m) for s, m in marks.items()}
        total = sum(marks.values())
        per = total / len(marks)
        grade, remark = get_grade(per)
        st.session_state["result"] = {
            "name": name.strip(),
            "roll": int(roll),
            "branch": branch.strip(),
            "marks": marks,
            "total": total,
            "per": per,
            "grade": grade,
            "remark": remark,
        }

result = st.session_state.get("result")
if result:
    render_report(result)
    st.download_button(
        "Download report card (.txt)",
        data=report_as_text(result),
        file_name=f"report_card_{result['roll']}.txt",
        mime="text/plain",
    )
