import argparse
import time
from FFM_SYSTEM.ffm_data import *
from datetime import date
from datetime import timedelta
from _datetime import datetime
from pandas.tseries.offsets import BDay

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
parser.add_argument("--nav_calc", help="Calculates portfolios NAV. Switch: Yes")
parser.add_argument("--live_nav", help="Calculates portfolios NAV with latest prices. Switch: Yes")
parser.add_argument("--hold_calc", help="Calculates portfolios holding data. Switch: Yes")

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

                #print(self.t_min_one_pos)
                self.trades = self.sql_connection.select_data(select_query="""select*from trade 
                                                                              where date = '{date}' 
                                                                              and portfolio_code = '{port_id}'""".format(
                                                                                                      port_id=port_id,
                                                                                                      date=self.query_date))
                print(self.trades)
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

                        if self.pos["name"] == "Margin":
                            pass
                        else:
                            self.new_bal = self.close_bal

                            print("Security:", self.pos["name"])
                            print("New trade total quantity:", self.close_bal)
                            print("T-2 balance:", self.pos["close_bal"])
                            print("Close balance:", self.new_bal+self.pos["close_bal"])
                            print("Writing data to data base")

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

                    for trade in range(len(self.trades["trade_id"])):

                        self.tr = self.trades.iloc[trade]
                        self.ps = self.t_min_one_pos[self.t_min_one_pos["sec_id"] == self.tr["sec_id"]]

                        if len(list(self.ps["pos_id"])) >= 1:
                            pass
                        else:
                            print("Security:", self.tr["ticker"])
                            print("T-2 balance: 0")
                            print("Close balance:", self.tr["quantity"])
                            print("Margin:", self.tr["margin_bal"])
                            print("Writing data to data base")

                            Entries(data_base=self.data_base,
                                    user_name=args.db_user_name,
                                    password=args.db_password).positions(date=self.query_date,
                                                                         portfolio_code=self.tr["portfolio_code"],
                                                                         strategy_code=self.tr["strategy_code"],
                                                                         open_bal=0,
                                                                         close_bal=self.tr["quantity"],
                                                                         sec_id=self.tr["sec_id"])

                            print("")

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

                        if (ticker == "MRGN") or (ticker == "CLTR"):
                            self.aum_price = 0
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

            print("")
            print("----------------------------------")
            print("  Starting Holding calculations   ")
            print("----------------------------------")
            print("")

            for port_id in list(self.portfolios["portfolio_id"]):

                print("Calculating Portfolio Holdings. Portfolio code:", port_id)

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

                        self.pos_lenght = self.sql_connection.select_data(select_query="""select count(*) 
                                                                                          from portfolio_holdings""")
                        self.pos_lenght = self.pos_lenght["count(*)"][0]
                        print("Data base position id starts from ", self.pos_lenght)
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

                        self.pos_lenght = self.sql_connection.select_data(select_query="""select count(*) 
                                                                                          from portfolio_holdings""")
                        self.pos_lenght = self.pos_lenght["count(*)"][0]

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

    if args.nav_calc == "Yes":

        ffm_process.nav_calc()

    if args.hold_calc == "Yes":

        ffm_process.portfolio_holding_calc()


