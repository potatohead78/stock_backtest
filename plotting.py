import plotly.graph_objects as go
import plotly.subplots as ms
import plotly.express as px
import plotly.io as po
from datetime import datetime
import pandas as pd

class Plotting:
    def single(self, df_result:pd.DataFrame) -> None:
        """평가금액, 현금 및 캔들차트를 plotting 함.
            웹페이지가 출력되지 않을 경우 F5(새로고침)

        Args:
        df_result (pd.DataFrame): OHLC 및 기타 컬럼 + 'current_cash', 'market_value', 'buy', 'sell'(매도 날짜에 해당하는 매도금액)
        """
        fig = ms.make_subplots(rows=5, cols=1, specs=   [[{}],                  # 평가금액
                                                        [{'rowspan':4}],        # 차트
                                                        [None],                 # 차트
                                                        [None],                 # 차트
                                                        [None]                  # 차트
                                                        ],shared_xaxes=True, horizontal_spacing=0.03, vertical_spacing=0.01)

        # row1
        market_value = go.Scatter(x=df_result.index,
                                    mode='lines',
                                    y=df_result['market_value'],
                                    line=dict(color='blue', width=2),
                                    showlegend=False,
                                    name='평가금액')
        current_cash = go.Scatter(x=df_result.index,
                                    mode='lines',
                                    y=df_result['current_cash'],
                                    line=dict(color='red', width=2),
                                    showlegend=False,
                                    name='현금')

        # row2
        candle = go.Candlestick(x=df_result.index,
                                open=df_result['open'],high=df_result['high'],low=df_result['low'],close=df_result['close'],
                                increasing_line_color='red',
                                decreasing_line_color='blue',
                                showlegend=False,
                                name='')
        ma5 = go.Scatter(x=df_result.index,
                            y=df_result['ma5'],
                            mode='lines',
                            line=dict(color='green', width=2),
                            opacity=0.4,
                            name='ma5',
                            showlegend=False)
        ma20 = go.Scatter(x=df_result.index,
                            y=df_result['ma20'],
                            mode='lines',
                            line=dict(color='red', width=2),
                            opacity=0.4,
                            name='ma20',
                            showlegend=False)
        ma60 = go.Scatter(x=df_result.index,
                            y=df_result['ma60'],
                            mode='lines',
                            line=dict(color='orange', width=2),
                            opacity=0.4,
                            name='ma60',
                            showlegend=False)
        ma120 = go.Scatter(x=df_result.index,
                            y=df_result['ma120'],
                            mode='lines',
                            line=dict(color='purple', width=2),
                            opacity=0.4,
                            name='ma120',
                            showlegend=False)
        buy = go.Scatter(x=df_result.index,
                            y=df_result['buy'],
                            mode='markers',
                            marker=dict(color='chocolate',size=20,symbol='triangle-up'),
                            opacity=0.8,
                            showlegend=False,
                            name='매수')
        sell = go.Scatter(x=df_result.index,
                            y=df_result['sell'],
                            mode='markers',
                            marker=dict(color='cyan',size=20,symbol='triangle-down'),
                            opacity=0.8,
                            showlegend=False,
                            name='매도')

        fig.add_trace(market_value,row=1,col=1)
        fig.add_trace(current_cash,row=1,col=1)

        fig.add_trace(candle,row=2,col=1)
        fig.add_trace(ma5,row=2,col=1)
        fig.add_trace(ma20,row=2,col=1)
        fig.add_trace(ma60,row=2,col=1)
        fig.add_trace(ma120,row=2,col=1)
        fig.add_trace(buy,row=2,col=1)
        fig.add_trace(sell,row=2,col=1)

        title = datetime.now().strftime('%Y.%m.%d.%H%M%S')

        fig.update_layout(autosize=True,
                            xaxis1_rangeslider_visible=False,
                            xaxis2_rangeslider_visible=False,
                            margin=dict(l=50,r=50,t=50,b=50),
                            template='seaborn',
                            title=f"{title}")
        fig.update_xaxes(tickformat='%y년%m월%d일',
                            zeroline=True,
                            zerolinewidth=1,
                            zerolinecolor='black',
                            showgrid=True,
                            gridwidth=2,
                            gridcolor='lightgray',
                            showline=True,
                            linewidth=2,
                            linecolor='black',
                            mirror=True)
        fig.update_yaxes(tickformat=',d',
                            zeroline=True,
                            zerolinewidth=1,
                            zerolinecolor='black',
                            showgrid=True,
                            gridwidth=2,
                            gridcolor='lightgray',
                            showline=True,
                            linewidth=2,
                            linecolor='black',
                            mirror=True)
        fig.update_traces(xhoverformat='%y년%m월%d일')

        config = dict({'scrollZoom': True})
        po.write_html(fig, file=f"결과/{title}.html")
        fig.show(config=config)