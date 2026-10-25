# Setup
import streamlit as st
import pandas as pd
import json
import os
from datetime import date, datetime, time

if "shifts" not in st.session_state:
    st.session_state.shifts = []

if "gross" not in st.session_state:
    st.session_state.gross = 0

if "totalHours" not in st.session_state:
    st.session_state.totalHours = 0

if "hoursSubmitted" not in st.session_state:
    st.session_state.hoursSubmitted = False

if ("shiftsData" not in st.session_state):
    st.session_state.shiftsData = pd.DataFrame([
        {
            "Job Name": None,
            "Date": None,
            "Start Time": None,
            "End Time": None,
            "Overtime Hours": None,
            "Unpaid Break Length (mins)": None,
            "Hourly Wage": None,
            "Overtime Wage": None,
            "Days Repeated": None,
        }
    ])

if "expNet" not in st.session_state:
    st.session_state.expNet = None

if "totalTax" not in st.session_state:
    st.session_state.totalTax = None

if "allTaxes" not in st.session_state:
    st.session_state.allTaxes = {}

if "formSubmitted" not in st.session_state:
    st.session_state.formSubmitted = False

# Questionnaire about state, and other things to understand taxes
if "questionnaire" not in st.session_state:
    st.session_state.questionnaire = {}

if "calcsubmitted" not in st.session_state:
    st.session_state.calcsubmitted = False

if "CS" not in st.session_state:
    st.session_state.CS = False

if "allTaxes" not in st.session_state:
    st.session_state.allTaxes = {}

if "bank_find_submitted" not in st.session_state:
    st.session_state.bank_find_submitted = False

if "bankFindSub" not in st.session_state:
    st.session_state.bankFindSub = False

if "progress" not in st.session_state:
    st.session_state.progress = 0

# Classes

# Functions
def pageSetUp(allowLogins=False):
    st.set_page_config(
        page_title="EarnVest - Understand and Maximize Your Paycheck",
        page_icon="📈",
        layout="wide"
    )

    st.title(":material/verified_user: :violet[Earn]:green[Vest] for Teens")
    st.markdown("**Understand** and **Maximize** Your Paycheck")
    st.logo("images/logo-bg.png", size="large")
    st.divider()

    dashboardPage = st.Page("dashboard.py", title="Dashboard", icon=":material/dashboard:")
    hourlogPage = st.Page("hourlog.py", title="Hour Log", icon=":material/schedule:")
    calculatorPage = st.Page("calculator.py", title="Pay Calculator", icon=":material/calculate:")
    comparisonPage = st.Page("comparison.py", title="Comparison", icon=":material/document_search:")
    savingsPage = st.Page("savings.py", title="Save Your Pay", icon=":material/savings:")
    
    pg = st.navigation([dashboardPage, hourlogPage, calculatorPage, comparisonPage, savingsPage])
    pg.run()

# On start
pageSetUp()
