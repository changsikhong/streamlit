import streamlit as st
import FinanceDataReader as fdr
import datetime
import time

# Finance Data Reader
# https://github.com/financedata-org/FinanceDataReader

st.title('종목 차트 검색')

with st.sidebar:
    start_date = st.date_input(
        "조회 시작일을 선택해 주세요",
        datetime.datetime(2023, 1, 1)
    )

    end_date = st.date_input(
        "조회 종료일을 선택해 주세요",
        #datetime.datetime(2023, 1, 1)
	datetime.datetime.now().date()
    )

    code = st.text_input(
        '종목코드', 
        value='',
        placeholder='종목코드를 입력해 주세요'
    )

    stock_code = fdr.StockListing('KRX')
    
    # Use a text_input to get the keywords to filter the dataframe
    text_search = st.text_input("회사이름을 입력해주세요", value="")

    # Filter the dataframe using masks
    m1 = stock_code["Name"].str.contains(text_search)
    df_search = stock_code[m1][['Code','Name']]
    if text_search:
        st.write(df_search)


if code and start_date and end_date:
    df = fdr.DataReader(code, start_date, end_date)
    data = df.sort_index(ascending=True).loc[:, 'Close']

    tab1, tab2 = st.tabs(['차트', '데이터'])

    with tab1:    
        st.line_chart(data)

    with tab2:
        st.dataframe(df.sort_index(ascending=False))

    with st.expander('컬럼 설명'):
        st.markdown('''
        - Open: 시가
        - High: 고가
        - Low: 저가
        - Close: 종가
        - Adj Close: 수정 종가
        - Volumn: 거래량
        ''')