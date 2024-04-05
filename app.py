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

# Streamlit app
st.title('Model Prediction')

# Sidebar for input
st.sidebar.title('Input Features')

# Input feature
year = st.sidebar.number_input('Upcoming Financial Year', value=0.0)

# User inputs
user_salary = st.sidebar.number_input("Enter Salary")
user_expense = st.sidebar.number_input("Enter Expense")

# Button to make predictions
if st.sidebar.button('Predict'):
    # Make prediction
    user_data = np.array([[year]])  # Adjust input based on your model's requirements

    predic_inflation = model.predict(user_data)
    st.write('Inflation Prediction of Entered year:', predic_inflation[0])

    predic_salary = model_sal.predict(user_data)
    st.write('Salary Prediction:', predic_salary[0])

    predic_gold = model_gold.predict(user_data)
    st.write('Gold Prediction:', predic_gold[0])

    predic_bse = model_bse.predict(user_data)
    st.write('BSE Prediction:', predic_bse[0])

    # Function to calculate expected monthly income next year
    def expected_monthly_income_nextyear(current_income, income_increase_percentage):
        nextyear_income = current_income + (current_income * income_increase_percentage)
        return nextyear_income

    st.write("You entered:", user_salary)
    st.write('Expected Monthly Income', expected_monthly_income_nextyear(user_salary, predic_salary[0]))

    # Function to calculate expected monthly expenses next year
    def expected_monthly_expenses_nextyear(current_monthly_expense, inflation_percentage):
        nextyear_monthly_expense = current_monthly_expense + (current_monthly_expense * inflation_percentage)
        return nextyear_monthly_expense

    st.write("You entered:", user_expense)
    st.write('Expected Monthly Expense', expected_monthly_expenses_nextyear(user_expense, predic_inflation[0]))

def debt_repayment_plan(current_debt, years, interest_rate):
    # Calculate annual payment using annuity formula
    annual_payment = current_debt * (interest_rate / (1 - (1 + interest_rate) ** -years))

    remaining_debt = current_debt
    repayment_plan = []

    # Calculate repayment plan
    for year in range(1, years + 1):
        interest_payment = remaining_debt * interest_rate
        principal_payment = annual_payment - interest_payment
        remaining_debt -= principal_payment

        repayment_plan.append((year, principal_payment, interest_payment, remaining_debt))

    return repayment_plan


# Streamlit app
st.title('Debt Repayment Plan Calculator')

# Sidebar for input
st.sidebar.title('Input Features')

# Input features
user_debt = st.sidebar.number_input("Enter Current Debt")
user_years = st.sidebar.number_input("Enter Number of Years", min_value=1, step=1)
user_interest_rate = st.sidebar.number_input("Enter Current Interest Rate")

# Display user inputs
st.write("You entered:")
st.write(f"Current Debt: ₹{user_debt}")
st.write(f"Number of Years: {user_years}")
st.write(f"Interest Rate: {user_interest_rate}%")

# Button to calculate
if st.sidebar.button('Calculate Repayment Plan'):
    # Calculate repayment plan
    repayment_plan = debt_repayment_plan(user_debt, user_years, user_interest_rate / 100)  # Convert interest rate to decimal

    # Display the repayment plan per year
    st.write("Year\t\tPrincipal Payment\t\tInterest Payment\t\tRemaining Debt")
    for year, principal_payment, interest_payment, remaining_debt in repayment_plan:
        st.write(f"{year}\t\t₹{principal_payment:.2f}\t\t₹{interest_payment:.2f}\t\t₹{remaining_debt:.2f}")
        savings = (user_salary * 12) - ((user_expense * 12) + (principal_payment + interest_payment))
        st.write(f"Savings: ₹{savings:.2f}")

        # Make prediction for the year
        user_data = np.array([[year]])
        predic_gold = model_gold.predict(user_data)
        predic_bse = model_bse.predict(user_data)

        # Compare gold and BSE predictions and print recommendation
        if predic_gold[0] > predic_bse[0]:
            st.write("Recommendation: It's recommended to invest more in gold, since gold rates are higher in this financial year.")
        else:
            st.write("Recommendation: It's recommended to invest more in BSE, since returns in BSE are higher in this financial year.")
