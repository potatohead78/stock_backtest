import plotly.graph_objects as go
import plotly.subplots as ms
import plotly.express as px
import plotly.io as po
from datetime import datetime
import pandas as pd

class Plotting:
    def single(self, df_result:pd.DataFrame):
        fig = ms.make_subplots(rows=3, cols=1, specs=   [[{}],                # 평가금액
                                                        [{'rowspan':2}],        # 차트
                                                        [None]                    # 차트
                                                        ],shared_xaxes=True, horizontal_spacing=0.03, vertical_spacing=0.01)

        # row1
        market_value = go.Scatter(x=df_result.index, y=df_result['market_value'], line=dict(color='blue', width=2), showlegend=False, name='평가금액')
        current_cash = go.Scatter(x=df_result.index, y=df_result['current_cash'], line=dict(color='red', width=2), showlegend=False, name='현금')

        # row2
        candle = go.Candlestick(x=df_result.index, open=df_result['open'],high=df_result['high'],low=df_result['low'],close=df_result['close'], increasing_line_color='red',decreasing_line_color='blue', showlegend=False, name='')
        buy = go.Scatter(x=df_result.index, y=df_result['buy'], mode='markers', marker=dict(color='red',size=20,symbol='triangle-up'), opacity=0.8, showlegend=False, name='매수')
        sell = go.Scatter(x=df_result.index, y=df_result['sell'], mode='markers', marker=dict(color='blue',size=20,symbol='triangle-down'), opacity=0.8, showlegend=False, name='매도')

        fig.add_trace(market_value,row=1,col=1)
        fig.add_trace(current_cash,row=1,col=1)

        fig.add_trace(candle,row=2,col=1)
        fig.add_trace(buy,row=2,col=1)
        fig.add_trace(sell,row=2,col=1)

        fig.update_layout(autosize=True, xaxis1_rangeslider_visible=False, xaxis2_rangeslider_visible=False, margin=dict(l=50,r=50,t=50,b=50), template='seaborn', title=f"{datetime.now().strftime('%Y.%m.%d.%H%M%S')}")
        fig.update_xaxes(tickformat='%y년%m월%d일', zeroline=True, zerolinewidth=1, zerolinecolor='black', showgrid=True, gridwidth=2, gridcolor='lightgray', showline=True,linewidth=2, linecolor='black', mirror=True)
        fig.update_yaxes(tickformat=',d', zeroline=True, zerolinewidth=1, zerolinecolor='black', showgrid=True, gridwidth=2, gridcolor='lightgray',showline=True,linewidth=2, linecolor='black', mirror=True)
        fig.update_traces(xhoverformat='%y년%m월%d일')

        config = dict({'scrollZoom': True})
        po.write_html(fig, file='결과/.html')
        fig.show(config=config)