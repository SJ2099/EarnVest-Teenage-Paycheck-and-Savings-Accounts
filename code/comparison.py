# Setup
import streamlit as st
import pandas as pd

# Classes

# Functions
def pageSetUp():
    st.header("Comparison")
    st.text("Compare your estimated take-home pay and total withholdings with what is actually shown on your paystub.")
    st.divider()

    st.text("Below is a table with each part of the tax calculation used in the estimated formula on this website. Once you have received your paycheck, you can enter your values in the column to the right, and then compare the website's estimated values with what actually appeared on your paystub.")
    st.text("NOTE: The values in the table are estimates with some variables set constant to simplify the tax calculation process on the website. If the numbers on your paystub are different from those of the estimations, it is not necessarily proof that your employer paid you incorrectly.")
    st.divider()

    if ("userSystemTaxData" not in st.session_state) and ("allTaxes" in st.session_state) and (st.session_state.allTaxes != {}):
        d = {"Tax": list(st.session_state.allTaxes.keys()), "Estimated Value ($)": list(st.session_state.allTaxes.values()), "Actual Value ($)": [0] * len(st.session_state.allTaxes), "Difference ($)": [0] * len(st.session_state.allTaxes)}
        st.session_state.userSystemTaxData = pd.DataFrame(d)
    elif "userSystemTaxData" not in st.session_state:
        return
    
    st.data_editor(st.session_state.userSystemTaxData, width="stretch", height="stretch", hide_index=True, disabled=["Tax", "Estimated Value ($)", "Difference ($)"], key="tax_comparison_editor", on_change=updateDifferences)

def updateDifferences():
    edited_rows = st.session_state.tax_comparison_editor["edited_rows"]

    df = st.session_state.userSystemTaxData.copy()

    for index, changes in edited_rows.items():
        if "Actual Value ($)" in changes:
            df.at[index, "Actual Value ($)"] = changes["Actual Value ($)"]

    df["Difference ($)"] = (
        df["Actual Value ($)"]
        - df["Estimated Value ($)"]
    )

    st.session_state.userSystemTaxData = df

# On start
pageSetUp()