from FFM_SYSTEM.ffm_data import *
from pandas.tseries.offsets import BDay
from datetime import date


class EqPortVar:

    def __init__(self, db, user_name, portfolio, password, port_date, conf_level=0.95, std_dev_hor="daily"):

        print("********************************************")
        print("         PORTFOLIO VAR CALCULATION          ")
        print("********************************************")

        if conf_level == 0.99:
            self.multiplier = 2.33
        elif conf_level == 0.95:
            self.multiplier = 1.65

        self.port_data = SQL(data_base=db,
                             user_name=user_name,
                             password=password).select_data(select_query="""select ph.ticker, ph.market_value, ph.weight 
                                                                            from portfolio_holdings ph, portfolios p 
                                                                            where ph.portfolio_id = p.portfolio_id 
                                                                            and ph.date = '{date}' 
                                                                            and ph.type = 'EQUITY' 
                                                            and p.portfolio_name = '{port}'""".format(port=portfolio,
                                                                                                      date=port_date))

        self.port_nav = SQL(data_base=db,
                            user_name=user_name,
                            password=password).select_data(select_query="""select pn.total_nav 
                                                                           from portfolio_nav pn, portfolios p 
                                                                           where pn.portfolio_code = p.portfolio_id 
                                                                           and pn.date = '{date}' 
                                                            and p.portfolio_name = '{port}'""".format(port=portfolio,
                                                                                                      date=port_date))

        print("PORTFOLIO POSITIONS")
        print(self.port_data)
        print("")
        print("NAV:", list(self.port_nav["total_nav"])[0])
        print("Confidence level:", conf_level)

        if std_dev_hor == "daily":

            self.start_date = date.today() -  BDay(30)
            self.trading_days = 1**(1/2)

        elif std_dev_hor == "yearly":

            self.start_date = date.today() - BDay(256)
            self.trading_days = 256**(1/2)

        print("Time horizon:", self.trading_days**2)

        self.std = StockData(stock_list=list(self.port_data["ticker"]),
                             start_date=self.start_date).describe_returns()

        self.std = list(self.std.loc["std"])

        self.variance_matrix = []

        for variance, var_pos in zip(self.std, range(len(self.std))):

            self.variance_list = []

            for list_element in range(len(self.std)):

                if list_element == var_pos:
                    self.variance_list.append(variance)
                else:
                    self.variance_list.append(0.0)

            self.variance_matrix.append(self.variance_list)

        self.variance_matrix = np.array(self.variance_matrix)

        self.correlation_matrix = StockData(stock_list=list(self.port_data["ticker"]),
                                            start_date=self.start_date).correlations()

        self.vc = np.array(self.variance_matrix.dot(np.array(self.correlation_matrix)))
        self.vcv = self.vc.dot(self.variance_matrix)
        self.weights = np.array([weight / 100 for weight in list(self.port_data["weight"])])[np.newaxis]
        self.wvcv = np.array(self.weights).dot(self.vcv)
        self.wvcvw = self.wvcv.dot(self.weights.T)
        self.port_std_dev = self.wvcvw**(1/2)
        self.port_var = self.port_nav*self.trading_days*self.multiplier*self.port_std_dev

        print(len("VAR Value: " + str(list(self.port_var["total_nav"])[0]))*"=")
        print("VAR Value: " + str(list(self.port_var["total_nav"])[0]))
        print("VAR %:", list(self.port_var["total_nav"])[0]/list(self.port_nav["total_nav"])[0])
        print(len("VAR Value: " + str(list(self.port_var["total_nav"])[0])) * "=")

    def get_port_var(self):

        return list(self.port_var["total_nav"])[0]

    def get_port_var_perc(self):

        return list(self.port_var["total_nav"])[0]/list(self.port_nav["total_nav"])[0]


if __name__ == "__main__":

    EqPortVar(portfolio="TRD-1")

    # x["FB"].plot()
    # plt.show()




