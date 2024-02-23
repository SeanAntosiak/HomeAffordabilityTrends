import numpy as np
import pandas as pd
import streamlit as st 
import plotly.express as px

# import Dataframe 
DF = pd.read_csv('data/CleanData.csv')


line1 = px.line(DF, x='Year', y=['Median Home Price', 'Median Personal Income'])
line2 = px.line(DF, x='Year', y='Home Price/Income Ratio')
line2.add_annotation(text='Ratio of median home price to median personal income over time', xref='paper', yref='paper', x=0.5, y=1, showarrow=False)

line3 = px.line(DF, x='Year', y='Mortgage/Income Ratio')
line3.add_annotation(text='Ratio of mortgage payment to median monthly income over time', xref='paper', yref='paper', x=0.5, y=1.1, showarrow=False)

st.title('Home Affordability Since 1974')
TabOverview, TabCompare, TabData = st.tabs(['Overview','Compare', 'Data'])

with TabOverview:
    st.write('This app was created to explore historical trends in home affordibility from 1974 to 2022.') 
    st.write('To compare datapoints from two specific years go to the "compare" tab.')
    st.write('To check data sources go to the "data" tab.')
    st.markdown('---')

    st.write('To start I wanted to compare median personal income to median home price over time.')
    st.plotly_chart(line1)
    st.write('''This graph can be misleading because the widening gap between the lines might suggest decreasing affordability, which isn't necessarily the case.
             Since home prices significantly exceed annual salaries, a parallel growth rate would naturally expand the dollar amount gap over time. 
             A better trend to look at would be the ratio of home prices to income over time.
             ''')
 
    st.plotly_chart(line2)
    st.write('''This graph illustrates a more significant trend: in 1974, the median home price was equivalent to just under 7 years of median income. 
             By 2023, this number had escalated to more than 11 years. This underscores the increasing discrepancy between home prices and wages over time. 
             However, it's important to note that the majority of homebuyers do not save up to pay the full price in cash. Instead, most people rely on a mortgage to purchase a home. 
             Therefore, a more relevant measure to consider is the affordability of mortgage payments. 
             ''')
    st.markdown('---')
    
    st.write('''To achieve this, I utilized the standard mortgage formula for a 30-year fixed-rate loan to estimate the annual mortgage payment. 
             The median home price served as the principal amount, while the average mortgage rate for that year was used as the interest rate. 
             To obtain the monthly income, I divided the annual median income by 12. With these figures, I calculated a ratio for each year and plotted the results below.
             ''')
    st.plotly_chart(line3)
    st.write('This trend actually suprised me. Even thoughout the pandemic, mortgage payments appeared to be more affordable than they historically have been.') 
    st.markdown('---')         
    st.write('''It is important to note that this analysis assumes no down payment is made and excludes mortgage insurance and property taxes from consideration. A full analysis of home affordability
             would need to include these factors as well as cost of living, income tax rates, time to save up a down payment, and many others variables that are outside the scope of this project. 
             ''')
            

# formating dataframe for display in app
DF['Year'] = DF['Year'].astype(str)
DF['Median Personal Income'] = DF['Median Personal Income'].astype(int).apply(lambda x: f'${x:,}')
DF['Median Home Price'] = DF['Median Home Price'].astype(int).apply(lambda x: f'${x:,}')
DF['Average Mortgage Rate'] = DF['Average Mortgage Rate'].round(2).apply(lambda x: f'{x} %')
DF['Home Price/Income Ratio'] = DF['Home Price/Income Ratio'].round(2)
DF['Mortgage/Income Ratio'] = DF['Mortgage/Income Ratio'].round(2)
DF['30YR Mortgage Payment'] = DF['30YR Mortgage Payment'].round(2).apply(lambda x: f'${x:,}')
DF['Monthly Gross Income'] = DF['Monthly Gross Income'].round(2).apply(lambda x: f'${x:,}')

with TabCompare:
    st.write('Choose two years to compare')
    Year1, Year2 = st.columns(2)
      

    with Year1:
        Year1Input = st.selectbox('Select first Year', DF['Year'], key='year1')
        Year1DF = DF[DF['Year'] == Year1Input].T
        st.table(Year1DF)



    with Year2:
        Year2Input = st.selectbox('Select second Year', DF['Year'], key='year2', index=48)
        Year2DF = DF[DF['Year'] == Year2Input].T
        st.table(Year2DF)

    st.write('''DISCLAIMERS:''') 
    st.write('Mortage rates change constatly throughout the year, but have been averaged to give one value for each year')       
    st.write('''The 30YR mortgage payment is based off the standard mortage formula using that years average mortgage rate and average median home price as the principal value.
              It does not include property tax or mortgage insurance''') 
  

with TabData:
    st.markdown('Mortgage rate data from [Macrotrends.net](https://www.macrotrends.net/2604/30-year-fixed-mortgage-rate-chart)')
    st.markdown('Median personal income data from [St. Louis FED](https://fred.stlouisfed.org/series/MEPAINUSA646N)')
    st.markdown('Median home price from [St. Louis FED](https://fred.stlouisfed.org/series/MSPNHSUS)')