import argparse
import time
from FFM_SYSTEM.ffm_data import *
from datetime import date
from datetime import timedelta
from _datetime import datetime
import datetime
from pandas.tseries.offsets import BDay
import os

# ----------------- #
#    ARGUMENTS      #
# ----------------- #

parser = argparse.ArgumentParser()

# General data points

parser.add_argument("--rundate", help="Specifies on which date to run production. Switch: specific")
parser.add_argument("--start_date", help="Start Date. Switch: specific")
parser.add_argument("--equity_ticker", help="Defining the list of equity tickers or single ticker to "
                                     "produce data. Switches: ALL - All tickers; Specific ticker code",)
parser.add_argument("--portfolio", help="Specifies on which portfolio to run ffm_processes. "
                                        "Switch: All - All portfolios"
                                        "Switch: FUND - Specific fund")

parser.add_argument("--strategy", help="Imports strategy data from db. Switch: Name of the strategy")

# Database related switches

parser.add_argument("--db_user_name", help="User name for database login. Switch: username")
parser.add_argument("--db_password", help="Password for database login. Switch: password")
parser.add_argument("--env", help="Environment switch. Default:prod; Switches: dev ")
parser.add_argument("--import_table", help="Imports table to database. Switch: Yes")
parser.add_argument("--table_file", help="Name of the table file.")
parser.add_argument("--table_file_path", help="Location of the table file.")

# Process related switches

parser.add_argument("--ied_download", help="Intraday equity data download. Switch: Yes")
parser.add_argument("--pos_calc", help="Calculates positions from trade data within a portfolio. Switch: Yes")
parser.add_argument("--nav_calc", help="Calculates portfolios NAV. Switch: Yes")
parser.add_argument("--live_nav", help="Calculates portfolios NAV with latest prices. Switch: Yes")
parser.add_argument("--hold_calc", help="Calculates portfolios holding data. Switch: Yes")
parser.add_argument("--ncf", help="Portfolio Net Cash Flow calculation. Switch: Yes")

# Broker data load processes

parser.add_argument("--broker_file", help="Name of the broker report file. Switch: name of the file")
parser.add_argument("--broker", help="Name of the broker. Switch: name of the broker")
parser.add_argument("--daytrade", help="Processes daytrade data. Switch: name of the broker")
parser.add_argument("--dt_sec_type", help="Daytrade security type to process only. Switch: Type of security")

args = parser.parse_args()

class FfmProcess:

    """
    Collection of FFM SYS main processes
    """

    def __init__(self):

        pd.set_option('display.max_rows', 500)
        pd.set_option('display.max_columns', 500)
        pd.set_option('display.width', 1000)

        # Date definition

        self.date0 = time.strftime("%Y:%m:%d")
        self.day = time.strftime("%A")
        self.begtime = time.strftime("%H:%M:%S")
        self.today = date.today()
        self.portfolios = ""
        self.trades = ""

        if args.rundate is not None:

            self.portdate1 = args.rundate

            self.portdate = datetime.date(year=int(self.portdate1[0:4]),
                                          month=int(self.portdate1[4:6]),
                                          day=int(self.portdate1[6:8]))

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
        self.query_date_1 = str(self.portdate - BDay(1))
        self.query_date_1 = self.query_date_1[0:4] + self.query_date_1[5:7] + self.query_date_1[8:10]

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
        print("SQL query date -1: " + str(self.query_date_1))
        print("Environment: " + str(self.data_base))
        print("")

    def import_tables(self):

        """
        Process which imports and amends table structure. Recommended for initial table setup
        :return:
        """

        if args.table_file is None:
            print("Table file name is missing! Process stopped!")
        elif args.table_file_path is None:
            print("Table file location is missing! Process stopped!")
        else:
            self.db_import_cmd = """mysql --protocol=tcp --host=localhost --user={user_name} --port=3306 --default-character-set=utf8 --comments --database={to_db}  < '{file_path}{table_name_file}' --password={password}""".format(user_name=args.db_user_name, to_db=self.data_base, file_path=args.table_file_path, table_name_file=args.table_file, password=args.db_password)

            print("Executing table structure import command on", self.data_base, "database... Amending table->", str(args.table_file)[12:-4])

            os.system(command=self.db_import_cmd)

            return self.db_import_cmd

    def net_cash_flow(self):

        print("********************************************")
        print("    PORTFOLIO NET CASH FLOW CALCULATOR      ")
        print("********************************************")

        if self.portdate.weekday() == 6 or self.portdate.weekday() == 5:
            print("WEEKEND ! POSITIONS CALCULATION IS SHUT DOWN!")
        else:
            self.chf = self.sql_connection.select_data(select_query="""select*from cash_flow cf, portfolios p 
                                                                       where p.portfolio_id = cf.portfolio_code 
                                                                       and p.portfolio_name = '{port}' 
                                                                       and cf.date between '{start_date}'
                                                                       and '{end_date}'""".format(port=args.portfolio,
                                                                                                  start_date=args.start_date,
                                                                                                  end_date=args.rundate))
            print(self.chf)

            self.start_date = date(year=int(args.start_date[0:4]),
                                   month=int(args.start_date[4:6]),
                                   day=int(args.start_date[6:]))

            self.end_date = date(year=int(args.rundate[0:4]),
                                   month=int(args.rundate[4:6]),
                                   day=int(args.rundate[6:]))

            self.cf_list = []

            while self.start_date <= self.end_date:

                self.chf_frame =self.chf[self.chf["date"] == self.start_date]
                self.net_chf = sum(list(self.chf_frame["ammount"]))
                self.cf_list.append(self.net_chf)
                self.start_date = self.start_date + BDay(1)
                self.start_date = self.start_date.date()

        return self.cf_list

    def position_calc(self):

        print("********************************************")
        print("       PORTFOLIO POSITION CALCULATOR        ")
        print("********************************************")

        if self.portdate.weekday() == 6 or self.portdate.weekday() == 5:
            print("WEEKEND ! POSITIONS CALCULATION IS SHUT DOWN!")
        else:

            self.collaterals = self.sql_connection.select_data(select_query="""select*from sec_info 
                                                                               where type = 'LOAN' 
                                                                               and ticker in ('MRGN', 'CLTR')""")

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

                self.port_text = "PORTFOLIO: " + str(portfolio)

                print(len(self.port_text)*"*")
                print(self.port_text)
                print(len(self.port_text)*"*")
                print("")
                print("Clearing out previous position records as of " +
                      str(self.query_date) + " for " + str(portfolio))

                self.sql_connection.insert_data(insert_query="""delete from positions 
                                                                        where date = '{date}' 
                                       and portfolio_code = '{port_code}'""".format(date=self.query_date,
                                                                                    port_code=port_id))

                print("")
                print("T-2 POSITIONS:")

                self.t_min_one_pos = self.sql_connection.select_data(select_query="""select p.pos_id, p.sec_id, 
                                                                p.portfolio_code, p.strategy_code, p.open_bal, p.close_bal, 
                                                                s.name, s.ticker from positions p, sec_info s
                                                                where p.sec_id = s.sec_id 
                                                                and p.date = '{date_1}'
                                                                and p.portfolio_code = '{port_code}'""".format(date_1=self.query_date_1,
                                                                                                               port_code=port_id))

                print(self.t_min_one_pos)
                print("")
                print("Quering out new trades...")
                print("NEW TRADES:")

                self.trades = self.sql_connection.select_data(select_query="""select*from trade 
                                                                              where date = '{date}' 
                                                                              and portfolio_code = '{port_id}'""".format(
                                                                                                      port_id=port_id,
                                                                                                      date=self.query_date))

                self.filtered_sec_ids = list(set(list(self.trades["sec_id"])))
                print(self.trades)
                print(list(set(list(self.trades["sec_id"]))))
                print("")

                if (len(list(self.t_min_one_pos["pos_id"])) == 0) and len(list(self.trades["trade_id"])) == 0:
                    print("PORTFOLIO DOES NOT HAVE ANY POSITIONS AND TRADES AS OF", self.query_date)
                    print("")
                else:
                    # Processing existing positions

                    print("PROCESSING EXISTING POSITIONS AND CALCULATING POSITION BALANCE")
                    print("")

                    for pos in range(len(self.t_min_one_pos["pos_id"])):
                        self.pos = self.t_min_one_pos.iloc[pos]
                        self.trade = self.trades[self.trades["sec_id"] == self.pos["sec_id"]]
                        self.close_bal = sum(list(self.trade["quantity"]))

                        if (self.pos["name"] == "Margin") or (self.pos["name"] == "Collateral"):
                            pass
                        else:
                            self.new_bal = self.close_bal

                            print("Security:", self.pos["name"])
                            print("New trade total quantity:", self.close_bal)
                            print("T-2 balance:", self.pos["close_bal"])
                            print("Close balance:", self.new_bal+self.pos["close_bal"])
                            print("Writing data to data base")

                            if self.pos["close_bal"] == 0:
                                print(self.pos["name"], "was traded out from the portfolio on previous day!")
                            else:
                                Entries(data_base=self.data_base,
                                        user_name=args.db_user_name,
                                        password=args.db_password).positions(date=self.query_date,
                                                                             portfolio_code=self.pos["portfolio_code"],
                                                                             strategy_code=self.pos["strategy_code"],
                                                                             open_bal=self.pos["close_bal"],
                                                                             close_bal=self.new_bal+self.pos["close_bal"],
                                                                             sec_id=self.pos["sec_id"])
                            print("")

                    print("PROCESSING NEW TRADES AND CALCULATING POSITION BALANCE")
                    print("")

                    for trade in list(set(list(self.trades["sec_id"]))):

                        self.tr = self.trades[self.trades["sec_id"] == trade]
                        self.ps = self.t_min_one_pos[self.t_min_one_pos["sec_id"] == trade]

                        if sum(self.tr["quantity"]) == 0:
                            print(list(self.tr["ticker"])[0], ": DAYTRADE! CLOSE BALANCE -> 0")
                            print("")
                        else:
                            if len(list(self.ps["pos_id"])) >= 1:
                                pass
                            else:
                                print("Security:", list(self.tr["ticker"])[0])
                                print("T-2 balance: 0")
                                print("Close balance:", sum(self.tr["quantity"]))
                                print("Margin:", list(self.tr["margin_bal"])[0])
                                print("Writing data to data base")
                                print("")

                                Entries(data_base=self.data_base,
                                        user_name=args.db_user_name,
                                        password=args.db_password).positions(date=self.query_date,
                                                                             portfolio_code=list(self.tr["portfolio_code"])[0],
                                                                             strategy_code=list(self.tr["strategy_code"])[0],
                                                                             open_bal=0,
                                                                             close_bal=sum(self.tr["quantity"]),
                                                                             sec_id=list(self.tr["sec_id"])[0])



                    print("MARGIN POSITION CALCULATION")
                    print("")

                    self.margin_filter = self.t_min_one_pos[self.t_min_one_pos["name"] == "Margin"]

                    if len(list(self.margin_filter["name"])) == 0:
                        self.open_margin = 0
                    else:
                        self.open_margin = list(self.margin_filter["close_bal"])[0]

                    print("New trade total quantity:", sum(list(self.trades["margin_bal"])))
                    print("T-2 balance:", self.open_margin)
                    print("Close balance:", sum(list(self.trades["margin_bal"]))+self.open_margin)
                    print("Writing data to data base")

                    if len(self.trades["portfolio_code"]) == 0:
                        self.port_code = list(self.t_min_one_pos["portfolio_code"])[0]
                        self.strat_code = list(self.t_min_one_pos["strategy_code"])[0]
                    else:
                        self.port_code = list(self.trades["portfolio_code"])[0]
                        self.strat_code = list(self.trades["strategy_code"])[0]

                    self.margin_id = self.collaterals[self.collaterals["ticker"] == "MRGN" ]

                    Entries(data_base=self.data_base,
                            user_name=args.db_user_name,
                            password=args.db_password).positions(date=self.query_date,
                                                                 portfolio_code=self.port_code,
                                                                 strategy_code=self.strat_code,
                                                                 open_bal=self.open_margin,
                                                                 close_bal=sum(list(self.trades["margin_bal"]))+self.open_margin,
                                                                 sec_id=list(self.margin_id["sec_id"])[0])

                    print("")

                    print("COLLATERAL POSITION CALCULATION")
                    print("")

                    self.coll_filter = self.t_min_one_pos[self.t_min_one_pos["name"] == "Collateral"]

                    if len(list(self.coll_filter["name"])) == 0:
                        self.open_coll = 0
                    else:
                        self.open_coll = list(self.coll_filter["close_bal"])[0]

                    print("New trade total quantity:", sum(list(self.trades["collateral"])))
                    print("T-2 balance:", self.open_coll)
                    print("Close balance:", sum(list(self.trades["collateral"])) + self.open_coll)
                    print("Writing data to data base")

                    if len(self.trades["portfolio_code"]) == 0:
                        self.port_code = list(self.t_min_one_pos["portfolio_code"])[0]
                        self.strat_code = list(self.t_min_one_pos["strategy_code"])[0]
                    else:
                        self.port_code = list(self.trades["portfolio_code"])[0]
                        self.strat_code = list(self.trades["strategy_code"])[0]

                    self.coll_id = self.collaterals[self.collaterals["ticker"] == "CLTR"]

                    Entries(data_base=self.data_base,
                            user_name=args.db_user_name,
                            password=args.db_password).positions(date=self.query_date,
                                                                 portfolio_code=self.port_code,
                                                                 strategy_code=self.strat_code,
                                                                 open_bal=self.open_coll,
                                                                 close_bal=sum(list(
                                                                     self.trades["collateral"])) + self.open_coll,
                                                                 sec_id=list(self.coll_id["sec_id"])[0])

                    print("")

    def nav_calc(self):

        print("********************************************")
        print("       PORTFOLIO NAV CALCULATOR        ")
        print("********************************************")

        if self.portdate.weekday() == 6 or self.portdate.weekday() == 5:
            print("WEEKEND ! PORTFOLIO NAV CALCULATION IS SHUT DOWN!")
        else:

            self.all_positions = self.sql_connection.select_data(select_query="""select p.date, p.portfolio_code, p.close_bal, s.ticker, s.type 
                                                                             from positions p, sec_info s 
                                                                             where p.sec_id = s.sec_id 
                                                                    and p.date = '{date}'""".format(date=self.query_date))
            print(self.all_positions)
            self.all_cash_flow = self.sql_connection.select_data(select_query="""select*from cash_flow 
                                                                      where date = '{date}'""".format(date=self.query_date))

            self.all_cash_flow_1 = self.sql_connection.select_data(select_query="""select*from cash_flow 
                                                                              where date < '{date}'""".format(
                                                                                                    date=self.query_date))

            if args.portfolio == "ALL":

                self.portfolios = self.sql_connection.select_data(select_query="""select portfolio_name, portfolio_id, inception_date
                                                                                  from portfolios 
                                                                                  where terminate is null 
                                                                                  and portfolio_group = 'No'""")
                print(self.portfolios)
                print("")

            else:
                self.portfolios = self.sql_connection.select_data(select_query="""select portfolio_name, portfolio_id, inception_date 
                                                                                  from portfolios 
                                                                                  where terminate is null 
                                                                                  and portfolio_group = 'No'
                                                            and portfolio_name = '{port_name}'""".format(
                                                                                                port_name=args.portfolio))
                print(self.portfolios)
                print("")

            for port_id in list(self.portfolios["portfolio_id"]):

                print("Clearing out previous record as of " + str(self.query_date) + " for portfolio_id: " + str(port_id))

                self.sql_connection.insert_data(insert_query="""delete from portfolio_nav where date = '{date}' 
                                                                    and portfolio_code = '{port_code}'""".format(
                                                                                                    date=self.query_date,
                                                                                                    port_code=port_id))

            print("")
            print("-------------------------------")
            print("  Starting NAV calculations   ")
            print("--------------------------------")
            print("")

            for port_id in list(self.portfolios["portfolio_id"]):

                self.port_incep_date = self.portfolios[self.portfolios["portfolio_id"] == port_id]

                if self.portdate < list(self.port_incep_date["inception_date"])[0]:
                    print("Calculation date is less then portfolio inception date!")
                    print("")
                else:

                    self.query_text = "   Quering out positions for " + str(port_id) + " as of " + str(self.query_date)+str("   ")

                    print(len(self.query_text)*"*")
                    print(self.query_text)
                    print(len(self.query_text) * "*")
                    print("HOLDING NAV CALCULATION")
                    print("")

                    self.positions = self.all_positions[self.all_positions["portfolio_code"] == port_id]

                    print(self.positions)
                    print("")

                    self.market_value = 0
                    self.aum_value = 0

                    for quantity, ticker in zip(list(self.positions["close_bal"]), list(self.positions["ticker"])):

                        # NAV

                        if (ticker == "MRGN") or (ticker == "CLTR"):
                            self.price = 1
                        else:

                            # NAV calculation with latest share prices

                            if args.live_nav == "Yes":
                                self.price = OnlineData(ticker=ticker).last_eq_price()
                                self.price = list(self.price["price"])[0]
                            else:

                                # NAV calculation with the selected date's price

                                self.price = OnlineData(ticker=ticker).get_one_year_prices()
                                self.price = self.price[self.price["date"] == str(self.query_date)]
                                self.price = list(self.price["close"])[0]

                        self.market_value = self.market_value + (quantity*self.price)

                        # AUM

                        if ticker == "MRGN":
                            self.aum_price = 0
                        elif ticker == "CLTR":
                            self.aum_price = 1
                        else:
                            self.aum_price = self.price

                        self.aum_value = self.aum_value + (quantity*self.aum_price)

                        print("MV: " + str(ticker) + " " + str(round(quantity * self.price, 2))+" Cumulative MV: "+str(self.market_value), "| Quantity: ", quantity, "Price: ", self.price)

                    self.market_value = round(self.market_value, 2)

                    print(len(self.query_text) * "-")
                    print("Holding NAV: " + str(self.market_value))
                    print("Holding AUM: " + str(self.aum_value))
                    print(len(self.query_text)*"-")

                    print("CASH BALANCE CALCULATION")
                    print("")

                    self.cash_flow = self.all_cash_flow[self.all_cash_flow["portfolio_code"] == port_id]
                    self.cash_flow_1 = self.all_cash_flow_1[self.all_cash_flow_1["portfolio_code"] == port_id]

                    cash_flow_balance = sum(list(self.cash_flow["ammount"])) + sum(list(self.cash_flow_1["ammount"]))

                    print("T-2 Cash Balance: "+str(sum(list(self.cash_flow_1["ammount"]))))
                    print("T-1 Cash Flow: "+str(sum(list(self.cash_flow["ammount"]))))
                    print(len(self.query_text) * "-")
                    print("Cash balance -> " + str(cash_flow_balance))
                    print(len(self.query_text)*"-")

                    self.id = self.sql_connection.select_data(select_query="""select*from portfolio_nav""")
                    try:
                        self.port_lev_per = (round((self.aum_value+cash_flow_balance)/(self.market_value+cash_flow_balance), 3)*100)-100
                    except:
                        self.port_lev_per = 0

                    print(len(self.query_text) * "=")
                    print("Total NAV: " + str(self.market_value + cash_flow_balance))
                    print("Total AUM: " + str(self.aum_value + cash_flow_balance))
                    print("Portfolio Leverage: " + str(self.port_lev_per) + " %")
                    print(len(self.query_text)*"=")
                    print("")
                    print("Writing calculated portfolio NAV data to database.")
                    print("")

                    if len(self.id["nav_id"]) < 1:
                        self.nav_id = 1
                    else:
                        self.nav_id = list(self.id["nav_id"])[-1]+1

                    self.sql_connection.insert_data(insert_query="""insert into portfolio_nav (date, portfolio_code, 
                                                                    holding_nav, nav_id, cash_balance, total_nav, 
                                                                    aum, port_lev_perc) 
                                                                    values ('{date}', '{port_code}', '{holding_nav}', 
             '{nav_id}', '{cash_bal}', '{tot_nav}', '{aum}', '{lev_perc}')""".format(date=self.query_date,
                                                                                     port_code=port_id,
                                                                                     holding_nav=self.market_value,
                                                                                     nav_id=self.nav_id,
                                                                                     cash_bal=cash_flow_balance,
                                                                                     tot_nav=self.market_value+cash_flow_balance,
                                                                                     aum=self.aum_value + cash_flow_balance,
                                                                                     lev_perc=self.port_lev_per))

    def portfolio_holding_calc(self):

        print("********************************************")
        print("       PORTFOLIO HOLDING CALCULATOR        ")
        print("********************************************")

        if self.portdate.weekday() == 6 or self.portdate.weekday() == 5:
            print("WEEKEND ! PORTFOLIO NAV CALCULATION IS SHUT DOWN!")
        else:
            if args.portfolio == "ALL":

                self.portfolios = self.sql_connection.select_data(select_query="""select portfolio_name, portfolio_id, inception_date
                                                                                  from portfolios 
                                                                                  where terminate is null 
                                                                                  and portfolio_group = 'No'""")
                print(self.portfolios)
                print("")

            else:
                self.portfolios = self.sql_connection.select_data(select_query="""select portfolio_name, portfolio_id, inception_date 
                                                                                  from portfolios 
                                                                                  where terminate is null 
                                                                                  and portfolio_group = 'No'
                                                            and portfolio_name = '{port_name}'""".format(
                                                                                                port_name=args.portfolio))
                print(self.portfolios)
                print("")

            for port_id in list(self.portfolios["portfolio_id"]):

                print("Clearing out previous holding record as of " + str(self.query_date) + " for portfolio_id: " + str(port_id))

                self.sql_connection.insert_data(insert_query="""delete from portfolio_holdings where date = '{date}' 
                                                                and portfolio_id = '{port_code}'""".format(
                                                                                                   date=self.query_date,
                                                                                                   port_code=port_id))

            for port_id in list(self.portfolios["portfolio_id"]):

                print("")
                print("===============================================")
                print("PORTFOLIO CODE:", port_id)
                print("===============================================")
                print("---------------------------------------")
                print("   Positions Valuations Calculations   ")
                print("---------------------------------------")
                print("")

                self.port_incep_date = self.portfolios[self.portfolios["portfolio_id"] == port_id]

                if self.portdate < list(self.port_incep_date["inception_date"])[0]:
                    print("Calculation date is less then portfolio inception date!")
                    print("")
                else:
                    self.nav_data = self.sql_connection.select_data(select_query="""select*from portfolio_nav 
                                                                                    where date = {date} 
                                                        and portfolio_code = {port_code}""".format(date=self.query_date,
                                                                                                   port_code=port_id))

                    if self.nav_data["total_nav"][0] == 0.0:
                        print("NAV is empty. Stop Portfolio Holding calculation")
                        print("")
                    else:
                        self.pos_sec_data = self.sql_connection.select_data(select_query="""select p.pos_id, p.date, 
                                                                                         p.portfolio_code, p.strategy_code, 
                                                                                         p.close_bal, s.sec_id, s.name, 
                                                                                         s.type, s.ticker, s.industry, 
                                                                                         s.sector, s.country
                                                                                         from positions p, sec_info s 
                                                                                            where p.sec_id = s.sec_id 
                                                                                            and p.date = '{date}' 
                                                        and p.portfolio_code = {port_id};""".format(date=self.query_date,
                                                                                                    port_id=port_id))

                        # Calculating pos_id number

                        self.pos_lenght = self.sql_connection.select_data(select_query="""SELECT MAX(pos_id) AS 'max_id' 
                                                                                          FROM portfolio_holdings""")

                        self.pos_lenght = self.pos_lenght["max_id"][0]

                        print("Data base position id starts from ", self.pos_lenght)
                        print("NAV:", self.nav_data["total_nav"][0])
                        print("Processing positions:")

                        # Security level calculations

                        for pos in range(len(list(self.pos_sec_data["pos_id"]))):

                            self.pos_sec = self.pos_sec_data.iloc[pos]

                            if (self.pos_sec["ticker"] == "MRGN") or (self.pos_sec["ticker"] == "CLTR"):
                                self.price = 1
                            else:
                                self.price = OnlineData(ticker=self.pos_sec["ticker"]).get_one_year_prices()
                                self.price = self.price[self.price["date"] == str(self.query_date)]
                                self.price = list(self.price["close"])[0]

                            print("Date:", self.query_date, "Pos ID:", self.pos_lenght + pos + 1, "Port ID:",
                                  self.pos_sec["portfolio_code"], "Strat Code:", self.pos_sec["strategy_code"],
                                  "Ticker:", self.pos_sec["ticker"], "Type:", self.pos_sec["type"],
                                  "Face:", self.pos_sec["close_bal"], "Price:", self.price,
                                  "MV:", self.price * self.pos_sec["close_bal"],
                                  "Weight:", ((self.price * self.pos_sec["close_bal"]) / self.nav_data["total_nav"][0]) * 100)

                            self.sql_connection.insert_data(insert_query="""insert into portfolio_holdings (date, pos_id, 
                                                                            portfolio_id, strategy_code, sec_id, name, 
                                                                            type, ticker, industry, sector, country, 
                                                                            face_value, current_price, market_value, weight)
                                                                            values ('{date}', '{pos_id}', 
                                                                            '{port_id}', '{strat_code}', '{sec_id}', 
                                                                            '{name}', '{type}', '{ticker}', '{industry}', 
                                                                            '{sector}', '{country}', '{face_value}', 
                                                                            '{price}', '{mv}', '{weight}')""".format(
                                date=self.query_date,
                                pos_id=self.pos_lenght + pos + 1,
                                port_id=self.pos_sec["portfolio_code"],
                                strat_code=self.pos_sec["strategy_code"],
                                sec_id=self.pos_sec["sec_id"],
                                name=self.pos_sec["name"],
                                type=self.pos_sec["type"],
                                ticker=self.pos_sec["ticker"],
                                industry=self.pos_sec["industry"],
                                sector=self.pos_sec["sector"],
                                country=self.pos_sec["country"],
                                face_value=self.pos_sec["close_bal"],
                                price=self.price,
                                mv=self.price * self.pos_sec["close_bal"],
                                weight=((self.price * self.pos_sec["close_bal"]) / self.nav_data["total_nav"][0]) * 100))

                        # Cash, margin calculation

                        print("Calculating Cash weight")

                        self.pos_lenght = self.sql_connection.select_data(select_query="""SELECT MAX(pos_id) AS 'max_id' 
                                                                                          FROM portfolio_holdings""")
                        self.pos_lenght = self.pos_lenght["max_id"][0]

                        print("Cash position ID starts from",self.pos_lenght)
                        print("Cash balance:", self.nav_data["cash_balance"][0])
                        print("Cash weight:", ((self.nav_data["cash_balance"][0]) / self.nav_data["total_nav"][0]) * 100)
                        print("Writing cash data to portfolio_holdings table")

                        self.sql_connection.insert_data(insert_query="""insert into portfolio_holdings (date, pos_id, 
                                                                            portfolio_id, strategy_code, sec_id, name, 
                                                                            type, ticker, industry, sector, country, 
                                                                            face_value, current_price, market_value, weight)
                                                                            values ('{date}', '{pos_id}', 
                                                                            '{port_id}', '{strat_code}', '{sec_id}', 
                                                                            '{name}', '{type}', '{ticker}', '{industry}', 
                                                                            '{sector}', '{country}', '{face_value}', 
                                                                            '{price}', '{mv}', '{weight}')""".format(
                                date=self.query_date,
                                pos_id=self.pos_lenght + 1,
                                port_id=self.pos_sec_data["portfolio_code"][0],
                                strat_code=self.pos_sec_data["strategy_code"][0],
                                sec_id=0,
                                name="Spendable Cash",
                                type="Cash Security",
                                ticker="CASH",
                                industry="-",
                                sector="-",
                                country="-",
                                face_value=self.nav_data["cash_balance"][0],
                                price=1,
                                mv=self.nav_data["cash_balance"][0],
                                weight=((self.nav_data["cash_balance"][0]) / self.nav_data["total_nav"][0]) * 100))

                        print("")

                        # Collateral calculation based on negative position sizes

                print("")
                print("---------------------------------------")
                print("   Positions Risk Calculations   ")
                print("---------------------------------------")
                print("")

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


class Broker:

    def __init__(self, broker):

        print("--------------------------")
        print("* BROKER DATA PROCESSING *")
        print("--------------------------")
        print("")

        self.broker = broker

        self.broker_file = """/home/apavlics/Developement/FFM_DEV/Codes/FFM_SYSTEM/Broker_data/{file}""".format(
            file=args.broker_file)

        print("Broker file:", self.broker_file)

        # Environment definiton

        if args.env == "dev":
            self.data_base = "dev_ffm_sys"
        else:
            self.data_base = "ffm_sys"

        self.sql_connection = SQL(data_base=self.data_base,
                                  user_name=args.db_user_name,
                                  password=args.db_password)

        self.strategy = self.sql_connection.select_data("""select*from strategy s, portfolios p 
                                                           where p.portfolio_id  = s.portfolio_code 
                                                           and s.strategy_name = '{strat_name}'""".format(
            strat_name=args.strategy))

        self.latest_trd_id = self.sql_connection.select_data("""SELECT MAX(trade_id) AS 'max_id' FROM trade""")
        self.latest_trd_id = self.latest_trd_id["max_id"][0]

        self.latest_trd_anal_id = self.sql_connection.select_data("""SELECT MAX(id) AS 'max_id' FROM trade_analysis""")
        self.latest_trd_anal_id = self.latest_trd_anal_id["max_id"][0]

        if self.latest_trd_anal_id is None:
            self.latest_trd_anal_id = 0

        print("Strategy Name:", self.strategy["strategy_name"][0])
        print("Strategy Code:", self.strategy["strategy_code"][0])
        print("Portfolio Code:", self.strategy["portfolio_code"][0])
        print("Trade Margin:", self.strategy["trade_margin"][0])
        print("Latest TRD ID:", self.latest_trd_id)
        print("Latest TRD Analysis ID:", self.latest_trd_anal_id)

        print("Broker:", self.broker)

        self.broker_process = self.sql_connection.select_data("""select b.strategy_name, b.data_type, b.latest_date, 
                                                                 b.broker_id from broker_processes b, broker_account ba 
                                                                 where b.broker_id=ba.broker_id 
                                                                 and ba.broker_name like '{broker}' 
                                                                 and b.strategy_name = '{strat}'""".format(
            broker=self.broker,
            strat=args.strategy))

        if len(self.broker_process["strategy_name"]) == 0:
            self.latest_intraday_date = self.strategy["inception_date"][0]
        else:
            self.latest_intraday_date = self.broker_process[self.broker_process["data_type"] == "INTRADAY"]
            self.latest_intraday_date = list(self.latest_intraday_date["latest_date"])[-1]

        # if len(self.broker_process["strategy_name"]) == 0 and self.broker_process["data_type"][0] == "COMISSION":
        #     self.latest_comm_date = self.strategy["inception_date"][0]
        # else:
        #     self.latest_comm_date = self.broker_process[self.broker_process["data_type"] == "COMISSION"]
        #     self.latest_comm_date = list(self.latest_comm_date["latest_date"])[-1]
        #
        # print("Latest commission calculation date:", self.latest_comm_date)
        print("Latest intraday calculation date:", self.latest_intraday_date)

        self.xl = pd.ExcelFile(self.broker_file)


class DayTrade(Broker):

    """
    Class to load and process the appropriate broker daytrade data to Trade and Trade analysis tables
    """

    def __init__(self, broker):
        super().__init__(broker)

    def etoro(self):

        self.df = self.xl.parse("Closed Positions")
        self.df = self.df[self.df["Position ID"] > 0]

        print("")
        print("TRADES")
        print(self.df)

        # Loading open positions into trade table
        print("")
        print("Loading and processing openening positions to trade table")

        self.trade_id_list = []
        self.record_date_list = []

        for record in range(len(list(self.df["Open Date"]))-1, 0, -1):

            self.trade = self.df.iloc[record]
            self.open_date = str(self.trade["Open Date"])[:10].replace("/", "")
            self.open_date = self.open_date[4:] + "-" + self.open_date[2:4] + "-" + self.open_date[0:2]

            self.close_date = str(self.trade["Open Date"])[:10].replace("/", "")
            self.close_date = self.close_date[4:] + "-" + self.close_date[2:4] + "-" + self.close_date[0:2]
            self.close_date = datetime.datetime.strptime(self.close_date[:10], '%Y-%m-%d')

            self.record_date = datetime.datetime.strptime(self.open_date[:10], '%Y-%m-%d')

            # Checking if trade is an intraday trade
            if str(self.close_date-self.record_date) == "0:00:00":

                # Checking if trade was already processed
                if self.record_date.date() <= self.latest_intraday_date:
                    print("Record was already processed:", self.record_date)
                else:
                    self.side = str(self.trade["Action"]).split()

                    self.security = self.sql_connection.select_data(select_query="""select*from broker_security_mapping bm, 
                                                                                    sec_info s 
                                                                                    where bm.ffm_sec_name = s.ticker 
                                                                                    and bm.br_sec_name = '{sec}'""".format(
                        sec=self.side[1]))

                    if len(self.security["sec_id"]) == 0:
                        print(self.side[1], " is not mapped in Broker Mapping Table!")
                    else:

                        if self.security["ffm_sec_type"][0] == args.dt_sec_type:

                            self.margin = float(self.trade["Units"]) * float(self.trade["Open Rate"]) * -1 * (
                                float(self.strategy["trade_margin"][0]))

                            if self.side[0] == "Buy":
                                self.db_side_type = "BUY_TO_OPEN"
                                self.db_side = "BUY"
                                self.collateral_bal = 0

                                self.cash_flow_ammount = (float(self.trade["Units"]) * float(
                                    self.trade["Open Rate"]) + self.margin) * -1
                                self.inflow_ammount = (float(self.trade["Units"]) * float(
                                    self.trade["Close Rate"]) + self.margin)
                            else:
                                self.db_side_type = "SELL_TO_OPEN"
                                self.db_side = "SELL"
                                self.collateral_bal = self.trade["Units"] * float(self.trade["Open Rate"]) * -2

                                self.cash_flow_ammount = (float(self.trade["Units"]) * float(
                                    self.trade["Open Rate"]) + self.margin)
                                self.inflow_ammount = (float(self.trade["Units"]) * float(
                                    self.trade["Close Rate"]) + self.margin) * -1

                            self.latest_trd_id = self.latest_trd_id + 1

                            print("New record:", "| TRD ID: ", self.latest_trd_id, "| Date:", self.record_date,
                                  "| Port Code:",
                                  self.strategy["portfolio_code"][0], "| Strat Code:",
                                  self.strategy["strategy_code"][0],
                                  "| Tran Type:", self.db_side_type, "| Sec:", self.side[1], "| Q:",
                                  self.trade["Units"],
                                  "| Price:", self.trade["Open Rate"], "| P&L:", self.trade["Profit"],
                                  "| Leverage: Yes",
                                  "| Lev %:", self.strategy["trade_margin"][0] * 100, "| Margin:", self.margin)

                            # Saving trade to trade table
                            self.insert_query = """insert into trade (trade_id, date, trade_num, portfolio_code,
                                                              strategy_code, side, quantity, trade_price,
                                                              leverage, status, sl, sl_level,
                                                              sec_id, leverage_perc, action, ticker, margin_bal, collateral)

                                           values ('{trade_id}',  '{date}',
                                                   '{trade_num}','{portfolio_code}',
                                                   '{strategy_code}',  '{side}',
                                                   '{quantity}', '{trade_price}',
                                                   '{leverage}', '{status}',
                                                   '{sl}', '{sl_level}',
                                                   '{sec_id}', '{leverage_perc}',
                                                   '{action}', '{ticker}','{mb}','{coll}')""".format(
                                trade_id=self.latest_trd_id,
                                date=self.record_date,
                                trade_num=-1,
                                portfolio_code=self.strategy["portfolio_code"][0],
                                strategy_code=self.strategy["strategy_code"][0],
                                side=self.db_side,
                                quantity=self.trade["Units"],
                                trade_price=self.trade["Open Rate"],
                                leverage="Yes",
                                status="OPEN",
                                sl="Yes",
                                sl_level=0,
                                sec_id=self.security["sec_id"][0],
                                leverage_perc=self.strategy["trade_margin"][0] * 100,
                                action=self.db_side_type,
                                ticker=self.security["ticker"][0],
                                mb=self.margin,
                                coll=self.collateral_bal)

                            # self.sql_connection.insert_data(insert_query=self.insert_query)

                            # Saving cash outflow movements into cash flow table

                            print("Cash Outflow:", self.cash_flow_ammount, "Cash Inflow:", self.inflow_ammount,
                                  "P&L:", self.inflow_ammount + self.cash_flow_ammount)

                            Entries(data_base=self.data_base,
                                    user_name=args.db_user_name,
                                    password=args.db_password).cash_flow(
                                                            port_code=self.strategy["portfolio_code"][0],
                                                            ammount=self.cash_flow_ammount,
                                                            cft="OUTFLOW",
                                                            date=self.record_date,
                                                            currency=self.strategy["currency"][0],
                                                            comment="Daytrade",
                                                            client="broker process")

                            Entries(data_base=self.data_base,
                                    user_name=args.db_user_name,
                                    password=args.db_password).cash_flow(
                                                            port_code=self.strategy["portfolio_code"][0],
                                                            ammount=self.inflow_ammount,
                                                            cft="INFLOW",
                                                            date=self.record_date,
                                                            currency=self.strategy["currency"][0],
                                                            comment="Daytrade",
                                                            client="broker process")

                            print("")

                            # Saving trade data to trade analysis table

                            self.latest_trd_anal_id = self.latest_trd_anal_id + 1

                            self.tr_insert_query = """insert into trade_analysis 
                                                     (trade_id, open_date, portfolio_id, strategy_id,
                                                      trd_price, quantity, sl, cost, sl_cost, status, sl_cost_to_nav, id, 
                                                      trd_duration, close_pnl) 

                                                      values ('{trd_id}', '{open_date}', '{portfolio_id}', '{strat_id}', 
                                                      '{trd_price}', '{quantity}', '{sl}', '{cost}', '{sl_cost}', 'CLOSED', 
                                                      '{slcn}','{id}', '{trd_dur}', '{cl_pnl}')""".format(
                                trd_id=self.latest_trd_id,
                                open_date=self.record_date,
                                portfolio_id=self.strategy["portfolio_code"][0],
                                strat_id=self.strategy["strategy_code"][0],
                                trd_price=self.trade["Open Rate"],
                                quantity=self.trade["Units"],
                                sl=0,
                                cost=0,
                                sl_cost=0,
                                slcn=0,
                                id=self.latest_trd_anal_id,
                                trd_dur=0,
                                cl_pnl=self.trade["Profit"])

                            self.sql_connection.insert_data(insert_query=self.tr_insert_query)

                            self.trade_id_list.append(self.latest_trd_id)
                        else:
                            print("Security cannot be processed in", str(args.strategy), "strategy!")

                self.record_date_list.append(self.record_date)

            else:
                print("Position is not an intraday trade!")

        print("Trade ID List:", self.trade_id_list)
        print("Latest Record Date:", self.record_date_list[-1])

        # Closing open daytrade positions in trade table
        print("Closing previously processed daytrades in trade table")

        print("Updating broker process table with new record.")
        self.process_id = self.sql_connection.select_data("""SELECT MAX(process_id) 
                                                             AS 'max_id' FROM broker_processes""")

        self.process_id = self.process_id["max_id"][0]

        if self.process_id is None:
            self.process_id = 0

        self.broker_id = self.sql_connection.select_data(select_query="""select * from broker_account 
                                                                         where strategy = '{strat}' 
                                                                         and broker_name like 'etoro'""".format(
            strat=args.strategy))

        self.sql_connection.insert_data(insert_query="""insert into broker_processes 
                                                        (process_id, broker_id, data_type, latest_date, 
                                                        date, strategy_name, sec_type) 
                                                        
                                                        values 
                                                        
                                                ({proc_id}, {br_id}, 'INTRADAY', '{latest_date}', 
                                                '{today}', '{strat}', '{sec_type}')""".format(
            proc_id=self.process_id+1,
            br_id=self.broker_id["broker_id"][0],
            latest_date=self.record_date_list[-1],
            today=date.today(),
            strat=args.strategy,
            sec_type=args.dt_sec_type))


class TradeAnalysis:

    """In this class trade and strategy analysis metrics can be found"""

    def __init__(self):
        pass


class TradeError(TradeAnalysis):

    def __init__(self):
        pass

    def know_market_dir(self):

        """This error measures if pre-defined trade risk is larger than it is allowed for the strategy compared to NAV.
        If within a trading day increasing number of trades occures with larger risk/pos represent this trading error"""

        pass

    def over_trading(self):

        """This check measures if over trading occured within the day."""

        pass


if __name__ == "__main__":

    ffm_process = FfmProcess()

    if args.pos_calc == "Yes":

        ffm_process.position_calc()

    if args.nav_calc == "Yes":

        ffm_process.nav_calc()

    if args.hold_calc == "Yes":

        ffm_process.portfolio_holding_calc()

    if args.ncf == "Yes":

        ffm_process.net_cash_flow()

    if args.import_table == "Yes":

        ffm_process.import_tables()

    if args.daytrade == "etoro":

        if args.broker_file is None:
            print("Broker file argument is empty. Process is stopped. Please define the broker file.")
        elif args.dt_sec_type is None:
            print("Security type for processing was not given. Process stopped !")
        else:
            DayTrade(broker=str(args.daytrade)).etoro()




