#calculator.py
import numpy as np
import datetime as dt
import streamlit as st
import pandas as pd
import os, sys

st.set_page_config(page_title='Repayment Calculator',
                   layout="wide")

st.title('Repayment Calculator')
st.write('To only be used for customers pre-disbursement')

loan_amount = st.number_input('Loan Amount', min_value=10000, step=1000)

admin_fee = st.number_input('Admin Fee', min_value=0, value=0, step=100)

interest_rate = st.number_input('Interest Rate', min_value=0.00)

disbursement_date = st.date_input('Disbursement Date')

first_repayment_date = st.date_input('First Repayment Date')

term_select = st.multiselect('Select Terms', [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])
grace_period = round((first_repayment_date - disbursement_date).days/365.25*12)

grace_amount = np.fv(interest_rate/100/12, grace_period,0,loan_amount+admin_fee)

grace_amount = loan_amount*(1+(interest_rate/100/12)*grace_period) + admin_fee*(1+(interest_rate/100/12)*grace_period)
opening_balance = abs(round(grace_amount))
cols = ['Term', 'Opening Balance at Repayment', 'Monthly Repayment', 'Total Repayable Amount', 'Total Interest']
df_terms = pd.DataFrame(index=term_select, columns=cols)

for term in term_select:
    try:
        payment = np.pmt(interest_rate/100/12, term*12, abs(grace_amount))
        monthly_payment = abs(round(payment))
        total_payable = abs(round(payment))*term*12
        total_interest = abs((round(payment))*term*12) - loan_amount
        df_temp = pd.DataFrame([[str(term) + ' Years', opening_balance, monthly_payment, total_payable, total_interest]], columns=cols)
        df_terms = df_terms.append(df_temp)
    except OverflowError as overflow:
        total_payable = abs(round(grace_amount))
        total_interest = abs(round(grace_amount) - loan_amount)
        df_temp = pd.DataFrame([[str(term) + ' Years', opening_balance, 0, total_payable, total_interest]], columns=cols)
        df_terms = df_terms.append(df_temp)

if st.button('Generate'):
    st.dataframe(df_terms.groupby('Term').sum())
    st.write("Please note these are estimated amounts")
    st.balloons()