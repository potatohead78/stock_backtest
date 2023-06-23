from backtest import Backtest_multi
from plotting import Plotting
import pandas as pd

# 여러 종목 동시 백테스트
def ohlc_maker():
        columns = ['open','high','low','close','volume','MFI5']
        rows = [[46400,46500,45100,45100,23569321,42.14411591],	
                [46000,46100,44800,44850,12926539,26.45925598],	
                [44600,45100,44150,44250,10612405,13.09183041],	
                [44000,44300,43700,44000,10202544,12.76253476],	
                [43400,44950,43400,44450,11049749,15.93690306],	
                [44450,44800,43800,43800,7729069 ,20.93601985],		
                [44400,44450,43650,43650,10717408,22.01248971],	
                [44300,44950,44150,44650,11431977,44.20485706],	
                [44250,44450,43700,43850,8108343 ,46.08421644],		
                [43700,44300,43550,43850,18039161,20.6334358],
                [43800,44250,43700,44200,16814163,43.57041239],	
                [43950,44150,43450,43700,8188876 ,45.34445198],		
                [43750,43900,43550,43900,7609563 ,41.60667862],		
                [43800,44200,43100,44050,9846242 ,56.67766517],		
                [44600,46250,44050,45850,21138016,87.30272174],	
                [46850,47000,46250,46550,12535911,86.55745426],	
                [45300,45650,44800,45500,8699728 ,85.40924411],		
                [45500,45700,44900,45250,9729811 ,70.2843228],	
                [44750,45600,44250,45350,9568081 ,54.93756354]
                ]							

        index = ['2019-02-28',
                '2019-03-04',
                '2019-03-05',
                '2019-03-06',
                '2019-03-07',
                '2019-03-08',
                '2019-03-11',
                '2019-03-12',
                '2019-03-13',
                '2019-03-14',
                '2019-03-15',
                '2019-03-18',
                '2019-03-19',
                '2019-03-20',
                '2019-03-21',
                '2019-03-22',
                '2019-03-25',
                '2019-03-26',
                '2019-03-27']

        df_ohlc = pd.DataFrame(rows, columns=columns, index=index)
        return df_ohlc

dict_ohlc = {'code1':ohlc_maker(), 'code2':ohlc_maker(), 'code3':ohlc_maker()}
"""증권사 api 등을 활용하여 OHLC 데이터를 수집해주세요."""
"""OHLC는 데이터프레임 형식으로 입력합니다. (오름차순)"""
"""index에 날짜를 입력합니다. 2019-01-01 형식으로 변경해주세요."""


#df_benchmark = 0.9 * ohlc_maker()
df_benchmark = 0
"""벤치마크 OHLC 데이터를 수집해주세요."""
"""0를 입력할 경우 KODEX 200으로 자동 수집, 설정됩니다."""


current_cash = 10000000
"""총 투자금"""


buy_tax = 0.00015
sell_tax = 0.00215
"""buy_tax : 0.015% (거래수수료) = 0.015% (기본값)"""
"""sell_tax : 0.015% (거래수수료) + 0.05% (증권거래세) + 0.15% (농어촌특별세) = 0.215% (기본값)"""
"""buy_tax와 sell_tax 입력은 옵션입니다. 세금을 제외할 때는 각각 0을 입력해주세요."""


target_buy_count = 10
"""종목을 매수하는 최대 개수 = 10 (기본값)"""


buy_method = 0
"""종목당 매수금액을 고정금액((예시) 1000000)또는 변동금액(비율)(0)로 설정합니다. = 0 (기본값)"""
"""고정금액 선택 시 매수 금액 입력. 해당 금액으로 매수합니다."""
"""변동금액 선택 시 0을 입력. current_cash/target_buy_count 금액으로 매수합니다."""


condition = {
                "Buy":"['MFI5'] < 20",
                "Sell":"['MFI5'] > 80",
                "Buy_price":"['close']",
                "Sell_price":"['close']"
                }
"""매수매도 조건을 입력해주세요."""
"""해당 조건의 데이터는 df_ohlc 컬럼에 존재하여야 합니다."""
"""다중조건도 가능합니다.
예시){
        "Buy":"['MFI5'] < 20 and ['volume'] > 1000000",
        "Sell":"['MFI5'] > 80 or ['volume'] > 1000000",
        "Buy_price":"['close']",
        "Sell_price":"['close'] if ['MFI5'] > 80 else ['high']"
        }
"""


df_result = Backtest_multi(current_cash, dict_ohlc, target_buy_count, buy_method, buy_tax, sell_tax).simulation(condition)
"""df_result에는 OHLC와 현금, 평가금액, 매수금액, 매도금액 등이 입력 되어있습니다."""
"""기본값은 buy_tax: 0.00015, sell_tax: 0.00215 입니다."""


Plotting().multi(df_result, df_benchmark)
"""결과를 Plotting 합니다."""
