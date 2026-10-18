# Setup
import streamlit as st

# Classes

# Functions
def onChange():
    st.session_state.formSubmitted = False

def pageSetUp():
    st.header("Pay Calculator")
    st.text("Here, you can answer some questions to see what taxes will withhold your paycheck, and you can see an estimation of what your take-home pay should be.")
    st.divider()

    col1, col2 = st.columns(2)
    col1.metric("Expected gross", f"${round(st.session_state.gross, 2)}", None, border=True, width="stretch")
    col2.metric("Hours logged", st.session_state.totalHours, None, border=True, width="stretch")
    
    col3, col4 = st.columns(2)
    col3.metric("Expected take-home pay (estimation)", f"${"---" if st.session_state.expNet == None else round(st.session_state.expNet, 2)}", border=True, width="stretch", delta=f"{"---%" if st.session_state.expNet == None else str(round(round(st.session_state.expNet/st.session_state.gross, 4) * 100, 4)) + "%"}", delta_arrow="off", delta_color="orange")
    col4.metric("Total withholdings (estimation)", f"${"---" if st.session_state.totalTax == None else round(st.session_state.totalTax, 2)}", border=True, width="stretch", delta=f"{"---%" if st.session_state.totalTax == None else str(round(round(st.session_state.totalTax/st.session_state.gross, 4) * 100, 4)) + "%"}", delta_arrow="off", delta_color="orange")

    for index, row in st.session_state.shiftsData.iterrows():
        if isinstance(row["Hourly Wage"], (int, float)):
            if float(row["Hourly Wage"]) < 15.00:
                st.error(f"Your hourly wage for your {row["Job Name"]} job on {row["Date"]} is below the minimum wage.")
            elif float(row["Hourly Wage"]) == 15.00:
                st.info(f"Your hourly wage for your {row["Job Name"]} job on {row["Date"]} is at the minimum wage.")

    preSubmitQ = {}

    st.divider()
    st.text("Please answer the following questions to estimate your tax withholdings and net pay.")
    st.divider()

    preSubmitQ["OftenPay"] = st.radio("1. How often are you paid?", ["Weekly", "Biweekly", "Twice a month", "Monthly"], on_change=onChange)
    preSubmitQ["MultipleJobs"] = st.radio("2. Is the multiple-jobs checkbox in Step 2 of your W-4 checked?", ["Yes", "No"], on_change=onChange)

    preSubmitQ["ExemptFederal"] = st.radio("3. What information appears on your federal Form W-4? Are you exempt from federal income-tax withholding?", ["'Exempt from withholding' is checked", "I am not exempt from a withholding", "I'm not sure"], on_change=onChange)

    preSubmitQ["W4Step3"] = st.number_input("4. What amount did you enter in Step 3 of your W-4? If you don't know, enter 0.", min_value=0.0, step=0.01, on_change=onChange)

    preSubmitQ["ExtraWithholding"] = st.radio("5. Do you request extra federal withholding?", ["Yes", "No", "Not sure"], on_change=onChange)

    if preSubmitQ["ExtraWithholding"] == "Yes":
        preSubmitQ["ExtraWithholdingAmount"] = st.number_input("6. How much extra federal withholding do you request per paycheck?", min_value=0.0, step=0.01, on_change=onChange)
    else:
        preSubmitQ["ExtraWithholdingAmount"] = 0
    
    preSubmitQ["Exemptions"] = st.number_input(f"{"7" if preSubmitQ["ExtraWithholding"] == "Yes" else "6"}. How many exemptions do you claim on your W-4?", min_value=0, step=1, on_change=onChange)

    preSubmitQ["CombinedYTD"] = st.number_input(f"{"8" if preSubmitQ["ExtraWithholding"] == "Yes" else "7"}. What is the combined year-to-date amount of Social Security and Medicare taxes withheld on your previous paychecks this year? If you have not received a paycheck yet, enter 0.", min_value=0.0, step=0.01, on_change=onChange)

    st.button("Submit", on_click=submitValues, args=(preSubmitQ,))

    if st.session_state.formSubmitted:
        st.text("✅ Questionnaire submitted. Scroll up to see your estimated take-home pay and total withholdings.")

def submitValues(dict):
    if st.session_state.hoursSubmitted:
        st.session_state.questionnaire = dict
        st.session_state.totalTax, st.session_state.expNet, st.session_state.allTaxes = calculateNetPay(st.session_state.questionnaire)
        st.session_state.formSubmitted = True
    else:
        st.toast(":red[Please go to the Hours Log page and submit your hours first.]", duration="long")

def calculateNetPay(dict):
    gross = st.session_state.gross
    allTaxes = {}

    # Calculate social security and medicare
    SS = gross * 0.062
    M = gross * 0.0145

    allTaxes["Social Security"] = SS
    allTaxes["Medicare"] = M

    # Calculate federal income tax withholding 
    N = [52, 26, 24, 12][["Weekly", "Biweekly", "Twice a month", "Monthly"].index(dict["OftenPay"])]
    W = gross * N
    A = D = 0
    if dict["MultipleJobs"] == "No":
        S = 8600
    else:
        S = 0 # S becomes something else reliant on another table if they have multiple jobs

    W_adjusted = max(0, W + A - D - S)

    allTaxes["Annual Wage"] = W
    allTaxes["Adjusted Annual Wage"] = W_adjusted
    
    if W_adjusted >= 328350:
        B = 96489.63
        L = 328350
        r = 0.37
    elif W_adjusted >= 136163:
        B = 29224.00
        L = 136163
        r = 0.35
    elif W_adjusted >= 108938:
        B = 20512.00
        L = 108938
        r = 0.32
    elif W_adjusted >= 60900:
        B = 8983.00
        L = 60900
        r = 0.24
    elif W_adjusted >= 33250:
        B = 2900.00
        L = 33250
        r = 0.22
    elif W_adjusted >= 14250:
        B = 620.00
        L = 14250
        r = 0.12
    elif W_adjusted >= 8050:
        B = 0.00
        L = 8050
        r = 0.1
    elif W_adjusted >= 0:
        B = 0.00
        L = 0
        r = 0
    
    T_annual = B + ((W_adjusted - L)*r)
    T_paycheck = T_annual / N
    C = float(dict["W4Step3"])
    X = float(dict["ExtraWithholdingAmount"])
    F = max(0, (T_paycheck - (C/N))) + X

    allTaxes["Total Annual Tax Before Exemptions"] = T_annual
    allTaxes["Total Tax Per Paycheck Before Exemptions"] = T_paycheck

    if dict["ExemptFederal"] == "'Exempt from withholding' is checked":
        F = 0

    allTaxes["Federal Income Tax"] = F

    # Calculate state income tax withholding
    E_etc = SS + M
    E_ytdbc = float(dict["CombinedYTD"])

    allTaxes["Eligible Contributions From Paycheck"] = E_etc
    allTaxes["Eligible Deducted YTD"] = E_ytdbc

    E_C = min(E_etc, max(0, 2000 - E_ytdbc))

    allTaxes["Amount Deducted from Current Paycheck Withholding"] = E_C

    e = int(dict["Exemptions"])

    if e == 0:
        E_MA = 0
    else:
        if dict["OftenPay"] == "Weekly":
            E_MA = 66 + 19*e
        elif dict["OftenPay"] == "Biweekly":
            E_MA = 131 + 38*e
        elif dict["OftenPay"] == "Twice a month":
            E_MA = 141 + 42*e
        elif dict["OftenPay"] == "Monthly":
            E_MA = 284 + 83*e

    B_MA = max(0, gross - E_C - E_MA)

    S_MA = B_MA * 0.05

    allTaxes["M4 Exemption Amount"] = E_MA
    allTaxes["Withholding Base"] = B_MA
    allTaxes["State Income Tax Withholding"] = S_MA

    # Get final net pay
    netPay = gross - F - SS - M - S_MA
    totalTax = F + SS + M + S_MA

    allTaxes["Net Pay"] = netPay
    allTaxes["Total Withholdings"] = totalTax

    return totalTax, netPay, allTaxes

# On start
pageSetUp()