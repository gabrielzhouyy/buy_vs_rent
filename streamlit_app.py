import streamlit as st
from common_logic import amortization_calculator  # Import the function from logic.py

st.title("Amortization Calculator")

# Input fields for function parameters
interest_rate = st.slider("Interest Rate (%)", 0.0, 20.0, 4.0)
loan_amount = st.number_input("Loan Amount ($)", min_value=0, value=1300000)
redemption_month = st.number_input("Redemption Month", min_value=1, value=72)
hoa_fee = st.number_input("HOA Fee ($)", min_value=0, value=200)
yearly_maintenance_cost = st.number_input(
    "Yearly Maintenance Cost ($)", min_value=0, value=1200
)
tenor = st.number_input("Loan Tenor (months)", min_value=1, value=360)

# Call the amortization_calculator function with user input
results = amortization_calculator(
    interest_rate, loan_amount, redemption_month, hoa_fee, yearly_maintenance_cost, tenor
)

# Unpack the returned values (assuming they are in the same order as the function definition)
cumulative_interest_paid, cumulative_principal_paid, outstanding_principal, monthly_payment, hoa_paid, maintenance_paid = results

# Display the results using st.write or other elements
st.subheader("Amortization Results")
st.write(f"Cumulative Interest Paid: ${cumulative_interest_paid:.2f}")
st.write(f"Cumulative Principal Paid: ${cumulative_principal_paid:.2f}")
st.write(f"Outstanding Principal: ${outstanding_principal:.2f}")
st.write(f"Monthly Payment: ${monthly_payment:.2f}")
st.write(f"Total HOA Paid: ${hoa_paid:.2f}")
st.write(f"Maintenance Paid: ${maintenance_paid:.2f}")

# Note: We can't directly "return" print statements from functions in Streamlit apps.
# We achieve similar functionality by using st.write or other elements to display the calculated values.