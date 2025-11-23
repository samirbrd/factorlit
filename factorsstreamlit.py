# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 15:50:19 2020

@author: Administrator
"""


import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image

st.title('Factor Returns and Selections')
st.write('For Investors who want to invest in markets with factor tilts')
path_string_1="./Factor Backtests/"
path_string_2="./Factor Backtests/Low Vol/"
path_string_3="./Factor Selections/"
df_date=pd.read_csv(path_string_3+'updated_till.csv')
updated_till=df_date['Date'].loc[0]
st.write('Updated till'+' '+updated_till)
dir_1={'High Alpha':'alpha','Low Vol':'vol','Low Beta':'beta','Low iVol':'ivol','High Momentum':'momentum'}
dir_2={'NSE50':'2704','NSE200':'3385','NSE500':'3386','ex Index':'0'}



add_selectbox_1 = st.sidebar.selectbox(
    'Strategy',
    ('High Alpha','Low Vol','Low Beta','Low iVol','High Momentum')
)
add_selectbox_2 = st.sidebar.selectbox(
    'Benchmark',
    ('NSE50','NSE200','NSE500','ex Index')
)
add_selectbox_3 = st.sidebar.selectbox(
    'Lookback Days',
    ('180','270','365')
)
add_selectbox_8 = st.sidebar.selectbox(
    'Rebalancing Days',
    ('30','90','180','270','365')
)
add_selectbox_4 = st.sidebar.selectbox(
    'No of Stocks Selected',
    ('5','10','15','20','25','30')
)
add_selectbox_5 = st.sidebar.selectbox(
    'Type of Weighting',
    ('Equal Weight','Factor Weight')
)
add_selectbox_6 = st.sidebar.selectbox(
    'Amount to be Invested',
    ('500000','750000','1000000','1500000','2000000','2500000')
)
add_selectbox_7 = st.sidebar.selectbox(
    'Display Trades?',
    ('YES','NO')
)

file_string_1=path_string_3+dir_2.get(add_selectbox_2)+add_selectbox_3+dir_1.get(add_selectbox_1)+'.csv'
df_factor=pd.read_csv(file_string_1)
print(df_factor)
#In df_factor, delete the first column
df_factor.drop(df_factor.columns[0], axis=1, inplace=True)
df_factor.drop(columns=['Factor'],inplace=True)
#rename column 'Selection Close' to 'Close'
df_factor.rename(columns={'Selection Close':'Close'},inplace=True)
df_factor_selection=df_factor.head(int(add_selectbox_4))
if add_selectbox_5=='Equal Weight':
    df_factor_selection['Quantity']=np.ceil((int(add_selectbox_6)/int(add_selectbox_4))/df_factor_selection['Close'])
if add_selectbox_5=='Factor Weight':
    min_weight=2
    max_weight=5
    factor=(max_weight-min_weight)/int(add_selectbox_4)
    weights=[]
    b=max_weight
    while b>=min_weight: 
        weights.append(b)
        b=b-factor
    if len(weights)>int(add_selectbox_4):         
        weights=weights[:-1]
    df_factor_selection['Weight']=weights
    df_factor_selection['Weight']=df_factor_selection['Weight']/df_factor_selection['Weight'].sum()
    #df_factor_selection['Quantity']=np.ceil(df_factor_selection['Weight']*int(add_selectbox_6)/df_factor_selection['Close'])
    df_factor_selection.drop(columns=['Weight'],inplace=True)
st.write(df_factor_selection)
image_string=path_string_1+add_selectbox_1+'/'+add_selectbox_2+' '+add_selectbox_1+' '+add_selectbox_4+' Stocks '+add_selectbox_5+' '+add_selectbox_3+' Days Look Back '+add_selectbox_8+' Rebalancing Days Long Strategy Only.jpg'
data_string=path_string_1+add_selectbox_1+'/'+add_selectbox_2+' '+add_selectbox_1+' '+add_selectbox_4+' Stocks '+add_selectbox_5+' '+add_selectbox_3+' Days Look Back '+add_selectbox_8+' Rebalancing Days Long Strategy Only.csv'
index_string=path_string_1+add_selectbox_1+'/'+add_selectbox_2+'.csv'
st.header('Backtest Results')
try:
    image=Image.open(image_string)
    st.image(image)
    df_data=pd.read_csv(data_string)
    df_data.drop(columns=['Unnamed: 0'],inplace=True)
    st.header('Strategy Backtest Returns')
    st.write(df_data)
    df_index=pd.read_csv(index_string)
    df_index.drop(columns=['Unnamed: 0'],inplace=True)
    st.header('Benchmark Backtest Returns')
    st.write(df_index)
except:
    st.write('Backtest Data Not Available. Not enough or too much diversification for index size')

if add_selectbox_7=='YES':
    data_string_trades=path_string_1+add_selectbox_1+'/'+add_selectbox_2+' '+add_selectbox_1+' '+add_selectbox_4+' Stocks '+add_selectbox_5+' '+add_selectbox_3+' Days Look Back '+add_selectbox_8+' Rebalancing Days Long Strategy Onlydetails.csv'
    try:
        st.header('Backtest Trade Details')
        df_data_trades=pd.read_csv(data_string_trades)
        df_data_trades.drop(columns=['Unnamed: 0'],inplace=True)
        st.write(df_data_trades)
    except:
        st.write('Backtest Trade Details Not Available')



disclaimer='This does not constitute investment advice. Only for educational purposes'
ownership='Samir Shah,samirbrd@gmail.com'
st.write(disclaimer)

st.write(ownership)


