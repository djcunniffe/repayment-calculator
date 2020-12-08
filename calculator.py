#calculator.py
import numpy as np
import datetime as dt
import streamlit as st
import os, sys
import geckoboard

client = geckoboard.client(os.environ['GECKOBOARD_KEY'])
dataset = client.datasets.find_or_create('prototype.repayments_calculator', {
    'calculation' : {'type' : 'number', 'name' : 'Calculations', 'optional' : False}
})

st.title('Repayment Calculator')
st.write('To only be used for customers pre-disbursement')

loan_amount = st.number_input('Loan Amount', min_value=10000, step=1000)

admin_fee = st.number_input('Admin Fee', min_value=0, value=0, step=100)

interest_rate = st.number_input('Interest Rate', min_value=0.00)

disbursement_date = st.date_input('Disbursement Date')

first_repayment_date = st.date_input('First Repayment Date')

early_repayment = st.slider('Years to repay',min_value=0, max_value=20,value=7, step=1)

grace_period = round((first_repayment_date - disbursement_date).days/365.25*12)
st.write(grace_period + (early_repayment)*12)

grace_amount = np.fv(interest_rate/100/12, grace_period,0,loan_amount+admin_fee)

grace_amount = loan_amount*(1+(interest_rate/100/12)*grace_period) + admin_fee*(1+(interest_rate/100/12)*grace_period)
st.write('Grace Amount: ', abs(round(grace_amount)))

try:
    payment = np.pmt(interest_rate/100/12, early_repayment*12, abs(grace_amount))
    st.write('Monthly Repayment: ', abs(round(payment)))
    st.write('Total Repayable: ', abs(round(payment))*early_repayment*12)
except OverflowError as overflow:
    st.write('Total Repayable: ', abs(round(grace_amount)))

try:
    dataset.post([
    {'calculation' : 1}
    ])
except Exception as e:
    print(e)


