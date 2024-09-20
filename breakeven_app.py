import pandas as pd
import streamlit as st
import warnings

warnings.filterwarnings("ignore")


st.title("Buy vs Rent Break-Even Chart")

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
        month +=1

        amortization_data.append([
            payment,
            year,
            month%12,
            monthly_payment,
            interest_payment,
            cumulative_interest_paid,
            outstanding_principal,
            hoa_paid,
            maintenance_paid
        ])

        if payment % 12 ==0:
            year += 1



        if outstanding_principal <= 0:
            break

    return amortization_data



def get_cost_metrics(interest_rate, loan_amount, redemption_month, hoa, yearly_maintenance_cost, tenor=360):
    df = pd.DataFrame(amortization_table(interest_rate, loan_amount, redemption_month, hoa, yearly_maintenance_cost, tenor=360),
                      columns=["payment", "year", "month", "monthly_payment", "interest_paid",
                               "cumulative_interest_paid", "outstanding_principal", "hoa_paid", "maintenance_paid"])
    df['loan_amt'] = loan_amount
    df['avr_monthly_interest'] = df['cumulative_interest_paid'] / df['payment']                                 # Over the tenor, monthly cost of funds
    df['total_interest_and_fees'] = df['cumulative_interest_paid'] + df['hoa_paid'] + df['maintenance_paid']    # Over the tenor, cost of funds + fees
    df['avr_monthly_interest_and_fees'] = df['total_interest_and_fees'] / df['payment']
    df['avr_monthly_principal'] = loan_amount/tenor
    df['avr_monthly_interest_and_principal'] = df['avr_monthly_interest'] + df['avr_monthly_principal']
    df['avr_monthly_interest_principal_fees'] = df['avr_monthly_interest_and_fees'] + df['avr_monthly_principal']
    df = df.round(2)

    return df.tail(1) # Take the last entry as we assume no redemption

# the = get_costs(5.6, 1000000, 360, 450, 100, tenor=360)





def produce_break_even_table(interest, tenor, hoa, maintenance):
    df = get_cost_metrics(interest, 100000, tenor, hoa, maintenance, tenor=tenor)
    new_dfs = []
    for i in range(110000, 1200000, 10000):
        new_df = get_cost_metrics(interest, i, tenor, hoa, maintenance, tenor)
        new_dfs.append(new_df)

    # Concatenate the original DataFrame with the new ones
    df = pd.concat([df] + new_dfs, ignore_index=True)
    df2 = df[['loan_amt', 'year','month','avr_monthly_interest',
              'avr_monthly_interest_and_fees',
              'cumulative_interest_paid',
              'avr_monthly_principal',
              'avr_monthly_interest_and_principal',
              'avr_monthly_interest_principal_fees'
              ]]

    return df2

display_table = produce_break_even_table(5.6, 60, 450, 100)

st.dataframe(display_table.sort_values(by='loan_amt', ascending=False))




