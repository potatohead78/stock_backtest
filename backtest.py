import pandas as pd
from message_log import Message_log

pd.options.mode.chained_assignment = None

class Backtest_single:
    """단일 종목의 백테스트를 진행."""
    def __init__(self, current_cash:int, df_ohlc:pd.DataFrame) -> None:
        """
        Args:
        current_cash (int): 총 투자금
        df_ohlc (pd.DataFrame): OHLC 컬럼 및 Strategy()에 필요한 컬럼
        """
        self.log = Message_log()

        self.bought_dict = {}
        self.current_cash = current_cash
        self.df_ohlc = df_ohlc
        self.df_result = pd.DataFrame(index=self.df_ohlc.index)

        self.df_result['current_cash'] = self.current_cash
        self.df_result['market_value'] = None
        self.df_result['buy'] = None
        self.df_result['sell'] = None

    def simulation(self, condition:dict) -> pd.DataFrame:
        """매수매도 백테스트 진행.

        Args:
        condition (dict): 매수매도 조건, {"Buy":조건, "Sell":조건, "Buy_price":조건, "Sell_price":조건} ->  {
                                                                                                            "Buy":"['MFI5'] < 20",
                                                                                                            "Sell":"['MFI5'] > 80",
                                                                                                            "Buy_price":"['close']",
                                                                                                            "Sell_price":"['close']"
                                                                                                            }

        Returns:
        pd.concat([self.df_ohlc, self.df_result], axis=1) (pd.DataFrame): OHLC 및 기타 컬럼 + 'current_cash', 'market_value'(평가금액), 'buy', 'sell'(매도 날짜에 해당하는 매도금액)
        """
        _code = 'temp_name'
        for i, date in enumerate(self.df_ohlc.index):
            ohlc_to_today = self.df_ohlc.loc[:date]
            # Buy
            if _code not in list(self.bought_dict)[:]:
                target_buy_price, qty = Strategy().buy_check(ohlc_to_today, self.current_cash, condition)
                if qty > 0:
                    self.df_result['current_cash'].iloc[i:] -= (target_buy_price*qty)
                    self.log.printlog(f"{self.df_result.index[i]} BUY: {format(int(target_buy_price),',')} 원, {format(int(qty),',')} qty")
                    self.df_result['buy'].iloc[i] = target_buy_price
                    self.bought_dict[_code] = (target_buy_price, qty)
            # Sell
            # 세금 추가요망
            elif _code in list(self.bought_dict)[:]:
                target_sell_price, qty = Strategy().sell_check(ohlc_to_today, self.bought_dict[_code], condition)
                if qty == 0:
                    self.df_result['current_cash'].iloc[i:] += (target_sell_price*self.bought_dict[_code][1])
                    self.log.printlog(f"{self.df_result.index[i]} SELL: {format(int(target_sell_price),',')} 원, {format(int(self.bought_dict[_code][1]),',')} qty")
                    self.df_result['sell'].iloc[i] = target_sell_price
                    del self.bought_dict[_code]
            # 평가금액 갱신
            self.df_result['market_value'].iloc[i] = self.df_result['current_cash'].iloc[i].copy()
            for _code in list(self.bought_dict)[:]:
                self.df_result['market_value'].iloc[i] += (ohlc_to_today['close'].iloc[-1] * self.bought_dict[_code][1])
        
        self.log.log_exit()
        return pd.concat([self.df_ohlc, self.df_result], axis=1)

    def data_check(self):
        """df_ohlc 입력 데이터를 검증."""
        pass

class Strategy:
    """매수와 매도 전략을 작성."""
    def buy_check(self, ohlc_to_today:pd.DataFrame, current_cash:int, condition:dict) -> tuple[int,int]:
        """매수 신호 체크.

        Args:
        ohlc_to_today (pd.DataFrame): OHLC 및 기타
        current_cash (int): 현재 금액
        condition (dict): 매수매도 조건, {"Buy":조건, "Sell":조건, "Buy_price":조건, "Sell_price":조건} ->  {
                                                                                                            "Buy":"['MFI5'] < 20",
                                                                                                            "Sell":"['MFI5'] > 80",
                                                                                                            "Buy_price":"['close']",
                                                                                                            "Sell_price":"['close']"
                                                                                                            }

        Returns:
        target_buy_price (int): 매수금액 또는 0
        qty (int): 매수 개수 또는 0(매수하지 않음)

        """
        buy_condition = condition['Buy'].replace('[','ohlc_to_today[')
        buy_condition = buy_condition.replace(']','].iloc[-1]')
        buy_price_condition = condition['Buy_price'].replace('[','ohlc_to_today[')
        buy_price_condition = buy_price_condition.replace(']','].iloc[-1]')

        if eval(buy_condition):
            target_buy_price = int(eval(buy_price_condition))
            qty = int(current_cash // target_buy_price)
            return target_buy_price, qty
        else:
            return 0, 0

    def sell_check(self, ohlc_to_today:pd.DataFrame, bought_tuple:tuple[int,int], condition:dict) -> tuple[int,int]:
        """매도 신호 체크.
        
        Args:
        ohlc_to_today (pd.DataFrame): OHLC 및 기타
        bought_tuple (tuple(int,int)): (target_buy_price, qty)
        condition (dict): 매수매도 조건, {"Buy":조건, "Sell":조건, "Buy_price":조건, "Sell_price":조건} ->  {
                                                                                                            "Buy":"['MFI5'] < 20",
                                                                                                            "Sell":"['MFI5'] > 80",
                                                                                                            "Buy_price":"['close']",
                                                                                                            "Sell_price":"['close']"
                                                                                                            }
        Returns:
        target_sell_price (int): 매도금액 또는 0
        qty (int) = 0(매도) 또는 bought_tuple[1](매도하지 않음)
        """
        sell_condition = condition['Sell'].replace('[','ohlc_to_today[')
        sell_condition = sell_condition.replace(']','].iloc[-1]')
        sell_price_condition = condition['Sell_price'].replace('[','ohlc_to_today[')
        sell_price_condition = sell_price_condition.replace(']','].iloc[-1]')

        if eval(sell_condition):
            target_sell_price = int(eval(sell_price_condition))
            qty = 0
            return target_sell_price, qty
        else:
            return 0, bought_tuple[1]