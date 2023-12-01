import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Function to round values to two decimal places
def round_two_decimals(value):
    return round(value, 2)

# Function to calculate the loan details
def calculate_loan_details(real_estate_value, initial_payment, interest_rate, max_monthly_payment, monthly_savings, start_date):
    # Initial setup
    remaining_loan = real_estate_value - initial_payment
    total_interest = 0
    monthly_interest_rate = interest_rate / 12 / 100
    wallet = 0
    records = []

    # Monthly calculations
    while remaining_loan > 0:
        interest = remaining_loan * monthly_interest_rate
        total_interest += interest
        payment = min(max_monthly_payment, remaining_loan + interest)
        remaining_loan += interest - payment
        remaining_loan = round_two_decimals(remaining_loan)
        wallet += monthly_savings
        wallet = round_two_decimals(wallet)
        records.append([start_date.strftime('%B %Y'), round_two_decimals(payment), wallet, remaining_loan])
        start_date += timedelta(days=30)  # approximate one month

    # Preparing the final summary
    total_months = len(records)
    total_paid = total_interest + real_estate_value - initial_payment
    total_paid = round_two_decimals(total_paid)
    total_interest = round_two_decimals(total_interest)

    return records, total_interest, total_paid, total_months

# Callback function to update initial payment percentage
def update_initial_payment_percentage():
    initial_payment = st.session_state.initial_payment
    real_estate_value = st.session_state.real_estate_value
    st.session_state.initial_percentage = round_two_decimals((initial_payment / real_estate_value) * 100)

# Callback function to update initial payment amount
def update_initial_payment_amount():
    initial_percentage = st.session_state.initial_percentage
    real_estate_value = st.session_state.real_estate_value
    st.session_state.initial_payment = round_two_decimals((initial_percentage / 100) * real_estate_value)

# Streamlit UI
st.title("Real Estate Loan Simulator")

# Input fields
real_estate_value = st.number_input("Real Estate Value (EUR)", value=100000, key="real_estate_value")
initial_payment = st.number_input("Initial Payment (EUR)", value=20000, key="initial_payment", on_change=update_initial_payment_percentage)
initial_percentage = st.number_input("Initial Payment (%)", value=20, key="initial_percentage", on_change=update_initial_payment_amount)
interest_rate = st.number_input("Interest Rate (%)", value=4.0)
max_monthly_payment = st.number_input("Max Monthly Payment (EUR)", value=1600)
monthly_savings = st.number_input("Monthly Savings in Wallet (EUR)", value=1460)

# Button to start simulation
if st.button('Simulate'):
    start_date = datetime(2024, 1, 1)
    results, total_interest, total_paid, total_months = calculate_loan_details(
        real_estate_value, initial_payment, interest_rate, max_monthly_payment, monthly_savings, start_date
    )

    # Displaying the results in a table
    st.write("Simulation Results:")
    df = pd.DataFrame(results, columns=['Month', 'Payment to Loan', 'Wallet', 'Remaining Loan'])
    st.dataframe(df)  # Changed from st.table to st.dataframe to display all rows

    # Displaying the summary
    st.write("Total Initial Amount:", real_estate_value)
    st.write("Total Interest Amount:", total_interest)
    st.write("Total Paid:", total_paid)
    st.write("Total Number of Months:", total_months)