import streamlit as st
import pandas as pd
import datetime as dt
import plotly.express as px

if 'expenses' not in st.session_state:
    st.session_state.expenses = []

if 'income' not in st.session_state:
    st.session_state.income = 0

if 'savings_goal' not in st.session_state:
    st.session_state.savings_goal = 0

st.sidebar.title("Setup Budget")
st.sidebar.write("Hello student! Set your income and savings goals.")
st.sidebar.markdown("---")

st.sidebar.text_input("Enter Your Name", key="user_name")
income = st.sidebar.number_input("Monthly Income (₹)", min_value=0, step=100)
savings_goal = st.sidebar.number_input("Monthly Savings Goal (₹)", min_value=0, step=100)

st.session_state.income = income
st.session_state.savings_goal = savings_goal

st.title("Daily Expense Tracker for Students")

st.subheader("Log a New Expense")

category = st.selectbox("Select Expense Category", ["Food", "Travel", "Books", "Entertainment", "Others"])
amount = st.number_input("Enter Expense Amount (₹)", min_value=0.0, step=1.0, format="%.2f")
date = st.date_input("Select Expense Date", value=dt.date.today())
log_button = st.button("Add Expense")

if log_button and amount > 0:
    new_expense = {"Date": date, "Category": category, "Amount": amount}
    st.session_state.expenses.append(new_expense)
    st.success("Expense logged successfully!")

df = pd.DataFrame(st.session_state.expenses)

if not df.empty:
    st.subheader("Expense Table")
    st.dataframe(df, use_container_width=True)

    total_spent = df["Amount"].sum()
    balance = income - total_spent
    remaining_after_savings = income - savings_goal - total_spent

    st.markdown(f"**Total Spent:** ₹{total_spent:.2f}")
    st.markdown(f"**Balance Left:** ₹{balance:.2f}")
    st.markdown(f"**Remaining After Savings Goal:** ₹{remaining_after_savings:.2f}")

    if total_spent > income:
        st.error("You have overspent your monthly income!")
    elif total_spent > (income - savings_goal):
        st.warning("You're exceeding your savings goal!")
    else:
        st.success("You're within your budget goals!")

    st.subheader("Visualize Spending")

    pie_data = df.groupby("Category")["Amount"].sum().reset_index()
    pie_chart = px.pie(pie_data, names="Category", values="Amount", title="Spending by Category")
    st.plotly_chart(pie_chart, use_container_width=True)

    bar_chart = px.bar(pie_data, x="Category", y="Amount", title="Amount Spent per Category", color="Category")
    st.plotly_chart(bar_chart, use_container_width=True)

    st.subheader("Export Data")
    weekly_df = df[df["Date"] >= dt.date.today() - dt.timedelta(days=7)]
    csv = weekly_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download This Week's Data as CSV",
        data=csv,
        file_name='weekly_expenses.csv',
        mime='text/csv',
    )

else:
    st.info("Log your first expense to begin tracking.")
