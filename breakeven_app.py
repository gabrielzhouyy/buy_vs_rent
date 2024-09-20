import pandas as pd
import streamlit as st
import warnings

warnings.filterwarnings("ignore")


def pmt(rate, nper, pv, fv=0, when=0):
    # mimics numpy_financial.pmt function
    if rate == 0:
        return -(pv + fv) / nper

    # Adjust for when payments are made at the beginning of the period
    if when == 'begin' or when == 1:
        when = 1
    else:
        when = 0

    # Calculate the periodic payment
    payment = (rate * (pv * (1 + rate) ** nper + fv)) / ((1 + rate * when) * ((1 + rate) ** nper - 1))
    return -payment


def amortization_table(interest_rate, loan_amount, redemption_month, hoa, yearly_maintenance_cost, tenor=360):
    """
    Creates an amortization table for a loan.

    :param interest_rate: in percentage (8%)
    :param loan_amount: (in $)
    :param redemption_month: (# months)
    :param hoa: monthly HOA fee (in $)
    :param yearly_maintenance_cost: yearly maintenance cost (in $)
    :param tenor: (in months)
    :return: A list of lists representing each row of the amortization table.
    """

    monthly_interest = interest_rate / 12 / 100
    monthly_maintenance_cost = yearly_maintenance_cost / 12
    monthly_payment = pmt(monthly_interest, tenor, -loan_amount)

    amortization_data = []
    outstanding_principal = loan_amount
    cumulative_interest_paid = 0
    cumulative_principal_paid = 0
    hoa_paid = 0
    maintenance_paid = 0
    year = 1
    month = 0
    payment = 0

    for payment in range(1, redemption_month):
        interest_payment = outstanding_principal * monthly_interest
        principal_payment = monthly_payment - interest_payment

        cumulative_interest_paid += interest_payment
        cumulative_principal_paid += principal_payment
        hoa_paid += hoa
        maintenance_paid += monthly_maintenance_cost

        outstanding_principal -= principal_payment
        month += 1

        amortization_data.append([
            payment,
            year,
            month % 12,
            monthly_payment,
            interest_payment,
            cumulative_interest_paid,
            outstanding_principal,
            hoa_paid,
            maintenance_paid
        ])

        if payment % 12 == 0:
            year += 1

        if outstanding_principal <= 0:
            break

    return amortization_data


def get_cost_metrics(interest_rate, loan_amount, redemption_month, hoa, yearly_maintenance_cost, tenor=360):
    df = pd.DataFrame(
        amortization_table(interest_rate, loan_amount, redemption_month, hoa, yearly_maintenance_cost, tenor=360),
        columns=["payment", "year", "month", "monthly_payment", "interest_paid",
                 "cumulative_interest_paid", "outstanding_principal", "hoa_paid", "maintenance_paid"])
    df['loan_amt'] = loan_amount
    df['avr_monthly_interest'] = df['cumulative_interest_paid'] / df['payment']  # Over the tenor, monthly cost of funds
    df['total_interest_and_fees'] = df['cumulative_interest_paid'] + df['hoa_paid'] + df[
        'maintenance_paid']  # Over the tenor, cost of funds + fees
    df['total_fees'] = df['hoa_paid'] + df['maintenance_paid']
    df['avr_monthly_fees'] = df['total_fees'] / df['payment']
    df['avr_monthly_interest_and_fees'] = df['total_interest_and_fees'] / df['payment']
    df['avr_monthly_principal'] = loan_amount / tenor
    df['avr_monthly_interest_and_principal'] = df['avr_monthly_interest'] + df['avr_monthly_principal']
    df['avr_monthly_interest_principal_fees'] = df['avr_monthly_interest_and_fees'] + df['avr_monthly_principal']
    df = df.round(2)

    return df.tail(1)  # Take the last entry as we assume no redemption


# the = get_costs(5.6, 1000000, 360, 450, 100, tenor=360)


def produce_break_even_table(interest, tenor, hoa, maintenance):
    df = get_cost_metrics(interest, 100000, tenor, hoa, maintenance, tenor=tenor)
    new_dfs = []
    for i in range(110000, 1210000, 10000):
        new_df = get_cost_metrics(interest, i, tenor, hoa, maintenance, tenor)
        new_dfs.append(new_df)

    # Concatenate the original DataFrame with the new ones
    df = pd.concat([df] + new_dfs, ignore_index=True)
    df2 = df[['loan_amt', 'year',
              'avr_monthly_interest_principal_fees',
              'avr_monthly_principal',
              'avr_monthly_interest',
              'avr_monthly_fees',
              'cumulative_interest_paid',
              ]]

    return df2


# Copy starts here:
st.title("Buy vs Rent Break-Even Chart")

st.markdown("""
    *Is your rent money going to waste?*

    See how much a mortgage would cost you and compare it to your current rent. If the numbers are similar, consider taking out a loan and owning your own home! Related: [Buy vs Rent Simulator](https://gzhou-buy-vs-rent.streamlit.app/)

    """)

# User Inputs
interest_rate = st.number_input("Annual Interest Rate (%)", min_value=0.0, max_value=20.0, value=7.0)
year_tenor = st.number_input("Loan Tenor (years)", min_value=1, value=30)  # Optional parameter
hoa_fee = st.number_input("Monthly Expenses/HOA ($)", min_value=0.0, value=200.0)
yearly_maintenance_cost = st.number_input("Annual Expenses (Taxes/Maintenance/Others) ($)", min_value=0.0, value=15000.0)
tenor = year_tenor * 12

# Call the functions
display_table = produce_break_even_table(interest_rate, tenor, hoa_fee, yearly_maintenance_cost)
display_table = display_table.set_index('loan_amt').sort_values(by='loan_amt', ascending=False)

# Teach user how to use the table
st.markdown("""
    Compare your rent against the **average monthly interest + principal + fees**.

    The moment your rent increases to correspond with the loan amount needed for a home purchase, if you buy, you'd break-even for the full loan term, and make gains after that.

    """)

# Print the table
st.dataframe(display_table)

# Teach user how to use the table
st.markdown("""
    ## How it works

    - First, mortgage is computed using the [PMT formula](https://en.wikipedia.org/wiki/Compound_interest#Monthly_amortized_loan_or_mortgage_payments). You can do it youself with an [amortization calculator](https://bretwhissel.net/cgi-bin/amortize).

    - Next, monthly and annual fees are added to get a cumulative cost over the entire term of the loan.

    - Then, these costs are divided equally into monthly installments to easily compare against your monthly rent. It's really just the same as the installment your creditor provides you with.

    - Finally, we repeat this across various loan amounts so you can get a sense of how much loan your rent will break-even with.

    """)



