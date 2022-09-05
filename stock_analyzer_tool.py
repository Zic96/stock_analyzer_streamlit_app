import yfinance as yf
import streamlit as st
import datetime
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import date


def recome_analyst(recco):
    """
    parameters: x (dataframe)
    Convert the recommendations dataframe into a bar
    plot for 2022
    """
    df = recco.recommendations
    df.reset_index(inplace=True)
    df["year"] = df["Date"].dt.year
    dfup = df.loc[df["year"] == currentYear]
    groupp = dfup.groupby(["To Grade"]).count()
    groupp.sort_values(by="Date", ascending=True, inplace=True)
    fig_recco = px.bar(groupp, x="Action", title="Analysts Recommendations 2022")
    return fig_recco


currentYear = date.today().year

title = st.title(":wave: Welcome, To Stock Analyzer Tool!")

# searchbar
with st.form(key="searchform", clear_on_submit=False):
    nav1, nav2 = st.columns([2, 1])

    with nav1:
        search_term = st.text_input("Please Enter The Ticket Sumbol")
    with nav2:
        st.text("")
        st.text("")
        sumbit_search = st.form_submit_button()
# if company exist
try:
    if sumbit_search:
        stock = yf.Ticker(search_term)

        # get the logo, sector and industry
        logocol, infocol = st.columns([2, 1])

        with logocol:
            string_logo = "<img src=%s>" % stock.info["logo_url"]
            st.markdown(string_logo, unsafe_allow_html=True)
        with infocol:
            st.text("")
            st.text("")
            st.write("**{} | {}**".format(stock.info["sector"], stock.info["industry"]))

        # create the price chart
        start_date = datetime.date(2019, 1, 1)
        end_date = date.today()
        st.line_chart(
            stock.history(period="1d", start=start_date, end=end_date)["Close"]
        )
        # summary metrics table
        with st.container():
            summ1, summ2, summ3 = st.columns([3, 2, 1])
            with summ1:
                divyield = stock.info["dividendYield"]
                markkcap = round(stock.info["marketCap"] / 1000000000, 2)
                st.write("**Market Cap: {} B $** ".format(markkcap))
                try:
                    st.write(
                        "**Div. Yield: {}%**".format(
                            round(stock.info["dividendYield"] * 100, 2)
                        )
                    )
                except:
                    st.write("**Div. Yield: {}**".format(stock.info["dividendYield"]))
            # more information section
            with summ2:

                st.write("**52-wk high: {}**".format(stock.info["fiftyTwoWeekHigh"]))
                st.write("**52-wk low: {}**".format(stock.info["fiftyTwoWeekLow"]))
            with summ3:

                try:
                    st.write("**P/E: {}**".format(stock.info["trailingPE"]))
                except:
                    st.write("**P/E: --**")
                st.write(
                    "**P/S: {}**".format(stock.info["priceToSalesTrailing12Months"])
                )
        expander = st.expander("More About This Company")
        expander.info(stock.info["longBusinessSummary"])

        x1 = stock.info["ebitdaMargins"]
        y1 = stock.info["profitMargins"]
        w = stock.info["grossMargins"]

        # creating the tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs(
            [
                "Financial Ratios",
                "Dividend",
                "Major Holders",
                "Analysts Rating",
                "Technical Analysis",
            ]
        )

        with tab1:
            valuations, margins_r, profitability, fina_health, growth = st.tabs(
                [
                    "Valuations",
                    "Margins",
                    "Profitability",
                    "Financial Health",
                    "Growth",
                ]
            )
            with valuations:
                fig_val = go.Figure(
                    data=[
                        go.Table(
                            header=dict(
                                values=[
                                    "Price To Book",
                                    "Enterprice To Revenue",
                                    "Enterprice To EBITDA",
                                    "Sort Ratio(%)",
                                ]
                            ),
                            cells=dict(
                                values=[
                                    [
                                        round(stock.info["priceToBook"], 2),
                                    ],
                                    [
                                        round(stock.info["enterpriseToRevenue"], 2),
                                    ],
                                    [
                                        round(stock.info["enterpriseToEbitda"], 2),
                                    ],
                                    [round(stock.info["shortRatio"], 2)],
                                ]
                            ),
                        )
                    ]
                )
                st.write(fig_val)
            with margins_r:
                fig_marg = go.Figure(
                    data=[
                        go.Table(
                            header=dict(
                                values=[
                                    "Gross Margins",
                                    "Operating Margins",
                                    "EBITDA Margins",
                                    "Profit Margins",
                                ]
                            ),
                            cells=dict(
                                values=[
                                    [
                                        round(stock.info["grossMargins"], 2),
                                    ],
                                    [
                                        round(stock.info["operatingMargins"], 2),
                                    ],
                                    [
                                        round(stock.info["ebitdaMargins"], 2),
                                    ],
                                    [round(stock.info["profitMargins"], 2)],
                                ]
                            ),
                        )
                    ]
                )
                st.write(fig_marg)
            with profitability:
                fig_profi = go.Figure(
                    data=[
                        go.Table(
                            header=dict(
                                values=[
                                    "ROA",
                                    "ROE",
                                ]
                            ),
                            cells=dict(
                                values=[
                                    [
                                        round(stock.info["returnOnAssets"], 2),
                                    ],
                                    [
                                        round(stock.info["returnOnEquity"], 2),
                                    ],
                                ]
                            ),
                        )
                    ]
                )
                st.write(fig_profi)
            with fina_health:
                fig_hea = go.Figure(
                    data=[
                        go.Table(
                            header=dict(
                                values=[
                                    "Current Ratio",
                                    "Quick Ratio",
                                    "Debt To Equity",
                                ]
                            ),
                            cells=dict(
                                values=[
                                    [
                                        round(stock.info["currentRatio"], 2),
                                    ],
                                    [
                                        round(stock.info["quickRatio"], 2),
                                    ],
                                    [
                                        round(stock.info["debtToEquity"], 2),
                                    ],
                                ]
                            ),
                        )
                    ]
                )
                st.write(fig_hea)
            with growth:
                fig_gro = go.Figure(
                    data=[
                        go.Table(
                            header=dict(
                                values=[
                                    "Revenue Growth",
                                    "Earnings Growth",
                                    "Earnings Quarterly Growth",
                                ]
                            ),
                            cells=dict(
                                values=[
                                    [
                                        round(stock.info["revenueGrowth"], 2),
                                    ],
                                    [
                                        round(stock.info["earningsGrowth"], 2),
                                    ],
                                    [
                                        round(stock.info["earningsQuarterlyGrowth"], 2),
                                    ],
                                ]
                            ),
                        )
                    ]
                )
                st.write(fig_gro)

        with tab2:
            try:
                if divyield < 20:
                    with st.container():
                        st.write("**Dividend Summary**")
                        # bulding dividend summary table
                        fig = go.Figure(
                            data=[
                                go.Table(
                                    header=dict(
                                        values=[
                                            "Dividend",
                                            "Div Yield",
                                            "5 Year Avg Div Yield",
                                            "Payout Ratio",
                                        ]
                                    ),
                                    cells=dict(
                                        values=[
                                            [
                                                stock.info["lastDividendValue"],
                                            ],
                                            [
                                                round(
                                                    stock.info[
                                                        "trailingAnnualDividendYield"
                                                    ]
                                                    * 100,
                                                    2,
                                                )
                                            ],
                                            [
                                                stock.info["fiveYearAvgDividendYield"],
                                            ],
                                            [round(stock.info["payoutRatio"], 2)],
                                        ]
                                    ),
                                )
                            ]
                        )
                        st.write(fig)

                    div_his = stock.dividends
                    # bulding the dividend history bar plot
                    fig_div = px.bar(div_his, y="Dividends", title="Dividend History")
                    st.write(fig_div)
                else:
                    st.title("This Company Doesn't Give A Dividend")
            except:
                # if comapny doesnt give dividend
                st.title("This Company Doesn't Give A Dividend")

        with tab3:
            # creating major holders tab
            st.write(
                "**This table shows the biggest institutional investors(Hedge Funds, Pansion Funds, etc.**)"
            )
            stock.institutional_holders
        with tab4:
            st.write(recome_analyst(stock))
            st.write(
                "**According to these analysts, this company is: {} 😎**".format(
                    stock.info["recommendationKey"].upper()
                )
            )
        with tab5:
            st.header("Moving Averages")
            df = stock.history(period="4y")[["Open", "Close", "High", "Low", "Volume"]]
            # creating the moving average for 50 and 200 days
            df["MA50"] = df["Close"].rolling(50).mean()
            df["MA200"] = df["Close"].rolling(200).mean()
            fig_mov1 = go.Figure(
                data=[
                    go.Candlestick(
                        x=df.index,
                        open=df["Open"],
                        high=df["High"],
                        low=df["Low"],
                        close=df["Close"],
                        showlegend=False,
                    ),
                ]
            )
            fig_mov1.add_trace(
                go.Scatter(x=df.index, y=df["MA50"], line=dict(width=2), name="MA50")
            )
            # Add the EMA 5
            fig_mov1.add_trace(
                go.Scatter(x=df.index, y=df["MA200"], line=dict(width=2), name="MA200")
            )
            st.write(fig_mov1)


# if company doesn't exist
except:
    st.success("Something Went Wrong 😔, Please Try Again!")
