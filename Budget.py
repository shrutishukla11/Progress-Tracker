import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import helper

from datetime import date

today = date.today()
# noinspection PyBroadException
try:
    income_data = pd.read_excel('income_data.xlsx')
    expenses = pd.read_excel('expense_data.xlsx')

    expenses = helper.clean_df(expenses)
    income_data = helper.clean_df(income_data)
except Exception as e:
    income_data = pd.DataFrame(columns=['source', 'amount', 'date'])
    expenses = pd.DataFrame(columns=['product', 'expended', 'date'])
tabs = st.tabs(['This Month', 'Monthly Data'])
with tabs[0]:
    with st.sidebar:
        save = st.slider('Set savings: ', value=30, min_value=0, max_value=100, step=5)
        with st.expander('Add income: '):
            # noinspection PyBroadException
            try:
                source = st.text_input('Source of income: ')
                income = int(st.text_input('Amount: '))

            except Exception as e:
                pass
            if st.button('Add Income'):
                # noinspection PyBroadException
                try:
                    income_data.loc[len(income_data.index)] = [source, income, today]
                    income_data.to_excel('income_data.xlsx')
                    expenses.to_excel('expense_data.xlsx')
                except Exception as e:
                    st.error('Something went wrong refresh the page')
        with st.expander('Add expense :'):

            # noinspection PyBroadException
            try:
                product = st.text_input('Product/Service: ')
                expended = int(st.text_input('Amount: ', key=1))

            except Exception as e:
                pass
            if st.button('Add Expense'):
                expenses.loc[len(expenses.index)] = [product, expended, today]
                income_data.to_excel('income_data.xlsx')
                expenses.to_excel('expense_data.xlsx')

    # Display this months data
    st.header(today.strftime("%B"))
    income_data = helper.budget_dates(income_data)
    expenses = helper.budget_dates(expenses)
    expenses = helper.drop_previous_year(expenses)
    income_data = helper.drop_previous_year(income_data)
    display_income = helper.get_this_month(income_data)
    display_expense = helper.get_this_month(expenses)
    # Start Displaying data according to time selected
    general_data, pie_chart = st.columns(2)
    try:
        display_total_income = sum([x for x in display_income['amount']])
        display_total_expense = sum([x for x in display_expense['expended']])
        display_total_budget_left = display_total_income - display_total_expense - (display_total_income * (save / 100))
    except Exception as e:
        st.write('Error in income or expense data')

    with general_data:
        st.success(f'Income: {display_total_income}')
        st.error(f'Expenses: {display_total_expense}')
        st.info(f'Remaining Budget: {int(display_total_budget_left)}')
    with pie_chart:
        if display_total_budget_left >= 0 and display_income.shape[0] !=0 and display_expense.shape[0]!=0:

            fig, ax = plt.subplots()
            ax.pie([display_total_income, display_total_expense, display_total_budget_left],
                   labels=['Income', 'Expense', 'Remaining budget'],
                   colors=['hotPink', 'cyan', 'red'],
                   explode=[0, 0, 0.2],
                   shadow=True)
            st.pyplot(fig)
        elif display_income.shape[0] !=0 and display_expense.shape[0]!=0:

            st.error('Expenses extended the budget value')
            fig, ax = plt.subplots()
            ax.pie([display_total_income, display_total_expense],
                   labels=['Income', 'Expense'],
                   colors=['hotPink', 'cyan'],
                   shadow=True)
            st.pyplot(fig)
        elif display_income.shape[0] != 0:
            fig, ax = plt.subplots()
            ax.pie([display_total_income, display_total_expense],
                   labels=['Income'],
                   colors=['hotPink'],
                   shadow=True)
            st.pyplot(fig)

    # DISPLAY THE RECENT INCOME

    with st.expander('View recent income'):
        colA, colB = st.columns(2)
        with colA:
            st.subheader('Total Income: ')
        with colB:
            st.subheader(str(sum([x for x in income_data['amount']])))

        with colA:
            st.subheader('Source')
        with colB:
            st.subheader('Amount')

        if income_data.shape[0] > 3:
            for i in range(income_data.shape[0] - 1, income_data.shape[0] - 4, -1):
                with colA:
                    st.write(str(income_data['source'][i]))
                with colB:
                    st.write(str(income_data['amount'][i]))
        elif income_data.shape[0] <= 3:
            for i in range(income_data.shape[0]):
                with colA:
                    st.write(str(income_data['source'][i]))
                with colB:
                    st.write(str(income_data['amount'][i]))
        elif income_data.shape[0] == 0:
            st.write('No income yet')
    with st.expander('View recent expenses'):
        # DISPLAY RECENT EXPENSES
        colC, colD = st.columns(2)
        with colC:
            st.subheader("Total Expense :")
        with colD:
            st.subheader(str(sum([x for x in expenses['expended']])))

        with colC:
            st.subheader('Product')
        with colD:
            st.subheader('Amount')

        if expenses.shape[0] > 0:
            for i in range(expenses.shape[0] - 1, expenses.shape[0] - 4, -1):
                with colC:
                    st.write(str(expenses['product'][i]))
                with colD:
                    st.write(str(expenses['expended'][i]))
        elif expenses.shape[0] == 0:
            st.write('No expense yet')

with tabs[1]:
    income_data = helper.budget_dates(income_data)
    expenses = helper.budget_dates(expenses)
    expenses = helper.drop_previous_year(expenses)
    months_list = ['Whole Year', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
                   'October', 'November', 'December']
    choice = st.selectbox('Select Month: ', months_list)
    income_data = helper.drop_previous_year(income_data)
    if choice == 'Whole Year':
        display_expense = expenses
        display_income = income_data
    else:
        display_expense = expenses.loc[expenses['month'] == choice]
        display_income = income_data.loc[income_data['month'] == choice]

    # Start Displaying data according to time selected
    general_data, pie_chart = st.columns(2)
    display_total_income = sum([x for x in display_income['amount']])
    display_total_expense = sum([x for x in display_expense['expended']])
    display_total_budget_left = display_total_income - display_total_expense - (display_total_income * (save / 100))

    with general_data:
        st.success(f'Income: {display_total_income}')
        st.error(f'Expenses: {display_total_expense}')
        st.info(f'Remaining Budget: {int(display_total_budget_left)}')
    with pie_chart:
        if display_total_budget_left >= 0 and display_income.shape[0] !=0 and display_expense.shape[0]!=0:

            fig, ax = plt.subplots()
            ax.pie([display_total_income, display_total_expense, display_total_budget_left],
                   labels=['Income', 'Expense', 'Remaining budget'],
                   colors=['hotPink', 'cyan', 'red'],
                   explode=[0, 0, 0.2],
                   shadow=True)
            st.pyplot(fig)
        elif display_income.shape[0] !=0 and display_expense.shape[0]!=0:
            st.error('Expenses extended the budget value')
            fig, ax = plt.subplots()
            ax.pie([display_total_income, display_total_expense],
                   labels=['Income', 'Expense'],
                   colors=['hotPink', 'cyan'],
                   shadow=True)
            st.pyplot(fig)
        elif display_income.shape[0] !=0 :
            fig, ax = plt.subplots()
            ax.pie([display_total_income, display_total_expense],
                   labels=['Income'],
                   colors=['hotPink'],
                   shadow=True)
            st.pyplot(fig)
        else:
            st.write("You haven't started this Month")

    with st.expander('All Income:'):
        col1,col2 = st.columns(2)
        if display_income.shape[0]!=0:
            for i in range(display_income.shape[0]):
                with col1:
                    st.write(str(display_income['source'][i]))
                with col2:
                    st.write(str(display_income['amount'][i]))
        else:
            st.write('No income yet')
    with st.expander('All expenses:'):
        col3, col4 = st.columns(2)
        if display_expense.shape[0] != 0:
            for i in range(expenses.shape[0]):
                with col3:
                    st.write(str(display_expense['product'][i]))
                with col4:
                    st.write(str(display_expense['expended'][i]))
        else:
            st.write('No expenses yet')


