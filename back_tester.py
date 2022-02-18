import os
import sys
import json
sys.path.append(os.curdir)

from toybox.src.toybox.base import baseTrader, logging
from toybox.src.toybox.libs import get_data, get_std
from toybox.src.toybox.consts import Status


class Conditions():
    def __init__(self) -> None:
        self.standard_ratio_crpyto = 0.1
        self.standard_ratio_cash = 0.9
        self.over_standard_ratio_crypto = 0.15
        self.under_standard_ratio_crypto = 0.067
    
    def set_args(self, **kwargs):
        for key,val in kwargs.items():
            setattr(self, key, val)

class BackTester(baseTrader):

    def __init__(self, capital=0, from_date=list(), test_mode=True, **kwargs) -> None:
        super().__init__(capital=capital)
        self.target_market = ["KRW-ETH", "KRW-BTC"]
        self.from_date = from_date
        self.data = self.get_datas()
        self.conditions = Conditions()
        self.conditions.set_args(**kwargs)
    
    def check_conditions(self, data) -> None:
        pass

    def get_datas(self, local=True):
        ret_datas = dict()

        if local:
            with open("crypto.json", "r") as fr:
                ret_datas = json.load(fr)
        else:
            for target in self.target_market:
                ret_datas[target] = get_data(self.client, market=target, 
                                            type="days", from_date=self.from_date)    
        return ret_datas

    def rebalancing(self, type="SELL"):
        # 여기서 over/under 구분해서 작업드가자
        
        pass

    def check_current_asset(self, stock_info:dict):
        sum_diff = 0
        for key, val in self.account.stock.items():
            diff = val["avg_price"] - stock_info[key]["price"]
            val["diff"] = stock_info[key]["price"] / val["avg_price"] - 1.0
            sum_diff += (diff * val["amount"])
        change_rate = sum_diff / self.account.last_capital
        
        if change_rate >= self.conditions.over_standard_ratio_crypto:
            return "SELL"
        elif change_rate <= self.conditions.under_standard_ratio_crypto:
            return "BUY"
        
        # TODO : 여기에서 ratio_by_crypto 출력해야 함
        return "HOLD"

    def main(self):
        self.check_current_asset()
        print()
        

if __name__ == "__main__":
    trader = BackTester(capital=1000000,from_date=[2021, 9, 25, 10, 0, 0])
    trader.main()
    
    
