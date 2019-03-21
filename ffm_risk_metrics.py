from FFM_SYSTEM.ffm_data import *
from pandas.tseries.offsets import BDay
from datetime import date
import argparse

# --------------- #
#  VAR ARGUMENTS  #
# --------------- #

parser = argparse.ArgumentParser()

# General data points
parser.add_argument("--var", help="VAR calculation. Switch: Yes")
parser.add_argument("--port", help="Portfolio. Switch: specific")
parser.add_argument("--date", help="Date. Switch: specific")

# Database
parser.add_argument("--db", help="Database. Switch: specific")
parser.add_argument("--user_name", help="User Name. Switch: specific")
parser.add_argument("--password", help="Password. Switch: specific")
parser.add_argument("--save", help="Save calculated data to database. Switch: Yes")

# Calculation specific arguments
parser.add_argument("--std_hor", help="Standard deviance horizon. Switch: specific")
parser.add_argument("--weights", help="Weights of simulated securities. Switch: list of weights")
parser.add_argument("--sec", help="List of securites. Switch: list of securites")

# -------------------- #
#  DRAWDOWN ARGUMENTS  #
# -------------------- #

args = parser.parse_args()


class EqPortVar:

    def __init__(self, db, user_name, password, port_date=None, portfolio=None, std_dev_hor="daily"):

        print("********************************************")
        print("         PORTFOLIO VAR CALCULATION          ")
        print("********************************************")

        if portfolio is not None:

            print("PORTFOLIO: ", portfolio)

            self.port_data = SQL(data_base=db,
                                 user_name=user_name,
                                 password=password).select_data(select_query="""select ph.ticker, ph.portfolio_id, 
                                                                                ph.weight 
                                                                                from portfolio_holdings ph, portfolios p 
                                                                                where ph.portfolio_id = p.portfolio_id 
                                                                                                and ph.date = '{date}' 
                                                                                                and ph.type = 'EQUITY' 
                                                                        and p.portfolio_name = '{port}'""".format(
                port=portfolio,
                date=port_date))

            self.port_nav = SQL(data_base=db,
                                user_name=user_name,
                                password=password).select_data(select_query="""select pn.total_nav 
                                                                               from portfolio_nav pn, portfolios p 
                                                                               where pn.portfolio_code = p.portfolio_id 
                                                                                               and pn.date = '{date}' 
                                                                        and p.portfolio_name = '{port}'""".format(
                port=portfolio,
                date=port_date))

        else:

            print("PORTFOLIO: SIMULATION")

            self.wh = str(args.weights)
            self.wh = self.wh.replace("[", "").replace("]", "").replace(",", "").split()
            self.wh = [float(wh) for wh in self.wh]

            self.securities = str(args.sec)
            self.securities = self.securities.replace("[", "").replace("]", "").replace(",", "").split()
            self.port_data = pd.DataFrame({"ticker": list(self.securities),
                                           "weight": self.wh})
            self.port_nav = pd.DataFrame({"total_nav": [1000]})

        if (port_date is None) and (portfolio is not None):
            print("Portfolio date input is missing ! Stop calculation!")
        else:
            print("PORTFOLIO POSITIONS")
            print(self.port_data)
            print("")
            print("NAV:", list(self.port_nav["total_nav"])[0])

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

            self.port_var_99 = self.port_nav*self.trading_days*2.33*self.port_std_dev

            print(len("VAR 99 Value: " + str(list(self.port_var_99["total_nav"])[0]))*"=")
            print("VAR 99 Value: " + str(list(self.port_var_99["total_nav"])[0]))
            print("VAR 99 %:", list(self.port_var_99["total_nav"])[0]/list(self.port_nav["total_nav"])[0])
            print(len("VAR 99 Value: " + str(list(self.port_var_99["total_nav"])[0])) * "=")

            self.port_var_95 = self.port_nav * self.trading_days * 1.65 * self.port_std_dev

            print(len("VAR 95 Value: " + str(list(self.port_var_95["total_nav"])[0])) * "=")
            print("VAR 95 Value: " + str(list(self.port_var_95["total_nav"])[0]))
            print("VAR 95 %:", list(self.port_var_95["total_nav"])[0] / list(self.port_nav["total_nav"])[0])
            print(len("VAR 95 Value: " + str(list(self.port_var_95["total_nav"])[0])) * "=")

    def save_var(self):

        print("Saving calculated records to database...")

        SQL(data_base=args.db,
            user_name=args.user_name,
            password=args.password).insert_data(insert_query="""update portfolio_nav 
                                                                set d_var_95 = {var_95},
                                                                d_var_99 = {var_99},
                                                                d_var_95_p = {var_95_p},
                                                                d_var_99_p = {var_99_p}
                                                                where date = '{date}' 
                                and portfolio_code={port_code}""".format(var_95=list(self.port_var_95["total_nav"])[0],
                         var_99=float(list(self.port_var_99["total_nav"])[0]),
                         var_95_p=float(list(self.port_var_95["total_nav"])[0] / list(self.port_nav["total_nav"])[0]),
                         var_99_p=float(list(self.port_var_99["total_nav"])[0]/list(self.port_nav["total_nav"])[0]),
                         date=args.date,
                         port_code=list(self.port_data["portfolio_id"])[0]))


class PortDrawDown:

    def __init__(self, db, user_name, portfolio, password,):

        self.port_nav = SQL(data_base=db,
                            user_name=user_name,
                            password=password).select_data(select_query="""select pn.total_nav, pn.aum from
                                                                           portfolio_nav pn, portfolios p
                                                                           where pn.portfolio_code = p.portfolio_id 
                                                    and p.portfolio_name = '{port_name}'""".format(port_name=portfolio))

    def nav_drawdown(self):

        self.nav_values = list(self.port_nav["total_nav"])[1:]
        self.nav_dd = round((1-(self.nav_values[-1]/np.max(self.nav_values)))*100, 2)

        return self.nav_dd

    def aum_drawdown(self):

        self.aum_values = list(self.port_nav["aum"])[1:]
        self.aum_dd = round((1 - (self.aum_values[-1] / np.max(self.aum_values))) * 100, 2)

        return self.aum_dd


if __name__ == "__main__":

    if args.var == "Yes":

        var = EqPortVar(db=args.db,
                        user_name=args.user_name,
                        password=args.password,
                        portfolio=args.port,
                        port_date=args.date)

        if args.save == "Yes":

            var.save_var()






