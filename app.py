import streamlit as st
import numpy as np
import pickle

# Load models
with open('inflation_precit.pkl', 'rb') as model_file_inflation:
    model = pickle.load(model_file_inflation)

with open('sallary.pkl', 'rb') as model_file_salary:
    model_sal = pickle.load(model_file_salary)

with open('gold.pkl', 'rb') as model_file_gold:
    model_gold = pickle.load(model_file_gold)

with open('bse.pkl', 'rb') as model_file_bse:
    model_bse = pickle.load(model_file_bse)

# Function to calculate expected monthly income next year
def expected_monthly_income_nextyear(current_income, income_increase_percentage):
    nextyear_income = current_income + (current_income * income_increase_percentage)
    return nextyear_income

# Function to calculate expected monthly expenses next year
def expected_monthly_expenses_nextyear(current_monthly_expense, inflation_percentage):
    nextyear_monthly_expense = current_monthly_expense + (current_monthly_expense * inflation_percentage)
    return nextyear_monthly_expense

def debt_repayment_plan(current_debt, years, interest_rate, starting_year):
    # Calculate annual payment using annuity formula
    annual_payment = current_debt * (interest_rate / (1 - (1 + interest_rate) ** -years))

    remaining_debt = current_debt
    repayment_plan = []

    # Calculate repayment plan
    for year in range(starting_year, starting_year + years):
        interest_payment = remaining_debt * interest_rate
        principal_payment = annual_payment - interest_payment
        remaining_debt -= principal_payment

        repayment_plan.append((year, principal_payment, interest_payment, remaining_debt))

    return repayment_plan

# Streamlit app
st.title('Buri Buri Finance App')
st.markdown("---")

# Sidebar for input
st.sidebar.title('Input Features')

# Input feature
starting_year = st.sidebar.number_input('Enter Financial Year', value=2025)
year = starting_year

# User inputs
user_salary = st.sidebar.number_input("Enter Current Salary")
user_expense = st.sidebar.number_input("Enter Current Expense")

# Button to make predictions
if st.sidebar.button('Predict'):
    # Make prediction
    user_data = np.array([[year]])  # Adjust input based on your model's requirements

    predic_inflation = model.predict(user_data)
    st.write('Predicted Inflation of Entered year:', predic_inflation[0][0]*100)

    predic_salary = model_sal.predict(user_data)
    st.write('Predicted Percentage Salary Increase:', predic_salary[0][0]*100)

    predic_gold = model_gold.predict(user_data)
    st.write('Predicted Gold Returns:', predic_gold[0][0]*100)

    predic_bse = model_bse.predict(user_data)
    st.write('Predicted BSE Returns:', predic_bse[0][0]*100)

    st.markdown("---")
    st.subheader('Expected Financial Outlook for Next Year')
    st.write(f'Expected Monthly Income: ₹{expected_monthly_income_nextyear(user_salary, predic_salary[0][0]):,.2f}')
    st.write(f'Expected Monthly Expense: ₹{expected_monthly_expenses_nextyear(user_expense, predic_inflation[0][0]):,.2f}')
    st.markdown("---")

# Streamlit app for debt repayment
st.sidebar.title('Debt Repayment Plan')

# Input features
user_debt = st.sidebar.number_input("Enter Current Debt")
user_years = st.sidebar.number_input("Enter Number of Years", min_value=1, step=1)
user_interest_rate = st.sidebar.number_input("Enter Current Interest Rate")

# Button to calculate
if st.sidebar.button('Calculate Repayment Plan'):
    # Calculate repayment plan
    repayment_plan = debt_repayment_plan(user_debt, user_years, user_interest_rate / 100, starting_year)

    # Display the repayment plan per year in tabular form
    st.subheader("Debt Repayment Plan")
    table_data = [["Year", "Principal Payment", "Interest Payment", "Remaining Debt", "Savings", "Recommendation"]]
    for year, principal_payment, interest_payment, remaining_debt in repayment_plan:
        savings = (user_salary * 12) - ((user_expense * 12) + (principal_payment + interest_payment))

        # Make prediction for the year
        user_data = np.array([[year]])
        predic_gold = model_gold.predict(user_data)
        predic_bse = model_bse.predict(user_data)

        # Determine recommendation
        recommendation = ""
        if predic_gold[0][0] > predic_bse[0][0]:
            recommendation = "It's recommended to invest more in gold, since gold rates are higher in this financial year. "
        else:
            recommendation = "It's recommended to invest more in BSE, since returns in BSE are higher in this financial year."

        table_data.append([f"{year}", f"₹{principal_payment:.2f}", f"₹{interest_payment:.2f}", f"₹{remaining_debt:.2f}", f"₹{savings:.2f}", recommendation])

    # Display table
    st.table(table_data)
