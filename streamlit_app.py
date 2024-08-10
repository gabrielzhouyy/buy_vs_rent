import streamlit as st
from common_logic import amortization_calculator, rent_calculator, \
    investment_calculator  # Import the function from common_logic.py

st.title("Buy vs Rent Decision Tool")

# Organize the inputs into two columns with background colors
col1, col2 = st.columns(2)

with col1:
    # Add background color for the BUY column
    st.markdown(
        """
        <div style="background-color: pink; padding: 10px;">
            <h4 style="text-align: center;">BUY</h4>
        """,
        unsafe_allow_html=True
    )

    # Property Loan Inputs
    interest_rate = st.number_input("Annual Interest Rate (%)", min_value=0.0, max_value=20.0, value=7.0)
    loan_amount = st.number_input("Loan Amount ($)", min_value=0.0, value=1100000.0)
    year_tenor = st.number_input("Loan Tenor (years)", min_value=1, value=30)  # Optional parameter
    redemption_year = st.number_input("Duration of Ownership before flipping (years)", min_value=1, value=5)
    sticker_profit_from_home_sales = st.number_input("Profit from Flipping ($)", min_value=0.0, value=140000.0)
    hoa_fee = st.number_input("Monthly HOA Fee ($)", min_value=0.0, value=200.0)
    yearly_maintenance_cost = st.number_input("Annual Taxes/Maintenance/Other Expenses ($)", min_value=0.0, value=1200.0)
    tenor = year_tenor*12
    redemption_month = redemption_year*12

    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    # Add background color for the RENT column
    st.markdown(
        """
        <div style="background-color: lightblue; padding: 10px;">
            <h4 style="text-align: center;">RENT</h4>
        """,
        unsafe_allow_html=True
    )

    # Rental Inputs
    monthly_rent = st.number_input("Initial Monthly Rent ($)", min_value=0.0, value=3100.0)
    inflation = st.number_input("Annual Rent Increase Rate (%)", min_value=0.0, value=5.0)

    # Opportunity Cost Inputs
    initial_deposit = st.number_input("Mortgage Downpayment/Initial Investment ($)", min_value=0.0,
                                      value=200000.0)  # Replace with actual downpayment value
    annual_returns = st.number_input("Annual Return Rate (%)", min_value=0.0, value=5.0)

    st.markdown("</div>", unsafe_allow_html=True)

# Call the amortization_calculator function with user input
cumulative_interest_paid, cumulative_principal_paid, outstanding_principal, monthly_payment, hoa_paid, maintenance_paid = amortization_calculator(
    interest_rate, loan_amount, redemption_month, hoa_fee, yearly_maintenance_cost, tenor)
actual_profit = sticker_profit_from_home_sales - cumulative_interest_paid - hoa_paid - maintenance_paid

# Call the rent_calculator with user input
total_rent_paid, average_monthly_rent, final_monthly_rent = rent_calculator(monthly_rent, inflation, redemption_month)

# Call the investment_calculator with user input
monthly_contribution = monthly_payment - monthly_rent  # Rent, or $3400 monthly contribution
investment_months = redemption_month  # Calculate returns for 60 months (5 years)
annual_contribution_incr_pct = -inflation  # annual contribution decreases since more $ going into rent rather than investment
total_savings_invested, total_investment_gains, final_balance = investment_calculator(
    initial_deposit, monthly_contribution, annual_returns, investment_months, annual_contribution_incr_pct)

# Results Section
st.subheader("Results")

# Organize the results into two columns
result_col1, result_col2 = st.columns(2)

with result_col1:
    st.markdown(
        """
        <div style="background-color: pink; padding: 10px;">
            <h4 style="text-align: center;">BUY SCENARIO</h4>
        """,
        unsafe_allow_html=True
    )
    st.markdown(f"Monthly Housing Expense of **${round(monthly_payment):,}**.")
    st.markdown(f"You bought a property with a **${round(loan_amount):,}** loan.")
    st.markdown(
        f"You sold the place after **{redemption_month}** months and paid **${round(cumulative_interest_paid):,}** in total interest, which was financed by sales profit of **{int(sticker_profit_from_home_sales)}**.")
    st.markdown(f"Overall, your net position from flipping was **${actual_profit:,.0f}**.")
    st.markdown("</div>", unsafe_allow_html=True)

with result_col2:
    st.markdown(
        """
        <div style="background-color: lightblue; padding: 10px;">
            <h4 style="text-align: center;">RENT SCENARIO</h4>
        """,
        unsafe_allow_html=True
    )
    st.markdown(f"Monthly Housing Budget of **${round(monthly_payment):,}**.")
    st.markdown(
        f"You rent at **${int(monthly_rent)}** and invest the remaining of the monthly budget. Your rent increases by **{inflation}%** every year.")
    st.markdown(
        f"After **{int(redemption_month)}** months, you'd have spent **${round(total_rent_paid):,}** on rent. You've invested **{int(total_savings_invested)}** in total, gaining **{int(total_investment_gains)}** in returns at a **{annual_returns}%** return rate.")
    st.markdown(
        f"Overall, your net position from renting and investing was **${int(final_balance - total_rent_paid)}** .")
    st.markdown("</div>", unsafe_allow_html=True)

# Display the results using st.write or other elements
# Organize the results into two columns for Mortgage and Rental/Investment Stats
stats_col1, stats_col2 = st.columns(2)

with stats_col1:
    st.subheader("BUY DETAILS")
    st.write(f"Cumulative Interest Paid: **${round(cumulative_interest_paid):,}**")
    st.write(f"Cumulative Principal Paid: **${round(cumulative_principal_paid):,}**")
    st.write(f"Outstanding Principal: **${round(outstanding_principal):,}**")
    st.write(f"Monthly Payment: **${round(monthly_payment):,}**")
    st.write(f"Total HOA Paid: **${round(hoa_paid):,}**")
    st.write(f"Maintenance Paid: **${round(maintenance_paid):,}**")
    st.write(f"Profit less interest & charges: **${round(actual_profit):,}**")

with stats_col2:
    st.subheader("RENT DETAILS")
    st.write(f"Total Rent Paid: **${round(total_rent_paid):,}**")
    st.write(f"Average Monthly Rent: **${round(average_monthly_rent):,}**")
    st.write(f"Final Monthly Rent: **${round(final_monthly_rent):,}**")
    st.write(f"Budget Available for Investment: **${round(total_savings_invested):,}**")
    st.write(f"Total Investment Gains: **${round(total_investment_gains):,}**")
    st.write(f"Investment Balance after Cost of Rent: **${round(final_balance - total_rent_paid):,}**")

# FAQ Section
st.subheader("FAQ")
st.write("**What are the drawbacks of Buying?**")
st.write("The 2 largest influencers are Opportunity Cost for investment, as well as Amortization. Amortization works in a way where most of your monthly payments go into paying for the interest, rather than reducing the mortgage principal. This trend only reverses after halfway into your loan tenor (i.e., 15 years later).")

st.write("**I buy my house. Why is my net position negative?**")
st.write("This is the cost of housing. A cost is always incurred when buying or renting a place. You only see a net positive if you manage to flip the house at a price greater than the cost of the house plus the total interest paid.")

st.write("**Did you consider the downpayment?**")
st.write("For Buyers, the downpayment is irrelevant regarding your net position because no interest is incurred upon it, nor profit made relevant to it. For Renters, the downpayment amount forms the initial deposit for investment.")