"""FollowThrough review dashboard.

Run after installing requirements:
    streamlit run app.py

This dashboard deliberately stops at the human approval gate. It never sends
an email or writes to an external service.
"""

from pathlib import Path

import streamlit as st

from agent import build_agent, check_calendar, draft_with_nova, parse_inquiry, search_portfolio

SAMPLES_DIR = Path(__file__).parent / "sample_inquiries"

st.set_page_config(page_title="FollowThrough", page_icon="✦", layout="wide")
st.title("FollowThrough")
st.caption("Turn a new client inquiry into a grounded proposal draft — with human approval required.")

sample_files = sorted(SAMPLES_DIR.glob("*.txt"))
choices = {sample.name: sample for sample in sample_files}
selected_name = st.selectbox("Demo inquiry", choices)
default_text = choices[selected_name].read_text(encoding="utf-8")
inquiry_text = st.text_area("Client inquiry", value=default_text, height=220)

if st.button("Prepare proposal", type="primary"):
    with st.spinner("Parsing inquiry, retrieving portfolio context, and drafting with Amazon Nova..."):
        inquiry = parse_inquiry(inquiry_text)
        matches = search_portfolio(inquiry_text)
        slots = check_calendar()
        agent = build_agent()
        draft = draft_with_nova(agent, inquiry, matches)

    st.session_state["inquiry"] = inquiry
    st.session_state["matches"] = matches
    st.session_state["slots"] = slots
    st.session_state["draft"] = draft
    st.session_state.pop("approved", None)

if "draft" in st.session_state:
    inquiry = st.session_state["inquiry"]
    matches = st.session_state["matches"]
    slots = st.session_state["slots"]

    left, right = st.columns([1, 1])
    with left:
        st.subheader("Agent reasoning")
        st.metric("Urgency", inquiry["urgency"])
        st.write("**Budget signal:**", inquiry["budget_signal"])
        st.write("**Timezone hint:**", inquiry["timezone_hint"])
        st.write("**Relevant past work:**")
        if matches:
            for match in matches:
                st.markdown(f"- **{match['title']}** — {match['summary']}")
        else:
            st.info("No strong past-project match found. The draft is told not to fabricate one.")

        st.write("**Suggested call times:**")
        for slot in slots:
            st.markdown(f"- {slot}")

    with right:
        st.subheader("Draft — human approval required")
        draft = st.text_area("Proposal email", value=st.session_state["draft"], height=320)
        st.session_state["draft"] = draft
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Approve draft", type="primary"):
                st.session_state["approved"] = True
        with col2:
            if st.button("Keep editing"):
                st.session_state["approved"] = False

        if st.session_state.get("approved"):
            st.success("Approved by a human. FollowThrough has prepared this draft — it has not sent anything.")
        else:
            st.warning("Awaiting human approval. No email will be sent automatically.")
