# Setup
import streamlit as st

# Classes

# Functions
def pageSetUp():
    st.header("Dashboard")
    st.divider()

    col1, col2 = st.columns(2)
    col1.metric("Hours logged", st.session_state.totalHours, None, border=True, width="stretch")
    col2.metric("Expected gross", f"${round(st.session_state.gross, 2)}", None, border=True, width="stretch")

    st.session_state.progress = 0
    tasks = {
        "Enter Hours and Pay": False,
        "Estimate Taxes": False,
        "Explore Compounding": False,
        "Search For Banks": False,
    }

    if st.session_state.hoursSubmitted:
        st.session_state.progress += 25
        tasks["Enter Hours and Pay"] = True
    if st.session_state.formSubmitted:
        st.session_state.progress += 25
        tasks["Estimate Taxes"] = True
    if st.session_state.CS:
        st.session_state.progress += 25
        tasks["Explore Compounding"] = True
    if st.session_state.bankFindSub:
        st.session_state.progress += 25
        tasks["Search For Banks"] = True

    progressBar = st.progress(st.session_state.progress, "Your Workflow")
    st.markdown("***Your Progress***")
    for name, completed in tasks.items():
        if completed:
            st.markdown(f"✅ ~~{name}~~ :green[(Completed)]")
        else:
            st.markdown(f"⭕ {name} :gray[(Incomplete)]")

    st.divider()

# On start
pageSetUp()
