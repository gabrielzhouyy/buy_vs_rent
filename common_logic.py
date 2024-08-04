
import numpy_financial as npf

def amortization_calculator(interest, loan_amount, redemption_month, hoa, yearly_maintenance_cost, tenor=360):
    """
    Calculates the important stats from selling a property
    :param interest: in percentage (8%)
    :param loan_amount: (in $)
    :param redemption_month: (# months)
    :param hoa: monthly HOA fee (in $)
    :param yearly_maintenance_cost: yearly maintenance cost (in $)
    :param tenor: (in months)
    :return: cumulative_interest_paid, cumulative_principal_paid, outstanding_principal, monthly_payment, hoa_paid, maintenance_paid
    """
    monthly_interest = interest / 12 / 100
    monthly_maintenance_cost = yearly_maintenance_cost / 12

    # Calculate monthly payment using numpy_financial's pmt function
    monthly_payment = npf.pmt(monthly_interest, tenor, -loan_amount)

    # Initialize variables
    cumulative_interest_paid = 0
    cumulative_principal_paid = 0
    outstanding_principal = loan_amount
    hoa_paid = 0
    maintenance_paid = 0

    for month in range(1, redemption_month + 1):
        # Calculate interest for the month
        interest_payment = outstanding_principal * monthly_interest
        principal_payment = monthly_payment - interest_payment

        # Update cumulative totals
        cumulative_interest_paid += interest_payment
        cumulative_principal_paid += principal_payment
        hoa_paid += hoa
        maintenance_paid += monthly_maintenance_cost

        # Update outstanding principal
        outstanding_principal -= principal_payment

        # If the loan has been fully paid off, break the loop
        if outstanding_principal <= 0:
            outstanding_principal = 0
            break


    return cumulative_interest_paid, cumulative_principal_paid, outstanding_principal, monthly_payment, hoa_paid, maintenance_paid

# # Property Loan Params:
# interest = 4  # 8% annual interest
# loan_amount = 1300000  # $1,400,000 loan
# hoa = 200  # $200 monthly HOA fee
# yearly_maintenance_cost = 1200  # $1200 yearly maintenance cost
# tenor = 360  # Defaults to 30 years (360 months) loan unless specified
# redemption_month = 72  # Loan redeemed in 60 months (5 years)
#
# cumulative_interest_paid, cumulative_principal_paid, outstanding_principal, monthly_payment, hoa_paid, maintenance_paid = amortization_calculator(interest, loan_amount, redemption_month, hoa, yearly_maintenance_cost, tenor)
#
# print(f"Cumulative Interest Paid: ${cumulative_interest_paid:.2f}")
# print(f"Cumulative Principal Paid: ${cumulative_principal_paid:.2f}")
# print(f"Outstanding Principal: ${outstanding_principal:.2f}")
# print(f"Monthly Payment: ${monthly_payment:.2f}")
# print(f"Total HOA Paid: ${hoa_paid:.2f}")
# print(f"Maintenance Paid: ${maintenance_paid:.2f}")



def rent_calculator(monthly_rent, inflation, redemption_month):
    """
    Calculates the total and average monthly rent over a specified period, taking into account yearly inflation
    :param monthly_rent: initial monthly rent (in $)
    :param inflation: yearly inflation rate (in %)
    :param redemption_month: total number of months to calculate rent for
    :return: total_rent, average_monthly_rent
    """
    total_rent = 0
    months = 0
    inflation_rate = inflation / 100

    while months < redemption_month:
        for _ in range(12):
            if months >= redemption_month:
                break
            total_rent += monthly_rent
            months += 1
        monthly_rent += monthly_rent * inflation_rate

    average_monthly_rent = total_rent / months
    final_monthly_rent = monthly_rent

    return total_rent, average_monthly_rent, final_monthly_rent

# # Rental Projections:
# monthly_rent = 3100  # $1000 initial monthly rent
# inflation = 3.5  # 2% yearly inflation
# redemption_month = 72  # Calculate rent for 60 months (5 years)
#
# total_rent_paid, average_monthly_rent, final_monthly_rent = rent_calculator(monthly_rent, inflation, redemption_month)
#
# print(f"Total Rent Paid: ${total_rent_paid:.2f}")
# print(f"Average Monthly Rent: ${average_monthly_rent:.2f}")
# print(f"Final Monthly Rent: ${final_monthly_rent:.2f}")



# # Property Sales Params
# raw_profit = 200000
# raw_profit_less_interest_paid = raw_profit - cumulative_interest_paid
# actual_profit = raw_profit_less_interest_paid - hoa_paid - maintenance_paid
# actual_profit
#
# print(f'Flipping a house after {redemption_month/12} yrs would change your savings by ${actual_profit:.0f} versus -${total_rent_paid:.0f} if you rented.')
#
#
# # Opportunity Cost
# downpayment_mortgage = 200000

def investment_calculator(initial_deposit, monthly_contribution, annual_returns, investment_months, annual_contribution_incr_pct=0):
    """
    Calculates the compounded investment returns over a specified period, including an initial deposit and monthly contributions
    :param initial_deposit: initial investment amount (in $)
    :param monthly_contribution: monthly investment contribution (in $)
    :param annual_returns: annual return rate (in %)
    :param investment_months: total number of months to calculate returns for
    :param annual_contribution_incr_pct: annual increase in monthly contribution (in %)
    :return: total_savings_invested, total_investment_gains, final_balance
    """
    monthly_returns = annual_returns / 12 / 100
    total_savings_invested = initial_deposit
    principle = initial_deposit
    months = 0

    while months < investment_months:
        for _ in range(12):
            if months >= investment_months:
                break
            principle += principle * monthly_returns + monthly_contribution
            total_savings_invested += monthly_contribution
            months += 1
        monthly_contribution += monthly_contribution * (annual_contribution_incr_pct / 100)

    total_investment_gains = principle - total_savings_invested
    final_balance = principle

    return total_savings_invested, total_investment_gains, final_balance

# # Example usage:
# initial_deposit = downpayment_mortgage  # $200,000 initial deposit
# monthly_contribution = 3400  # Rent, or $3400 monthly contribution
# annual_returns = 7  # 7% annual return rate
# investment_months = 60  # Calculate returns for 60 months (5 years)
# annual_contribution_incr_pct = 2  # 2% annual increase in monthly contribution
#
# total_savings_invested, total_investment_gains, final_balance = investment_calculator(initial_deposit, monthly_contribution, annual_returns, investment_months, annual_contribution_incr_pct)
#
# print(f"Total Savings Invested: ${int(total_savings_invested)}")
# print(f"Total Investment Gains: ${int(total_investment_gains)}")
# print(f"Final Balance: ${int(final_balance)}")









# raw_profit_less_interest_paid = raw_profit - cumulative_interest_paid
# actual_profit = raw_profit_less_interest_paid - hoa_paid - maintenance_paid
# actual_profit


# Full Run

# Property Loan Params:
interest = 7  # 8% annual interest
loan_amount = 1100000  # $1,400,000 loan
hoa = 200  # $200 monthly HOA fee
yearly_maintenance_cost = 1200  # $1200 yearly maintenance cost
tenor = 360  # Defaults to 30 years (360 months) loan unless specified
redemption_month = 60  # Loan redeemed in 60 months (5 years)
sticker_profit_from_home_sales = 140000
actual_profit = sticker_profit_from_home_sales - cumulative_interest_paid - hoa_paid - maintenance_paid
cumulative_interest_paid, cumulative_principal_paid, outstanding_principal, monthly_payment, hoa_paid, maintenance_paid = amortization_calculator(interest, loan_amount, redemption_month, hoa, yearly_maintenance_cost, tenor)

# Rental Params:
monthly_rent = 3100  # $1000 initial monthly rent
inflation = 5  # 2% yearly inflation
redemption_month = redemption_month  # Calculate rent for 60 months (5 years)
total_rent_paid, average_monthly_rent, final_monthly_rent = rent_calculator(monthly_rent, inflation, redemption_month)

# Opportunity Cost Params:
downpayment_mortgage = 40344.74
initial_deposit = downpayment_mortgage  # $200,000 initial deposit or downpayment mortgage
monthly_contribution = monthly_payment - monthly_rent  # Rent, or $3400 monthly contribution
annual_returns = 5  # 7% annual return rate
investment_months = redemption_month  # Calculate returns for 60 months (5 years)
annual_contribution_incr_pct = -inflation  # annual contribution decreases since more $ going into rent rather than investment
total_savings_invested, total_investment_gains, final_balance = investment_calculator(initial_deposit, monthly_contribution, annual_returns, investment_months, annual_contribution_incr_pct)

print(f'Flipping a house after {int(redemption_month/12)} yrs at a ${int(sticker_profit_from_home_sales/1000)}k profit would change your savings by ${int(actual_profit)}')
print(f'Renting for {int(redemption_month/12)} yrs would change your savings by -${int(total_rent_paid)}')
print(f'Investing the money that would otherwise go into said mortgage will make you ${int(final_balance)}')
print(f'So by renting, your balance would be ${int(final_balance-total_rent_paid)} vs buying balance ${int(actual_profit)}')





