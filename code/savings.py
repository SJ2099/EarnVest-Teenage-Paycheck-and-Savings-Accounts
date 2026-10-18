# Setup
import streamlit as st
import pandas as pd
import json
import math

# Classes

# Functions
def fillSavingsForm():
    st.session_state.savings_start_balance = round(float(st.session_state.expNet), 2)
    pay_frequency_options = ["Weekly", "Biweekly", "Twice a month", "Every month"]
    questionnaire = st.session_state.get("questionnaire", {})
    saved_pay_frequency = questionnaire.get("OftenPay")
    if saved_pay_frequency not in pay_frequency_options:
        saved_pay_frequency = next(
            (value for value in questionnaire.values() if value in pay_frequency_options),
            "Weekly",
        )
    st.session_state.savings_pay_frequency = saved_pay_frequency

def pageSetUp():
    st.header("Save Your Pay")
    st.text("Learn about different types of saving accounts on this interactive page so you can save and grow your money.")
    st.divider()

    tab1, tab2, tab3 = st.tabs(["Find the right account", "Watch your money grow", "Find the right bank"])

    with tab1:
        st.header("Understanding Savings Accounts")
        st.text("Learn about the advantages and disadvantages of different types of saving accounts")
        st.divider()

        with st.container(border=True, width="stretch", height="stretch"):
            st.subheader("Checking Account")
            pros, cons = st.columns(2)

            with pros:
                st.markdown("**Pros**")
                st.text("▶ Easy access to funds anytime")
                st.text("▶ Allows unlimited deposits and withdrawals")
                st.text("▶ Provides immediate tracking and daily expense management")

            with cons:
                st.markdown("**Cons**")
                st.text("▶ Has very low or no interest")
                st.text("▶ Higher risk of impulse spending")
                st.text("▶ Not structured for long-term wealth accumulation")

        with st.container(border=True, width="stretch", height="stretch"):
            st.subheader("Regular Savings Account")
            pros, cons = st.columns(2)

            with pros:
                st.markdown("**Pros**")
                st.text("▶ In-person access at branch locations and ATMs")
                st.text("▶ Low opening deposit and minimal balance requirements")

            with cons:
                st.markdown("**Cons**")
                st.text("▶ Very low annual percentage yield (APY), money grows slowly and may lose value due to inflation")
                st.text("▶ Many banks charge monthly fees")

        with st.container(border=True, width="stretch", height="stretch"):
            st.subheader("High-Yield Savings Account")
            st.text("Offered mostly by online-only banks")
            pros, cons = st.columns(2)

            with pros:
                st.markdown("**Pros**")
                st.text("▶ Earns signifiantly more interest, often up to 5% APY")
                st.text("▶ Often zero monthly maintenance fees")

            with cons:
                st.markdown("**Cons**")
                st.text("▶ No physical branches, you cannot walk into a physical bank and get a deposit")
                st.text("▶ Slower transfers, moving money typically takes 2-3 business days")

        with st.container(border=True, width="stretch", height="stretch"):
            st.subheader("Certificate of Deposit (CD)")
            st.text("A time-based savings tool with a locked term")
            pros, cons = st.columns(2)

            with pros:
                st.markdown("**Pros**")
                st.text("▶ Locks in a guaranteed interest rate (often 3% to 5% or higher) for set term")
                st.text("▶ Generally no monthly account fees")

            with cons:
                st.markdown("**Cons**")
                st.text("▶ During the set term, your money is locked away. Withdrawing early triggers a penalty which costs money")

        with st.container(border=True, width="stretch", height="stretch"):
            st.subheader("Money Market Deposit Account")
            st.text("A hybrid that combines saving and checking features")
            pros, cons = st.columns(2)

            with pros:
                st.markdown("**Pros**")
                st.text("▶ Usually allows you to spend the money in the account")
                st.text("▶ Often pays higher rates than a regular savings account")

            with cons:
                st.markdown("**Cons**")
                st.text("▶ Often requires a higher opening deposit or larger daily balance to avoid fees")
                st.text("▶ May restrict monthly withdrawals or checks")

    with tab2:
        st.header("Interactive Savings-Growth Calculator")
        st.text("Change a few values and immediately see how your money could grow in this simulation")
        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            st.session_state.setdefault("savings_start_balance", 0.0)
            st.session_state.setdefault("savings_pay_frequency", "Weekly")
            st.button(
                "Fill in from Paycheck",
                on_click=fillSavingsForm,
                disabled=st.session_state.expNet is None,
            )           

            with st.form("savings_growth_form"):
                start_balance = st.number_input(
                    "How much money will you start with in the account?",
                    min_value=0.0,
                    help="Enter the amount in dollars",
                    key="savings_start_balance",
                )
                amount_per_paycheck = st.number_input("How much money per paycheck will you put in?", min_value=0.0, help="Enter the amount in dollars")
                pay_frequency_options = ["Weekly", "Biweekly", "Twice a month", "Every month"]
                pay_frequency = st.radio(
                    "How often are you paid?",
                    pay_frequency_options,
                    key="savings_pay_frequency",
                )
                account_type = st.radio("Which savings account type?", ["Checking Account [0.01% APY]", "Regular Savings Account [0.5% APY]", "High-Yield Savings Account [5% APY]", "Certificate of Deposit (CD) [4% APY]", "Money Market Deposit Account [0.63% APY]", "Custom"], help="Note that for the preset values, the APY can vary from bank to bank, so the values here are just estimates.")

                if account_type == "Checking Account [0.01% APY]":
                    apy = 0.0001
                elif account_type == "Regular Savings Account [0.5% APY]":
                    apy = 0.005
                elif account_type == "High-Yield Savings Account [5% APY]":
                    apy = 0.05
                elif account_type == "Certificate of Deposit (CD) [4% APY]":
                    apy = 0.04
                elif account_type == "Money Market Deposit Account [0.63% APY]":
                    apy = 0.0063
                else:
                    apy = st.slider("What is the annual percentage yield (APY) of your account?", min_value=0.0, max_value=10.0, step=0.001, format="%.3f") / 100

                duration = st.number_input("How many months will you save for?", min_value=1, step=1, help="Enter the number of months")
                submitted = st.form_submit_button("Calculate savings growth")

        with col2:
            with st.container(border=True):    
                if submitted:
                    payments_per_year = {
                        "Weekly": 52,
                        "Biweekly": 26,
                        "Twice a month": 24,
                        "Every month": 12,
                    }[pay_frequency]
                    daily_rate = (1 + apy) ** (1 / 365) - 1
                    total_days = round(duration * 365 / 12)
                    balance = start_balance
                    payment_progress = 0.0
                    balances = [balance]
                    totalPaycheckAdditions = 0.0

                    for _ in range(total_days):
                        balance *= 1 + daily_rate
                        payment_progress += payments_per_year / 365
                        if payment_progress >= 1:
                            balance += amount_per_paycheck
                            totalPaycheckAdditions += amount_per_paycheck
                            payment_progress -= 1
                        balances.append(balance)

                    st.subheader("Savings Growth Over Time")
                    with st.container(border=True, width="stretch", height="stretch"):
                        st.line_chart(pd.DataFrame({"Time (days)": list(range(total_days + 1)), "Account balance ($)": balances}), y="Account balance ($)", x="Time (days)", width="stretch")
                    
                    st.metric("Estimated balance", f"${balance:,.2f}", delta=f"${balance - start_balance:,.2f}", border=True)

                    col1, col2 = st.columns(2)
                    col1.metric("Total paycheck additions", f"${totalPaycheckAdditions:,.2f}", border=True)
                    col2.metric("Total interest earned", f"${balance - start_balance - totalPaycheckAdditions:,.2f}", border=True)
                else:
                    st.text("Fill out the form on the left and click 'Calculate savings growth' to see how your money could grow over time.")

    with tab3:
        st.header("Find the Right Bank")
        st.text("Discover which banks offer the best accounts to help you reach your financial goals.")
        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            with st.form("find_bank_form"):
                preferred_account = st.radio("Preferred account type", ["Checking Account", "Regular Savings Account", "High-Yield Savings Account", "Certificate of Deposit (CD)", "Money Market Deposit Account"], help="Select the type of account you are looking for")
                age_of_user = st.radio("Who will use the account?", ["Under 18", "Over 18"], help="How old is the person who will use this account?")
                preferred_access = st.radio("Preferred access", ["Online banking preferred", "In-person branches preferred", "No preference"], help="Do you prefer to have an in-person or online bank?")
                sort_results = st.radio("Sorts results by:", ["Highest APY", "Lowest fees", "Alphabetical"])

                bank_find_submitted = st.form_submit_button("Find the right bank")

        with col2:
            if bank_find_submitted:
                with open("info/bank_data.json", "r", encoding="utf-8") as file:
                    banks = json.load(file)

                allAccounts = banks["accounts"]
                validOptions = []

                for account in allAccounts:
                    points = 0
                    if preferred_account == "Checking Account" and account["account_type"] == "checking":
                        account["typeEasy"] = "Checking Account"
                        points += 1
                    elif preferred_account == "Regular Savings Account" and account["account_type"] == "savings":
                        account["typeEasy"] = "Regular Savings Account"
                        points += 1
                    elif preferred_account == "High-Yield Savings Account" and "high_yield_savings" in account["categories"]:
                        account["typeEasy"] = "High-Yield Savings Account"
                        points += 1
                    elif preferred_account == "Certificate of Deposit (CD)" and ((account["account_type"] == "cd") or ("cd" in account["categories"])):
                        account["typeEasy"] = "Certificate of Deposit (CD)"
                        points += 1
                    elif preferred_account == "Money Market Deposit Account" and account["account_type"] == "money_market":
                        account["typeEasy"] = "Money Market Deposit Account"
                        points += 1

                    if age_of_user == "Under 18" and account["eligibility"]["under_18_eligible"]:
                        points += 1
                    elif age_of_user == "Over 18":
                        points += 1

                    if preferred_access == "No preference":
                        points += 1
                    elif preferred_access == "In-person branches preferred" and (account["bank_type"] == "regional_bank" or account["bank_type"] == "credit_union"):
                        points += 1
                    elif preferred_access == "Online banking preferred" and account["bank_type"] == "online_bank":
                        points += 1

                    if points >= 3:
                        if account["fees"]["monthly_fee_usd"] is None:
                            account["fees"]["monthly_fee_usd"] = math.inf

                        validOptions.append(account)

                # Sort accounts
                if sort_results == "Highest APY":
                    sortedAccounts = sorted(validOptions, key = lambda x: x["apy"]["value_percent"])
                    sortedAccounts.reverse()
                elif sort_results == "Lowest fees":
                    sortedAccounts = sorted(validOptions, key = lambda x: x["fees"]["monthly_fee_usd"])
                elif sort_results == "Alphabetical":
                    sortedAccounts = sorted(validOptions, key = lambda x: x["institution"])

                validOptions = sortedAccounts

                # Display vertically scrollable list of valid options
                with st.container(height=540, border=True):
                    for account in validOptions:
                        giveContainerFromDict(account)

                    if len(validOptions) == 0:
                        st.markdown(":red[There are unfortunately no banks in the saved database that satisfy those conditions. Please try something else.]")
                
            else:
                with st.container(height=540, border=True):
                    st.text("Please submit the form to the left to find bank accounts that work for you.")

def giveContainerFromDict(account):
    with st.expander(f":material/account_balance: {account["institution"]}"):
        st.subheader(f"**{account["institution"]}**")
        st.markdown(f"**{account["typeEasy"]}**")
        with st.container(horizontal=True):
            st.badge(f"{account["product_name"]}", color="orange")
            if len(account["features"]) > 0:
                st.badge(f"{account["features"][0]}", color="orange")
            if len(account["features"]) > 1:
                st.badge(f"{account["features"][1]}", color="orange")
        
        st.divider()
        st.metric("Annual Percentage Yield (APY)", f":green[{account["apy"]["value_percent"]}%]")

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Monthly Fee", f"${account["fees"]["monthly_fee_usd"]}" if account["fees"]["monthly_fee_usd"] is not None else "$0")
        with col2:
            st.metric("Minimum Opening Deposit", f"${account["fees"]["minimum_opening_deposit_usd"]}" if account["fees"]["minimum_opening_deposit_usd"] is not None else "$0")

        st.text(f"Notes: {account["notes"]}")
        st.link_button("Go to official website", account["official_url"])

# On start
pageSetUp()