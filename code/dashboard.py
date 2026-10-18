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

    st.divider()

# On start
pageSetUp()