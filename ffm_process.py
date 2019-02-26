import argparse
import time
from FFM_SYSTEM.ffm_data import *
from datetime import date
from datetime import timedelta
from _datetime import datetime
import os

# ----------------- #
#    ARGUMENTS      #
# ----------------- #

parser = argparse.ArgumentParser()

# General data points

parser.add_argument("--rundate", help="Specifies on which date to run production. Switch: specific")
parser.add_argument("--equity_ticker", help="Defining the list of equity tickers or single ticker to "
                                     "produce data. Switches: ALL - All tickers; Specific ticker code",)
parser.add_argument("--portfolio", help="Specifies on which portfolio to run ffm_processes. "
                                        "Switch: All - All portfolios"
                                        "Switch: FUND - Specific fund")

# Database related switches

parser.add_argument("--db_user_name", help="User name for database login. Switch: username")
parser.add_argument("--db_password", help="Password for database login. Switch: password")
parser.add_argument("--env", help="Environment switch. Default:prod; Switches: dev ")

# Process related switches

parser.add_argument("--ied_download", help="Intraday equity data download. Switch: Yes")
parser.add_argument("--pos_calc", help="Calculates positions from trade data within a portfolio. Switch: Yes")

args = parser.parse_args()


class FfmProcess:

    """
    Collection of FFM SYS main processes
    """

    def __init__(self):

        # Date definition

        self.date0 = time.strftime("%Y:%m:%d")
        self.day = time.strftime("%A")
        self.begtime = time.strftime("%H:%M:%S")
        self.today = date.today()
        self.portfolios = ""
        self.trades = ""

        if args.rundate is not None:

            self.portdate1 = args.rundate
            self.portdate = datetime.date(datetime(year=int(self.portdate1[0:4]),
                                                   month=int(self.portdate1[4:6]),
                                                   day=int(self.portdate1[6:8])))
            self.weekday = self.portdate.weekday()

        else:

            if self.today.weekday() == 0:

                if self.begtime > "22:18:00":
                    self.portdate = self.today
                else:
                    self.delta = timedelta(days=-3)
                    self.portdate = self.today + self.delta

            elif self.today.weekday() == 6:

                self.delta = timedelta(days=-2)
                self.portdate = self.today + self.delta

            elif self.today.weekday() == 5:

                self.delta = timedelta(days=-1)
                self.portdate = self.today + self.delta

            else:

                if self.begtime < "15:00:00":
                    self.delta = timedelta(days=-1)
                    self.portdate = self.today + self.delta
                else:
                    self.portdate = self.today

        # Environment definiton

        if args.env == "dev":
            self.data_base = "dev_ffm_sys"
        else:
            self.data_base = "ffm_sys"

        # SQL query date

        self.query_date0 = str(self.portdate)
        self.query_date = self.query_date0[0:4] + self.query_date0[5:7] + self.query_date0[8:10]

        # SQL data base connection session start

        self.sql_connection = SQL(data_base=self.data_base,
                                  user_name=args.db_user_name,
                                  password=args.db_password)

        # Equity ticker definition

        if args.equity_ticker == "All":

            self.equity_tickers = list(self.sql_connection.select_data("""select ticker 
                                                                          from dev_ffm_sys.sec_info 
                                                                          where type = 'EQUITY'""")['ticker'])
        else:
            self.equity_tickers = [args.equity_ticker]

        print("********************************************")
        print("           DAILY DATA PRODUCTION            ")
        print("********************************************")
        print("-----------------")
        print("* DAY PARAMTERS *")
        print("-----------------")
        print("Day: " + self.day)
        print("Start time: " + self.begtime)
        print("Current date: " + self.date0)
        print("Portfolio date: " + str(self.portdate))
        print("SQL query date: " + str(self.query_date))
        print("Environment: " + str(self.data_base))
        print("")

    def position_calc(self):

        print("********************************************")
        print("       PORTFOLIO POSITION CALCULATOR        ")
        print("********************************************")

        if args.portfolio == "ALL":

            self.portfolios = self.sql_connection.select_data(select_query="""select portfolio_name, portfolio_id from portfolios 
                                                                              where terminate is null 
                                                                              and portfolio_group = 'No'""")
            print(self.portfolios)
            print("")

        else:
            self.portfolios = self.sql_connection.select_data(select_query="""select portfolio_name, portfolio_id from portfolios 
                                                                              where terminate is null 
                                                                              and portfolio_group = 'No'
                                                and portfolio_name = '{port_name}'""".format(port_name=args.portfolio))
            print(self.portfolios)
            print("")

        for portfolio, port_id in zip(list(self.portfolios["portfolio_name"]), list(self.portfolios["portfolio_id"])):

            print("Clearing out previous position records as of " +
                  str(self.query_date) + " for " + str(list(self.portfolios["portfolio_name"])[0]))

            self.sql_connection.insert_data(insert_query="""delete from positions 
                                                                    where date = '{date}' 
                                   and portfolio_code = '{port_code}'""".format(date=self.query_date,
                                                                                port_code=port_id))

            print("Quering out trades for "+str(portfolio))

            self.trades = self.sql_connection.select_data(select_query="""select*from trade t, portfolios p 
                                                                          where t.portfolio_code = p.portfolio_id 
                                                                          and t.status = 'OPEN'
                                                                          and p.portfolio_name='{port_name}'""".format(
                                                                          port_name=portfolio))

            print("Processing trades...")

            for trade in self.trades.index.values:

                self.trade = self.trades.iloc[trade]

                if self.trade["side"] == "BUY":
                    self.quantity = self.trade["quantity"]
                else:
                    self.quantity = self.trade["quantity"]*-1

                print("Date:", self.query_date,
                      "Port Code:", self.trade["portfolio_code"],
                      "Strat Code", self.trade["strategy_code"],
                      "Quantity:", self.quantity,
                      "Trade Price:", self.trade["trade_price"],
                      "Sec ID:", self.trade["sec_id"])

                Entries(data_base=self.data_base,
                        user_name=args.db_user_name,
                        password=args.db_password).positions(date=self.query_date,
                                                             portfolio_code=self.trade["portfolio_code"],
                                                             strategy_code=self.trade["strategy_code"],
                                                             quantity=self.quantity,
                                                             trade_price=self.trade["trade_price"],
                                                             sec_id=self.trade["sec_id"])

                if self.trade["side"] == "SELL":

                    Entries(data_base=self.data_base,
                            user_name=args.db_user_name,
                            password=args.db_password).positions(date=self.query_date,
                                                                 portfolio_code=self.trade["portfolio_code"],
                                                                 strategy_code=self.trade["strategy_code"],
                                                                 quantity=(self.quantity*self.trade["trade_price"])/100,
                                                                 trade_price=100,
                                                                 sec_id=201)

                if self.trade["leverage"] == "Yes":

                    print("Leveraged trade")

                    Entries(data_base=self.data_base,
                            user_name=args.db_user_name,
                            password=args.db_password).positions(date=self.query_date,
                                                                 portfolio_code=self.trade["portfolio_code"],
                                                                 strategy_code=self.trade["strategy_code"],
                                                                 quantity=(self.trade["trade_price"]*self.trade["quantity"])*(self.trade["leverage_perc"]/100)/100,
                                                                 trade_price=100,
                                                                 sec_id=200)

            print("")


    def open_position_calc(self):
        pass

    def security_return_calc(self):
        pass

    def security_risk_calc(self):
        pass

    def intraday_equity_price_download(self):

        print("------------------------------------------------")
        print("* IEX EQUITY INTRADAY PRICE AND QUOTE DOWNLOAD *")
        print("------------------------------------------------")
        print("")
        print("TICKERS:")
        print(self.equity_tickers)

        for equity_ticker in self.equity_tickers:

            if self.sql_connection.select_data("""select * 
                            from process_monitor 
                            where ticker = '{tkr}' 
                            and date = '{dt}'""".format(tkr=equity_ticker,
                                                        dt=self.query_date))["intraday_data_download"].values == "Yes":

                print("Record exists in database for " + str(equity_ticker) + " as of " + str(self.query_date))

            else:

                try:
                    self.eq_ticker_query = OnlineData(equity_ticker).import_intraday_quote_to_database(self.query_date)

                    self.sql_connection.insert_data(self.eq_ticker_query)
                    self.sql_connection.insert_data("""insert into process_monitor (ticker, intraday_data_download,date) 
                                                       
                                                       values ('{ticker}', 
                                                               '{data}', 
                                                               '{date}')""".format(ticker=equity_ticker,
                                                                                   data="Yes",
                                                                                   date=self.query_date))

                    print("Downloading data for " + str(equity_ticker) +
                          " -> DOWNLOADED AND INSERTED INTO " + str(self.data_base))
                except:

                    print("Error while downloading data or inserting data into database! " + str(equity_ticker))

    def close_process(self):

        self.sql_connection.close_connection()


if __name__ == "__main__":

    ffm_process = FfmProcess()

    if args.pos_calc == "Yes":

        ffm_process.position_calc()


