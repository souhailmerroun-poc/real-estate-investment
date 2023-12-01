import streamlit as st
import pandas as pd

# Function to calculate the percentage breakdown and cumulative amounts
def calculate_breakdown(salary, amount_1, amount_2, amount_3):
    # Create a DataFrame for the 60-month projection
    data = {
        'Month': range(1, 61),
        '50% Cumulative': [amount_1 * month for month in range(1, 61)],
        '30% Cumulative': [amount_2 * month for month in range(1, 61)],
        '20% Cumulative': [amount_3 * month for month in range(1, 61)]
    }
    return pd.DataFrame(data)

# Check if the total amount is not equal to the salary
def check_total():
    if 'amount_1' in st.session_state and 'amount_2' in st.session_state and 'amount_3' in st.session_state:
        total = st.session_state.amount_1 + st.session_state.amount_2 + st.session_state.amount_3
        if total > st.session_state.salary:
            overflow = total - st.session_state.salary
            st.error(f"The total of the allocated amounts exceeds your salary by {overflow} EUR. Please adjust to fit within your salary.")
        elif total < st.session_state.salary:
            shortfall = st.session_state.salary - total
            st.error(f"The total of the allocated amounts is less than your salary by {shortfall} EUR. Please adjust to fit your salary.")
        return total == st.session_state.salary
    return False

# Streamlit UI
st.title("Salary Breakdown and Projection App")

# Input field for salary
salary = st.number_input("Enter your salary", value=3800, key='salary', step=1)

# Input fields for breakdown amounts with callback to check the total
amount_1 = st.number_input("50% Amount", value=int(salary * 0.5), key='amount_1', on_change=check_total, step=1)
amount_2 = st.number_input("30% Amount", value=int(salary * 0.3), key='amount_2', on_change=check_total, step=1)
amount_3 = st.number_input("20% Amount", value=int(salary * 0.2), key='amount_3', on_change=check_total, step=1)

# Calculating and displaying the projection if total matches salary
if check_total():
    df = calculate_breakdown(salary, amount_1, amount_2, amount_3)
    st.write("60 Month Projection:")
    st.dataframe(df)