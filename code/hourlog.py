# Setup
import streamlit as st
import pandas as pd
from datetime import datetime

# Classes

# Functions
def onChange():
    st.session_state.hoursSubmitted = False

def pageSetUp():
    st.header("Hour Log")
    st.text("For each row in the table below, fill in the required information regarding your most recent pay period for each shift. If you have the same information for multiple days, set the Days Repeated column, extra rows are only necessary for different shifts or different jobs. Once you have filled in the information, go the the tax calculation page.")
    st.divider()

    st.session_state.shiftsData["Date"] = pd.to_datetime(
        st.session_state.shiftsData["Date"],
        errors="coerce"
    ).dt.date

    edited_shifts = st.data_editor(
        st.session_state.shiftsData,
        num_rows="dynamic",
        width="stretch",
        key="shiftsData_editor",
        column_config={
            "Job Name": st.column_config.TextColumn("Job Name"),
            "Date": st.column_config.DateColumn("Date", help="Submit amount in YYYY-MM-DD format."),
            "Start Time": st.column_config.TextColumn("Start Time", help="Submit amount in HH:MM format."),
            "End Time": st.column_config.TextColumn("End Time", help="Submit amount in HH:MM format."),
            "Overtime Hours": st.column_config.NumberColumn("Overtime Hours", help="Enter the number of overtime hours worked."),
            "Unpaid Break Length (mins)": st.column_config.NumberColumn("Unpaid Break Length (mins)", help="Enter the length of any unpaid breaks in minutes."),
            "Hourly Wage": st.column_config.NumberColumn("Hourly Wage", help="Submit amount in XX.XX format."),
            "Overtime Wage": st.column_config.NumberColumn("Overtime Wage", help="Submit amount in XX.XX format."),
            "Days Repeated": st.column_config.NumberColumn("Days Repeated", help="How many times have you done this exact schedule?"),
        },
        on_change=onChange,
    )

    st.button("Update Hours and Gross", on_click=lambda: updateInfo(edited_shifts), icon=":material/update:")

    if st.session_state.hoursSubmitted:
        st.text("✅ Hours and gross updated. Continue to Pay Calculator page to find your estimated take-home pay.")

def updateInfo(shifts):
    try:
        st.session_state.shiftsData = shifts
        st.session_state.totalHours = 0
        listOfGrosses = []
        for index, row in st.session_state.shiftsData.iterrows():
            start = datetime.strptime(row["Start Time"], "%H:%M")
            end = datetime.strptime(row["End Time"], "%H:%M")

            hours = ((end - start).total_seconds() - (float(row["Unpaid Break Length (mins)"]) * 60)) / 3600
            overtimeHours = float(row["Overtime Hours"])
            st.session_state.totalHours += (hours + overtimeHours) * float(row["Days Repeated"])
            listOfGrosses.append((st.session_state.totalHours * float(row["Hourly Wage"])) + (overtimeHours * float(row["Overtime Wage"])))

        st.session_state.gross = sum(listOfGrosses)
        st.session_state.hoursSubmitted = True

    except:
        st.toast(":red[Please do leave any fields blank. If necessary, fill empty fields with 0.]", duration="long")

# On start
pageSetUp()