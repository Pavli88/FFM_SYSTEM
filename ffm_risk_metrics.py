import numpy as np
from FFM_SYSTEM.ffm_data import *


class PortVar:

    # For daily portfolio VAR use 30 days data sample

    # For monthly VAR use

    def __init__(self):
        pass


if __name__ == "__main__":

    stock_list = ['AAPL', 'FB', 'MSFT']
    start_date = "2019-03-08"
    x = StockData(stock_list=stock_list, start_date=start_date).correlations()

    std = StockData(stock_list=stock_list, start_date=start_date).describe_returns()

    std1 = np.asarray(std.loc["std"])

    w = [0.5, 0.2, 0.3 ]

    print(np.asarray(w))
    print(x.as_matrix())
    print(np.asarray(w)*x.as_matrix())

    # x["FB"].plot()
    # plt.show()




