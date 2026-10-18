# Setup
import streamlit as st
import sqlite3 as sql
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

if "allTaxes" not in st.session_state:
    st.session_state.allTaxes = {}

# Classes

# Functions
def addDataToUser(username):
    username = username.strip()
    if not username:
        return

    file_path = "info/user_data.json"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            users = json.load(file, object_hook=_json_object_hook)
    except (FileNotFoundError, json.JSONDecodeError):
        users = {}

    # Widget state is managed by Streamlit and cannot safely be restored directly.
    users[username] = {
        key: value
        for key, value in st.session_state.items()
        if key != "shiftsData_editor"
    }
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(users, file, default=_json_default)


def _json_default(value):
    if isinstance(value, pd.DataFrame):
        return {"__type__": "DataFrame", "data": value.to_dict(orient="split")}
    if isinstance(value, (datetime, date, time)):
        return {"__type__": type(value).__name__, "data": value.isoformat()}
    if hasattr(value, "item"):
        return value.item()
    raise TypeError(f"Cannot save value of type {type(value).__name__} to JSON")


def _json_object_hook(value):
    value_type = value.get("__type__")
    if value_type == "DataFrame":
        data = value["data"]
        # Keep the saved columns exactly as-is, but let pandas create a fresh
        # default index so an old row index is not shown as part of the table.
        return pd.DataFrame(data["data"], columns=data["columns"])
    constructors = {
        "datetime": datetime.fromisoformat,
        "date": date.fromisoformat,
        "time": time.fromisoformat,
    }
    if value_type in constructors:
        return constructors[value_type](value["data"])
    return value

def logInUserData(username):
    username = username.strip()
    if not username:
        return

    try:
        with open("info/user_data.json", "r", encoding="utf-8") as file:
            users = json.load(file, object_hook=_json_object_hook)
    except (FileNotFoundError, json.JSONDecodeError):
        st.error("No saved user data was found.")
        return

    if username not in users:
        st.error("No saved data was found for that username.")
        return

    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.session_state.update(
        {
            key: value
            for key, value in users[username].items()
            if key != "shiftsData_editor"
        }
    )

def pageSetUp():
    st.set_page_config(
        page_title="EarnVest - Understand and Maximize Your Paycheck",
        page_icon=":material/verified_user:",
        layout="wide"
    )

    st.title(":material/verified_user: EarnVest for Teens")
    st.text("Understand and Maximize Your Paycheck")
    st.logo("images/logo-bg.png", size="large")
    st.divider()

    dashboardPage = st.Page("dashboard.py", title="Dashboard", icon=":material/dashboard:")
    hourlogPage = st.Page("hourlog.py", title="Hour Log", icon=":material/schedule:")
    calculatorPage = st.Page("calculator.py", title="Pay Calculator", icon=":material/calculate:")
    comparisonPage = st.Page("comparison.py", title="Comparison", icon=":material/document_search:")
    savingsPage = st.Page("savings.py", title="Save Your Pay", icon=":material/savings:")
    
    pg = st.navigation([dashboardPage, hourlogPage, calculatorPage, comparisonPage, savingsPage])
    pg.run()

    with st.sidebar:
        username = st.text_input("Username: ")
        st.button("Import Data", on_click=logInUserData, args=[str(username)])
        st.button("Export Data", on_click=addDataToUser, args=[str(username)])

# On start
pageSetUp()
