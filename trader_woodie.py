import os
import sys
sys.path.append(os.curdir)

from toybox.src.toybox.base import baseTrader, logging
from toybox.src.toybox.libs import get_data, get_std


class woodieTrader(baseTrader):
    
    def __init__(self, capital=0, from_date=list(), test_mode=True):
        super().__init__(capital=capital)
        self.target_market = "KRW-SAND"
        self.from_date = from_date
        self.data = get_data(self.client, market=self.target_market,from_date=self.from_date)
        
        self.buy_ratio = 0.5
        self.sell_ratio = 1.0
        self.stds = get_std(data=self.data)
        self.buy_conditions = [    
            self.stds["Hclose_by_open"] * 100,
            self.stds["Htail_by_close"] * 100,
        ]
        self.sell_conditions = [
            self.stds["Lclose_by_open"] * 100,
            self.stds["Ltail_by_close"] * 100,
        ]

    def check_conditions(self, data) -> str:
        open = float(data.get("opening_price", ""))
        close = float(data.get("trade_price", ""))
        high = float(data.get("high_price", ""))
        low = float(data.get("low_price", ""))
        time = data.get("candle_date_time_kst", "")
        
        positive_candle = True if close - open > 0 else False
        open_to_close = abs((close - open) / open * 100)
        decision = "Stay"
        desc = ""

        if positive_candle:
            close_to_high = (high - open) / open * 100 - open_to_close
            desc = f"{time}, [Buy] Close : {round(open_to_close , 2)}, Close compared to High : {round(close_to_high, 2)}"
        else:
            close_to_low = (low - open) / open * (-100) - open_to_close
            desc = f"{time}, [Sell] Close : {round(open_to_close , 2)}, Close compared to Low : {round(close_to_low, 2)}"

        if positive_candle:
            if open_to_close >= self.buy_conditions[0] and close_to_high <= self.buy_conditions[1]:
                # Price is higher than std and upper-tail is lower than std
                decision = "Buy"
        else:
            if open_to_close >= self.sell_conditions[0]:
                # The Price is lower than std
                decision = "Sell"
        return decision, desc
    
    def main(self):
        print(f"data : {len(trader.data)} EA")
        print(f"buy_conditions : {trader.buy_conditions}")
        print(f"sell_conditions : {trader.sell_conditions}")
        
        try:
            for d in self.data:
                market = d.get("market", None)
                price = d.get("trade_price", None)
                time = d.get("candle_date_time_kst", None)
                
                if not market or not price or not time:
                    print(f"Error : {market}, {price}, {time}")
                    raise RuntimeError("Error : invaild data")

                decision, desc = self.check_conditions(d)
                if decision == "Buy":
                    if self.buy_stock(market=market, price=price, time=time, buy_ratio=self.buy_ratio):
                        print(desc)
                elif decision == "Sell":
                    if self.sell_stock(market=market, price=price, time=time, sell_ratio=self.sell_ratio):
                        print(desc)
                else:
                    # Stay ~!
                    pass
        except Exception as e:
            print(e)
        finally:
            if self.sell_stock(market=market, price=price, time=time, sell_ratio=self.sell_ratio):
                print("sell all of stocks")
        
        self.show_trade_history()
        self.account.show_account()

        

if __name__ == "__main__":
    trader = woodieTrader(capital=1000000,from_date=[2021, 12, 12, 10, 0, 0])
    trader.main()
    
    
