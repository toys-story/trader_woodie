import os
import sys
import json
sys.path.append(os.curdir)

from toybox.src.toybox.base import baseTrader, logging
from toybox.src.toybox.libs import get_data, get_std

class updater(baseTrader):

    def __init__(self, capital=0) -> None:
        super().__init__(capital=capital)
        self.target_market = ["KRW-ETH", "KRW-BTC"]
        self.from_date = from_date=[2021, 9, 25, 10, 0, 0]

    def check_conditions(self, data) -> str:
        return super().check_conditions(data)

    @logging
    def get_datas(self):
        ret_datas = dict()
        for target in self.target_market:
            ret_datas[target] = get_data(self.client, market=target, 
                                         type="days", from_date=self.from_date)
        return ret_datas

    @logging
    def write_json(self, data):
        with open("crypto.json", "w") as fw:
            json.dump(data, fw)

    def run(self):
        datas = self.get_datas()
        self.write_json(datas)


if __name__ == "__main__":
    u = updater()
    u.run()