import os
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime
from datetime import timedelta
import numpy as np
import pandas as pd
import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator


from app_utility import settings
from app_utility import company_valuation as cv
from app_utility import stock_time_series as sts

from matplotlib.font_manager import FontProperties
fontP = FontProperties()
fontP.set_size('small')

today = datetime.today()
todaystr = today.strftime("%Y-%m-%d")
ten_years_ago = datetime.today() - timedelta(days=10*365)
ten_years_ago_str = ten_years_ago.strftime("%Y-%m-%d")

years = mdates.YearLocator()   # every year
months = mdates.MonthLocator()  # every month
years_fmt = mdates.DateFormatter('%Y')


st.title('Fundamentals')

st.sidebar.title("Setup")
api_key = st.sidebar.text_input('FMPCLOUD Key', os.environ['fmp_key'], type="password")
settings.set_apikey(api_key)

symbol_search = st.sidebar.text_input('Symbol', 'AMZN')
#df_ticker = sts.ticker_search(match = symbol_search)

#scroll_list = list(df_ticker.name.values)
#scroll_list.append(symbol_search)

#selected = st.sidebar.selectbox('symbols found', scroll_list)

if st.sidebar.button("Start"):

    try:
        symbol = symbol_search
        #df_ticker.loc[df_ticker['name'] == selected,'symbol'][0]

        st.write('showing results for:', symbol)

        # get historical prices
        df_prices_ = sts.historical_stock_data(symbol, dailytype = 'line', start = ten_years_ago_str, end =todaystr)
        df_prices = df_prices_.reset_index()
        # get financial ratios
        df_ratios = cv.financial_ratios(ticker=symbol,period='annual',ttm = False)
        # get performance metrics
        df_metrics = cv.key_metrics(ticker =symbol, period = 'annual')
        # get income statement
        df_income = cv.income_statement(ticker = symbol, period = 'annual', ftype = 'full')
        # get cashflow statement
        df_cashflow = cv.cash_flow_statement(ticker = symbol, period = 'annual', ftype = 'full')
        # get discounted cash_flow_statement
        df_dcf = cv.dcf(ticker = symbol, history = 'annual')

    except:
        st.write("Stock data unavailable!")


st.header('Quote')

try:

    fig, ax = plt.subplots()
    ax.plot(list(df_prices.date.values), list(df_prices.close.values))

    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_major_formatter(years_fmt)
    st.pyplot(fig)
except:
    st.write("Prices data unavailable!")

#------------------------------------------------------------------------------#
st.header('Ratios')

try:
    st.markdown("**Price To Book Ratio**")
    st.write("It is calculated by dividing the company's stock price per share by its book value per share (BVPS). An asset's book value is equal to its carrying value on the balance sheet, and companies calculate it netting the asset against its accumulated depreciation.")
    st.markdown(str(round(df_ratios.loc[0,'priceToBookRatio'],2)))

    st.markdown("**Price To Sales Ratio**")
    st.write("The P/S ratio can be calculated either by dividing the company’s market capitalization by its total sales over a designated period – usually twelve months, or on a per-share basis by dividing the stock price by sales per share. The P/S ratio is also known as a sales multiple or revenue multiple.")
    st.markdown(str(round(df_ratios.loc[0,'priceToSalesRatio'],2)))

    st.markdown("**Price To Earnings Ratio**")
    st.write("The price-to-earnings ratio (P/E ratio) is the ratio for valuing a company that measures its current share price relative to its per-share earnings (EPS). The price-to-earnings ratio is also sometimes known as the price multiple or the earnings multiple.")
    st.markdown(str(round(df_ratios.loc[0,'priceEarningsRatio'],2)))

    df_ratios['date'] = pd.to_datetime(df_ratios.date)

    fig, ax = plt.subplots()
    plt.plot(list(df_ratios.date.dt.year), list(df_ratios.priceToBookRatio.values), marker='o', label='P/B')
    plt.plot(list(df_ratios.date.dt.year), list(df_ratios.priceToSalesRatio.values), marker='o', label='P/S')
    plt.plot(list(df_ratios.date.dt.year), list(df_ratios.priceEarningsRatio.values), marker='o', label='P/E')

    #ax.xaxis.set_major_locator(years)
    #ax.xaxis.set_major_formatter(years_fmt)
    plt.legend(loc='upper left')
    st.pyplot(fig)

except:
    st.write("Fundamental Ratios data unavailable!")

#------------------------------------------------------------------------------#

st.header('Profitability Ratios')

#try:
st.markdown("**Gross Margin**")
st.write("It is a company's net sales revenue minus its cost of goods sold (COGS). In other words, it is the sales revenue a company retains after incurring the direct costs associated with producing the goods it sells, and the services it provides.")
st.markdown(str(round(df_ratios.loc[0,'grossProfitMargin']*100,2))+"%")

st.markdown("**Operating Margin**")
st.write("It measures how much profit a company makes on a dollar of sales, after paying for variable costs of production, such as wages and raw materials, but before paying interest or tax. It is calculated by dividing a company’s operating profit by its net sales.")
st.markdown(str(round(df_ratios.loc[0,'operatingProfitMargin']*100,2))+"%")

st.markdown("**Net Margin**")
st.write("It is equal to how much net income or profit is generated as a percentage of revenue. Net profit margin is the ratio of net profits to revenues for a company or business segment. Net profit margin is typically expressed as a percentage but can also be represented in decimal form. The net profit margin illustrates how much of each dollar in revenue collected by a company translates into profit.")
st.markdown(str(round(df_ratios.loc[0,'netProfitMargin']*100,2))+"%")

fig, ax = plt.subplots()
plt.plot(list(df_ratios.date.values), list(df_ratios.grossProfitMargin.values), marker='o', label='Gross')
plt.plot(list(df_ratios.date.values), list(df_ratios.operatingProfitMargin.values), marker='o', label='Operating')
plt.plot(list(df_ratios.date.values), list(df_ratios.netProfitMargin.values), marker='o', label='Net')
ax.xaxis.set_major_locator(years)
ax.xaxis.set_major_formatter(years_fmt)
plt.legend(loc='upper left')
st.pyplot(fig)

st.markdown("**Return on Assets**")
st.write("It is an indicator of how profitable a company is relative to its total assets. ROA is calculated by dividing a company’s net income by total assets.")
st.markdown(round(df_ratios.loc[0,'returnOnAssets']*100,2))

st.markdown("**Return on Equity**")
st.write("It is a measure of financial performance calculated by dividing net income by shareholders' equity. Because shareholders' equity is equal to a company’s assets minus its debt, ROE is considered the return on net assets.")
st.markdown(round(df_ratios.loc[0,'returnOnEquity']*100,2))

st.markdown("**Return on Capital Employed**")
st.write("It is a financial ratio that measures a company's profitability and the efficiency with which its capital is used. In other words, the ratio measures how well a company is generating profits from its capital. ")
st.markdown(round(df_ratios.loc[0,'returnOnCapitalEmployed']*100,2))

fig, ax = plt.subplots()
plt.plot(list(df_ratios.date.values), list(df_ratios.returnOnAssets.values), marker='o',  label='Return on Assets', )
plt.plot(list(df_ratios.date.values), list(df_ratios.returnOnEquity.values), marker='o', label='Return on Equity', )
plt.plot(list(df_ratios.date.values), list(df_ratios.returnOnCapitalEmployed.values), marker='o', label='Return on Capital Employed', )
ax.xaxis.set_major_locator(years)
ax.xaxis.set_major_formatter(years_fmt)
plt.legend(loc='upper left')

st.pyplot(fig)

#except:
#    st.write("Profitability ratios data unavailable!")

#------------------------------------------------------------------------------#
st.header('Performance Metrics')

try:
    st.markdown("**Revenue per Share**")
    st.write("Sales per share is a ratio that computes the total revenue earned per share \
    over a designated period, whether quarterly, semi-annually, annually, or trailing \
    twelve months (TTM). It is calculated by dividing total revenue by average shares outstanding.")
    st.markdown(round(df_metrics.loc[0,'revenuePerShare'],2))

    st.markdown("**Debt to Equity**")
    st.write("It is calculated by dividing a company’s total liabilities by \
    its shareholder equity. These numbers are available on the balance sheet of \
    a company’s financial statements. It is a measure of the degree to which \
    a company is financing its operations through debt versus wholly-owned funds. \
    More specifically, it reflects the ability of shareholder equity to cover \
    all outstanding debts in the event of a business downturn.")
    st.markdown(round(df_metrics.loc[0,'debtToEquity'],2))

    st.markdown("**Current Ratio**")
    st.write("It is a liquidity ratio that measures a company's ability to pay short-term \
    obligations or those due within one year. The current ratio is sometimes referred \
    to as the “working capital” ratio and helps investors understand more \
    about a company’s ability to cover its short-term debt with its current assets.")
    st.markdown(round(df_metrics.loc[0,'currentRatio'],2))

    st.markdown("**Interest Coverage**")
    st.write("It is a debt ratio and profitability ratio used to determine how easily \
    a company can pay interest on its outstanding debt. The interest coverage ratio \
    may be calculated by dividing a company's earnings before interest and \
    taxes (EBIT) during a given period by the company's interest payments due within the same period.")
    st.markdown(round(df_metrics.loc[0,'interestCoverage'],2))

    df_metrics['date'] = pd.to_datetime(df_metrics.date)

    fig, ax = plt.subplots()

    plt.subplot(411)
    plt.plot(list(df_metrics.date.dt.year), list(df_metrics.revenuePerShare.values), marker='o',  label='Revenue per Share', )
    plt.tick_params(axis='x', which='both',bottom=False, top=False, labelbottom=False)
    plt.legend(loc='upper left')

    plt.subplot(412)
    plt.plot(list(df_metrics.date.dt.year), list(df_metrics.debtToEquity.values), marker='o',  label='Debt To Equity', )
    plt.tick_params(axis='x', which='both',bottom=False, top=False, labelbottom=False)
    plt.legend(loc='upper left')


    plt.subplot(413)
    plt.plot(list(df_metrics.date.dt.year), list(df_metrics.currentRatio.values), marker='o',  label='Current ratio', )
    plt.tick_params(axis='x', which='both',bottom=False, top=False, labelbottom=False)
    plt.legend(loc='upper left')

    plt.subplot(414)
    plt.plot(list(df_metrics.date.dt.year), list(df_metrics.interestCoverage.values), marker='o',  label='Interest Coverage', )
    plt.legend(loc='upper left')
    ax.minorticks_off()

    st.pyplot(fig)

except:
    st.write("Performance metrics data unavailable!")

#------------------------------------------------------------------------------#
st.header('Income Statement (Annual)')

try:
    df_income.drop(['link', 'finalLink'], axis=1, inplace=True)
    df_income.replace(0, method='bfill', inplace=True)

    st.markdown("**Cost of Revenue**")
    st.write("It is the total cost of manufacturing and delivering a product or service to consumers. \
    Cost of revenue information is found in a company's income statement and is designed \
    to represent the direct costs associated with the goods and services the company provides.")
    st.markdown(str(round(df_income.loc[0,'costOfRevenue']/float(1e9),2)) +" billions")

    st.markdown("**Operating Expense**")
    st.write("It is an expense a business incurs through its normal business operations. \
    Often abbreviated as OPEX, operating expenses include rent, equipment, inventory costs, \
    marketing, payroll, insurance, step costs, and funds allocated for research and development.")
    st.markdown(str(round(df_income.loc[0,'operatingExpenses']/float(1e9),2)) + " billions")

    st.markdown("**Interest Expense**")
    st.write("It is the cost incurred by an entity for borrowed funds. \
    Interest expense is a non-operating expense shown on the income statement. \
    It represents interest payable on any borrowings – bonds, loans, convertible \
    debt or lines of credit. Interest expense on the income statement represents \
    interest accrued during the period covered by the financial statements, \
    and not the amount of interest paid over that period.")
    st.markdown(str(round(df_income.loc[0,'interestExpense']/float(1e9),2)) + " billions")

    st.markdown("**Tax Expense**")
    st.write("It  is a liability owed to federal, state/provincial, and/or municipal governments within a given period, typically over the course of a year.")
    st.markdown(str(round(df_income.loc[0,'incomeTaxExpense']/float(1e9),2)) + " billions")

    st.markdown("**Other Expense**")
    st.markdown(str(round(df_income.loc[0,'otherExpenses']/float(1e9),2)) + " billions")

    st.markdown("**Net Income**")
    st.write("Net income after taxes (NIAT) is the net income of a business less all taxes. \
    In other words, NIAT is the sum of all revenues generated from the sale of the company's \
    products and services minus the costs to run it.")
    st.markdown(str(round(df_income.loc[0,'netIncome']/float(1e9),2)) + " billions")


    totals = [i+j+k+l+m+n for i,j,k,l,m,n in zip(df_income['costOfRevenue'],
                                                df_income['operatingExpenses'],
                                                df_income['interestExpense'],
                                                df_income['incomeTaxExpense'],
                                                df_income['otherExpenses'],
                                                df_income['netIncome'])]

    try:
        # From raw value to percentage
        cost = [i / j * 100 for i,j in zip(df_income['costOfRevenue'], totals)]
        operating = [i / j * 100 for i,j in zip(df_income['operatingExpenses'], totals)]
        interest = [i / j * 100 for i,j in zip(df_income['interestExpense'], totals)]
        tax = [i / j * 100 for i,j in zip(df_income['incomeTaxExpense'], totals)]
        other = [i / j * 100 for i,j in zip(df_income['otherExpenses'], totals)]
        net = [i / j * 100 for i,j in zip(df_income['netIncome'], totals)]

        fig, ax = plt.subplots()
        plt.bar(df_income['date'].dt.year, cost, edgecolor='white', label='Cost of Revenue')
        plt.bar(df_income['date'].dt.year, operating, bottom=cost, edgecolor='white', label='Operating Expense')
        plt.bar(df_income['date'].dt.year, interest, bottom=[i+j for i,j in zip(cost, operating)], edgecolor='white', label='Interest Expense')
        plt.bar(df_income['date'].dt.year, tax, bottom=[i+j+k for i,j,k in zip(cost, operating,interest)], edgecolor='white', label='Tax Expense')
        plt.bar(df_income['date'].dt.year, other, bottom=[i+j+k+l for i,j,k,l in zip(cost, operating,interest,tax)], edgecolor='white', label='Other Expenses')
        plt.bar(df_income['date'].dt.year, net, bottom=[i+j+k+l+m for i,j,k,l,m in zip(cost, operating,interest,tax,other)], edgecolor='white', label='Net Income')
        plt.xticks(np.arange(min(df_income['date'].dt.year), max(df_income['date'].dt.year)+1, 2))

        #ax.xaxis.set_major_locator(years)
        #ax.xaxis.set_major_formatter(years_fmt)

        plt.legend(loc='upper left', prop=fontP)
        st.pyplot(fig)
    except:
        st.dataframe(df_income)

except:
    st.write("Income statement data unavailble!")

#------------------------------------------------------------------------------#
st.header('Earnings per Share')

try:
    st.markdown("**EPS**")
    st.write("It is calculated as a company's profit divided by the outstanding shares of its common stock. EPS indicates how much money a company makes for each share of its stock and is a widely used metric for corporate profits. A higher EPS indicates more value because investors will pay more for a company with higher profits.")
    st.markdown(df_income.loc[0,'eps'])

    st.markdown("**EPS Diluted**")
    st.write("It calculates a company’s earnings per share if all convertible securities were converted. Dilutive securities aren’t common stock, but instead securities that can be converted to common stock. Converting these securities decreases EPS, thus, diluted EPS tends to always be lower than EPS. Dilutive EPS is considered a conservative metric because it indicates a worst-case scenario in terms of EPS.")
    st.markdown(df_income.loc[0,'epsdiluted'])

    fig, ax = plt.subplots()
    plt.subplot(211)
    plt.plot(list(df_income.date.values), list(df_income.eps.values), marker='o',  label='EPS', )
    plt.tick_params(axis='x', which='both',bottom=False, top=False, labelbottom=False)
    plt.legend(loc='upper left')

    plt.subplot(212)
    plt.plot(list(df_income.date.values), list(df_income.epsdiluted.values), marker='o',  label='EPS Diluted')
    plt.legend(loc='upper left')

    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_major_formatter(years_fmt)


    st.pyplot(fig)

except:
    st.write("Income statement data unavailble!")

#------------------------------------------------------------------------------#
st.header('Margins')

try:
    st.markdown("**Gross Margin**")
    st.write("It is a company's net sales revenue minus its cost of goods sold (COGS). \
    In other words, it is the sales revenue a company retains after incurring \
    the direct costs associated with producing the goods it sells, and the services it provides.")
    st.markdown(str(round(df_ratios.loc[0, 'grossProfitMargin']*100,2))+"%")

    st.markdown("**EBITDA Margin**")
    st.write("It is a measure of a company's operating profit as a percentage of its revenue. \
    Knowing the EBITDA margin allows for a comparison of one company's real performance \
    to others in its industry.")
    st.markdown(str(round(df_ratios.loc[0, 'operatingProfitMargin']*100,2))+"%")

    st.markdown("**EBIT Margin**")
    st.write("or Operating Margin is measures how much profit a company makes on a dollar of sales, \
    after paying for variable costs of production, such as wages and raw materials, \
    but before paying interest or tax. It is calculated by dividing a company’s operating profit \
    by its net sales. Also known as **Return on Sales**, is a good indicator of how well \
    it is being managed and how risky it is. It shows the proportion of revenues that are available \
    to cover non-operating costs.")
    st.markdown(str(round(df_ratios.loc[0, 'pretaxProfitMargin']*100,2))+"%")

    st.markdown("**Profit Margin**")
    st.write("It is one of the commonly used profitability ratios to gauge the degree to which \
    a company or a business activity makes money. \
    It represents what percentage of sales has turned into profits. \
    Simply put, the percentage figure indicates how many cents of profit the business has \
    generated for each dollar of sale")
    st.markdown(str(round(df_ratios.loc[0, 'netProfitMargin']*100,2))+"%")

    fig, ax = plt.subplots()

    plt.subplot(411)
    plt.plot(list(df_ratios.date.values), list(df_ratios.grossProfitMargin.values), marker='o',  label='Gross Margin', )
    plt.tick_params(axis='x', which='both',bottom=False, top=False, labelbottom=False)
    plt.legend(loc='upper left')

    plt.subplot(412)
    plt.plot(list(df_ratios.date.values), list(df_ratios.operatingProfitMargin.values), marker='o',  label='EBITDA Margin', )
    plt.tick_params(axis='x', which='both',bottom=False, top=False, labelbottom=False)
    plt.legend(loc='upper left')

    plt.subplot(413)
    plt.plot(list(df_ratios.date.values), list(df_ratios.pretaxProfitMargin.values), marker='o',  label='EBIT Margin', )
    plt.tick_params(axis='x', which='both',bottom=False, top=False, labelbottom=False)
    plt.legend(loc='upper left')

    plt.subplot(414)
    plt.plot(list(df_ratios.date.values), list(df_ratios.netProfitMargin.values), marker='o',  label='Profit Margin', )
    plt.legend(loc='upper left')

    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_major_formatter(years_fmt)
    ax.xaxis.set_minor_locator(months)
    st.pyplot(fig)
except:
    st.write("Margins data unavailble!")


#------------------------------------------------------------------------------#
st.header('Cash Flow')


st.markdown("**Operating Cashflow**")

try:
    st.write("It is a measure of the amount of cash generated by a company's normal business operations. \
    Operating cash flow indicates whether a company can generate sufficient positive cash flow to maintain and grow its operations, otherwise, it may require external financing for capital expansion. \
    Operating cash flows concentrate on cash inflows and outflows related to a company's main business activities, such as selling and purchasing inventory, providing services, and paying salaries.")
    st.markdown(str(round(df_cashflow.loc[0,'operatingCashFlow']/float(1e9),2)) + " billions")

    st.markdown("**Investing Cashflow**")
    st.write("It reports how much cash has been generated or spent from various investment-related activities in a specific period. \
    Investing activities include purchases of physical assets, investments in securities, or the sale of securities or assets. \
    Cash flows from investing activities provides an account of cash used in the purchase of non-current assets–or long-term assets– that will deliver value in the future. \
    Investing activity is an important aspect of growth and capital. \
    A change to property, plant, and equipment (PPE), a large line item on the balance sheet, is considered an investing activity.")
    st.markdown(str(round(df_cashflow.loc[0,'netCashUsedForInvestingActivites']/float(1e9),2)) + " billions")

    st.markdown("**Financing Cashflow**")
    st.write("It shows the net flows of cash that are used to fund the company. Financing activities include transactions involving debt, equity, and dividends. \
    Financing activities include transactions involving debt, equity, and dividends. \
    A company that frequently turns to new debt or equity for cash might show positive cash flow from financing activities. However, it might be a sign that the company is not generating enough earnings. \
    Also, as interest rates rise, debt servicing costs rise as well. Conversely, if a company is repurchasing stock and issuing dividends while the company's earnings are underperforming, it may be a warning sign.")
    st.markdown(str(round(df_cashflow.loc[0,'netCashUsedProvidedByFinancingActivities']/float(1e9),2)) + " billions")

    #years = df_cashflow['date'].dt.year
    #years = [d.year for d in date]
    totals = [i+j+k for i,j,k in zip(df_cashflow['operatingCashFlow'],
                                     df_cashflow['netCashUsedForInvestingActivites'],
                                     df_cashflow['netCashUsedProvidedByFinancingActivities'])]

    fig, ax = plt.subplots()
    plt.plot(list(df_cashflow.date.values), list(df_cashflow.operatingCashFlow.values),label='Operating Cashflow', color='#5886a5', marker='o')
    plt.plot(list(df_cashflow.date.values), list(df_cashflow.netCashUsedForInvestingActivites.values), label='Investing Cashflow', color='#7aa6c2', marker='o')
    plt.plot(list(df_cashflow.date.values), list(df_cashflow.netCashUsedProvidedByFinancingActivities.values), label='Financing Cashflow', color='#c1e7ff', marker='o')
    plt.plot(list(df_cashflow.date.values), list(df_cashflow.netChangeInCash.values), label='Net Cashflow',linestyle='--', color='#004c6d', marker='o')

    plt.legend(loc='upper left', prop=fontP)
    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_major_formatter(years_fmt)
    st.pyplot(fig)

    st.markdown("**Free Cashflow**")
    st.write("It represents the cash a company generates after accounting for cash outflows to support operations and maintain its capital assets. \
    Unlike earnings or net income, free cash flow is a measure of profitability that excludes the non-cash expenses of the income statement \
    and includes spending on equipment and assets as well as changes in working capital from the balance sheet.")
    st.markdown(str(round(df_cashflow.loc[0,'freeCashFlow']/float(1e9),2)) + " billions")

    fig, ax = plt.subplots()
    plt.plot(list(df_cashflow.date.values), list(df_cashflow.freeCashFlow.values),label='Free Cashflow', color='#5886a5', marker='o')
    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_major_formatter(years_fmt)
    st.pyplot(fig)

except:
    st.write("Cashflow data unavailble!")

#------------------------------------------------------------------------------#
st.header('Discounted Cash Flow')

try:
    st.write("It is a valuation method used to estimate the value of an investment based on its future cash flows. \
    The purpose of DCF analysis is to estimate the money an investor would receive from an investment, adjusted for the time value of money. \
    The time value of money assumes that a dollar today is worth more than a dollar tomorrow because it can be invested.")
    st.markdown(df_dcf.loc[0,'dcf'])

    fig, ax = plt.subplots()
    plt.plot(list(df_dcf.date.values), list(df_dcf.dcf.values),label='Discounted Cashflow', color='#004c6d', marker='o')
    plt.plot(list(df_dcf.date.values), list(df_dcf.price.values),label='Price', color='#5886a5', linestyle='--')
    plt.legend(loc='upper left', prop=fontP)
    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_major_formatter(years_fmt)
    st.pyplot(fig)
except:
    st.write("Cashflow data unavailble!")

#------------------------------------------------------------------------------#
st.subheader('References')
st.markdown("Explanatory text from [Investopedia](https://www.investopedia.com/)")
st.markdown("fmpcloud Python wrapper from [Github](https://github.com/razorhash/pyfmpcloud)")
