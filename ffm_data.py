import mysql.connector as sql
import pandas as pd
import requests
import numpy as np
import fix_yahoo_finance as fyf
from pandas.plotting import scatter_matrix
from datetime import date
from matplotlib.finance import candlestick2_ohlc
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


class SQL:

    """
    SQL query class for reading, writing and updating data to FFM databases.
    """

    def __init__(self, data_base, user_name, password):

        self.data_base = data_base
        self.user_name = user_name
        self.password = password
        self.df = None

        self.db_connection = sql.connect(user=self.user_name,
                                         password=self.password,
                                         host='localhost',
                                         database=self.data_base)

        self.cursor = self.db_connection.cursor()

    def select_data(self, select_query):

        """
        Runs select query on database and returns a pandas dataframe
        :param select_query: SQL query
        :return: Pandas dataframe
        """

        self.df = pd.read_sql(select_query, con=self.db_connection)

        return self.df

    def insert_data(self, insert_query):

        """
        Inserts data to the defined database and table
        :param insert_query: Insert query
        """

        self.cursor.execute(insert_query)

        self.db_connection.commit()

    def close_connection(self):

        """
        Closing SQL session
        :return: -
        """

        self.db_connection.close()


class StockData:

    def __init__(self, stock_list, start_date):

        self.returns = None
        self.stocks = stock_list
        self.stock_data = fyf.download(self.stocks, start=start_date)

    def stock_data_frame(self):

        return self.stock_data

    def close_prices(self):

        self.stock_data = self.stock_data["Close"]

        return self.stock_data

    def daily_returns(self):

        self.returns = pd.DataFrame()
        self.stock_data = self.stock_data["Close"]

        for stock in self.stock_data:
            if stock not in self.returns:
                self.returns[stock] = np.log(self.stock_data[stock]).diff()

        return self.returns

    def describe_returns(self):

        self.returns = self.daily_returns()

        return self.returns.describe()

    def correlations(self):

        self.returns = self.daily_returns()
        self.correl = self.returns.corr()

        return self.correl

    def scatter_matrix_plot(self):

        scatter_matrix(self.daily_returns(), figsize=(16, 12), alpha=0.5)
        plt.show()


class OnlineData:

    """
    Downloads data from IEX Exchange to database for a particular equity security. The class creates only the
    appropriate SQL queries.
    """

    def __init__(self, ticker):

        self.ticker = ticker
        self.row = None
        self.url = None
        self.period = None
        self.r = None
        self.data_frame = None
        self.query = None

    def import_intraday_quote_to_database(self, period):

        """
        Inserts intraday raw quote data to database
        :param period: "Intraday" switch refers to T-1 data. Other switch refers to specific date.
        :param ticker: Ticker of the equity
        :return: SQL query which inserts 1 min data points into data frame
        """

        self.period = period

        if self.period == "intraday":

            self.url = 'https://api.iextrading.com/1.0/stock/' + str(self.ticker) + '/batch?types=chart&range=1d&last=1'
            self.r = requests.get(self.url)

        else:

            self.url = 'https://api.iextrading.com/1.0/stock/' + str(self.ticker) + '/chart/date/' + str(self.period)
            self.r = requests.get(self.url)

        self.data_frame = pd.read_json(self.r.text)

        self.query = "insert into intraday_eq_price (ticker,date,minute,high,low,average,volume,notional,number_of_trades,market_high,market_low,market_average,market_volume,market_notional,market_number_of_trades,open,close,market_open,market_close) values "

        for self.row in range(len(np.asarray(self.data_frame["average"]))):

            self.changed_list = [self.ticker,
                                 self.data_frame.loc[self.row, :]['date'],
                                 self.data_frame.loc[self.row, :]['minute'],
                                 round(float(self.data_frame.loc[self.row, :]['high']), 2),
                                 round(float(self.data_frame.loc[self.row, :]['low']), 2),
                                 round(float(self.data_frame.loc[self.row, :]['average']), 2),
                                 self.data_frame.loc[self.row, :]['volume'],
                                 round(float(self.data_frame.loc[self.row, :]['notional']), 2),
                                 self.data_frame.loc[self.row, :]['numberOfTrades'],
                                 round(float(self.data_frame.loc[self.row, :]['marketHigh']), 2),
                                 round(float(self.data_frame.loc[self.row, :]['marketLow']), 2),
                                 round(float(self.data_frame.loc[self.row, :]['marketAverage']), 2),
                                 self.data_frame.loc[self.row, :]['marketVolume'],
                                 round(float(self.data_frame.loc[self.row, :]['marketNotional']), 2),
                                 self.data_frame.loc[self.row, :]['marketNumberOfTrades'],
                                 round(float(self.data_frame.loc[self.row, :]['open']), 2),
                                 round(float(self.data_frame.loc[self.row, :]['close']), 2),
                                 round(float(self.data_frame.loc[self.row, :]['marketOpen']), 2),
                                 round(float(self.data_frame.loc[self.row, :]['marketClose']), 2)]

            for n in range(len(self.changed_list)):

                if str(self.changed_list[n]) == 'nan':
                    self.changed_list[n] = 0

            self.string_list = str(self.changed_list)
            self.query_values = "("+self.string_list[1:-1]+")"+","
            self.query += self.query_values

        self.query0 = str(self.query)

        return self.query[:-1]+";"

    def general_eq_data(self, row):

        """
        Inserts general security data to data base
        :param row: The row where the data will be inserted
        :return: SQL Insert query
        """

        self.row = row
        self.url = "https://api.iextrading.com/1.0/stock/" + str(self.ticker) + "/company"
        self.r = requests.get(self.url)
        self.data_frame = pd.read_json(self.r.text).loc[0]

        self.query = "insert into sec_info (sec_id, name, type, ticker, industry, sector, website ) values ('" + str(
                    self.row + 1) + "','" + str(self.data_frame["companyName"]) + "','EQUITY','" + str(
                    self.data_frame["symbol"]) + "','" + str(self.data_frame["industry"]) + "','" + str(
                    self.data_frame["sector"]) + "','" + str(self.data_frame["website"]) + "')"

        print("id", self.row + 1)
        print("company name", self.data_frame["companyName"])
        print("type", "EQUITY")
        print("ticker", self.data_frame["symbol"])
        print("industry", self.data_frame["industry"])
        print("sector", self.data_frame["sector"])
        print("website", self.data_frame["website"])
        print("")
        
        return self.query

    def last_eq_price(self):

        """
        Downloads the last quote of the particular equity
        :return:
        """

        self.url = """https://api.iextrading.com/1.0/tops/last?symbols={ticker}""".format(ticker=self.ticker)
        self.r = requests.get(self.url)
        self.data_frame = pd.read_json(self.r.text)

        return self.data_frame

    def get_one_year_prices(self):

        """
        Gets one day daily prices for the selected security for 1 year
        :return:
        """

        self.url = """https://api.iextrading.com/1.0/stock/{ticker}/chart/1y""".format(ticker=self.ticker)
        self.r = requests.get(self.url)
        self.data_frame = pd.read_json(self.r.text)

        return self.data_frame

    def get_five_year_prices(self):

        """
        Gets one day daily prices for the selected security for 5 years
        :return:
        """

        self.url = """https://api.iextrading.com/1.0/stock/{ticker}/chart/5y""".format(ticker=self.ticker)
        self.r = requests.get(self.url)
        self.data_frame = pd.read_json(self.r.text)

        return self.data_frame

    def get_one_month_prices(self):

        """
        Gets one day daily prices for the selected security for one month
        :return:
        """

        self.url = """https://api.iextrading.com/1.0/stock/{ticker}/chart/1m""".format(ticker=self.ticker)
        self.r = requests.get(self.url)
        self.data_frame = pd.read_json(self.r.text)

        return self.data_frame


class Entries(SQL):

    """
    Class for data entry for those tables where the entry is defined by a human.
    """

    def __init__(self, data_base, user_name, password):
        super().__init__(data_base, user_name, password)

        self.insert_query = None
        self.id = None
        self.trd_num = None
        self.mod_query = None

    def portfolios(self, portfolio_name, portfolio_type, currency, inception_date, full_name, portfolio_group):

        """
        Portfolio entry

        :param portfolio_name:
        :param portfolio_type:
        :param currency:
        :param inception_date:
        :param full_name:
        :return: -
        """

        self.id = len(self.select_data("""select portfolio_id 
                                          from portfolios""")["portfolio_id"])

        self.insert_query = """insert into portfolios (portfolio_id, portfolio_name, 
                                                          portfolio_type, currency, 
                                                          inception_date, full_name, portfolio_group)
                                                           
                                  values ('{port_id}', '{port_name}', 
                                          '{port_type}', '{crcy}', 
                                          '{inc_date}', '{fl_name}',
                                          '{port_group}')""".format(port_id=int(self.id)+1,
                                                                    port_name=portfolio_name,
                                                                    port_type=portfolio_type,
                                                                    crcy=currency,
                                                                    inc_date=inception_date,
                                                                    fl_name=full_name,
                                                                    port_group=portfolio_group)

        self.insert_data(self.insert_query)
        self.close_connection()

        print("Portfolio was successfully created !")

    def cash_flow(self, port_code, ammount, cft, date, currency, comment, client):

        """
        Cash Flow Entry
        :param port_code:
        :param ammount:
        :param cft:
        :param date:
        :param currency:
        :param comment:
        :param client:
        :return:
        """

        self.id = list(self.select_data("""select cash_id 
                                          from cash_flow""")["cash_id"])

        if len(self.id) < 1:
            self.cf_id = 1
        else:
            self.cf_id = list(self.id)[-1] + 1

        self.insert_query = """insert into cash_flow (cash_id, portfolio_code, 
                                                      ammount, cash_flow_type, 
                                                      date, currency,
                                                      comment, client)

                               values ('{cash_id}', '{port_code}', 
                                       '{ammount}', '{cft}', 
                                       '{date}', '{currency}',
                                       '{comment}', '{client}')""".format(cash_id=self.cf_id,
                                                                          port_code=port_code,
                                                                          ammount=ammount,
                                                                          cft=cft,
                                                                          date=date,
                                                                          currency=currency,
                                                                          comment=comment,
                                                                          client=client)

        self.insert_data(self.insert_query)
        self.close_connection()

        print("Cash flow record was successfully inserted into data base !")

    def sec_info(self, name, type, ticker, industry="-", sector="-", website="-", country="-"):

        """
        Security Entry

        :param name:
        :param type:
        :param ticker:
        :param industry:
        :param sector:
        :param website:
        :return: -
        """

        if (type == "FX") or (type == "CRYPTO") or (type == "LOAN"):

            self.type = type
            self.industry = "-"
            self.sector = "-"
            self.website = "-"
            self.country = "-"

        elif (type == "FUTURES") or (type == "OPTION"):
            self.type = type
            self.industry = "-"
            self.sector = "-"
            self.website = "-"
            self.country = "-"
        elif type == "EQUITY":
            self.type = type
            self.industry = industry
            self.sector = sector
            self.website = website
            self.country = country

        self.id = list(self.select_data("""select sec_id 
                                           from sec_info""")["sec_id"])[-1]

        self.insert_query = """insert into sec_info (sec_id, name, 
                                                     type, ticker, 
                                                     industry, sector, website, country)

                               values ('{sec_id}',  '{name}', 
                                       '{type}',    '{ticker}', 
                                       '{industry}','{sector}',
                                       '{website}', '{country}')""".format(sec_id=int(self.id) + 1,
                                                              name=name,
                                                              type=self.type,
                                                              ticker=ticker,
                                                              industry=self.industry,
                                                              sector=self.sector,
                                                              website=website,
                                                              country=self.country)

        self.insert_data(self.insert_query)
        self.close_connection()

        print("New security was successfully added to the system !")

    def strategy(self, strat_name, strat_desc, start_date, smcode, port_code):

        """
        Strategy Entry

        :param strat_name:
        :param strat_desc:
        :param start_date:
        :param end_date:
        :param smcode:
        :return: -
        """

        self.id = len(self.select_data("""select strategy_code
                                          from strategy""")["strategy_code"])

        self.insert_query = """insert into strategy (strategy_code, strategy_name, 
                                                     strategy_desc, start_date, 
                                                     end_date, strat_modell_code, portfolio_code)

                               values ('{strat_id}',  '{strat_name}', 
                                       '{strat_desc}','{start_date}', 
                                       '{end_date}',  '{smcode}', '{pc}')""".format(strat_id=int(self.id) + 1,
                                                                                    strat_name=strat_name,
                                                                                    strat_desc=strat_desc,
                                                                                    start_date=start_date,
                                                                                    end_date="21000101",
                                                                                    smcode=smcode,
                                                                                    pc=port_code)

        self.insert_data(self.insert_query)
        self.close_connection()

        print("New strategy was successfully added to the system !")

    def strategy_modell(self, modell_name, modell_desc, modell_type):

        self.id = len(self.select_data("""select modell_code
                                          from strategy_modell""")["modell_code"])

        self.insert_query = """insert into strategy_modell (modell_code, modell_name, 
                                                            modell_desc, modell_type)

                                       values ('{md_code}','{md_name}', 
                                               '{md_desc}','{md_type}')""".format(md_code=int(self.id) + 1,
                                                                                  md_name=modell_name,
                                                                                  md_desc=modell_desc,
                                                                                  md_type=modell_type)

        self.insert_data(self.insert_query)
        self.close_connection()

        print("New strategy model was successfully added to the system !")

    def trade(self, date, portfolio_code, strategy_code,
              side, quantity, trade_price, leverage,
              sl, sl_level, sec_id,
              leverage_perc, ticker, margin_bal, collateral, action, status):

        """
        Only for trade booking into trade table. Adding to previous open position is treated as a new trade with
        new trade_num.
        :return:
        """

        self.id = list(self.select_data("""select trade_id
                                          from trade""")["trade_id"])

        if len(self.id) < 1:
            self.trd_id = 1
        else:
            self.trd_id = list(self.id)[-1] + 1

        try:
            self.trd_num = list(self.select_data("""select trade_num
                                                    from trade""")["trade_num"])[-1]
        except:

            self.trd_num = 0

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
                                       '{action}', '{ticker}','{mb}','{coll}')""".format(trade_id=self.trd_id,
                                                                                         date=date,
                                                                                         trade_num=int(self.trd_num) + 1,
                                                                                         portfolio_code=portfolio_code,
                                                                                         strategy_code=strategy_code,
                                                                                         side=side,
                                                                                         quantity=quantity,
                                                                                         trade_price=trade_price,
                                                                                         leverage=leverage,
                                                                                         status=status,
                                                                                         sl=sl,
                                                                                         sl_level=sl_level,
                                                                                         sec_id=sec_id,
                                                                                         leverage_perc=leverage_perc,
                                                                                         action=action,
                                                                                         ticker=ticker,
                                                                                         mb=margin_bal,
                                                                                         coll=collateral)

        self.insert_data(self.insert_query)
        self.close_connection()

        print("New trade was successfully entered into the system !")

    def trade_modify(self, trade_id, last_price, date="0", action="0", quantity="0", trade_price="0"):

        """
        Modify an open trade in trade table. Closing out part of existing trade position.

        action=close-out option modifies existing trade. Default value is to close a trade.
        :return:
        """

        if action == "close-out":

            self.id = len(self.select_data("""select trade_id
                                              from trade""")["trade_id"])

            self.mod_query = self.select_data("""select*from trade 
                                                where trade_id = {trd_id}""".format(trd_id=trade_id))

            if self.mod_query["action"].values == "CLOSED":
                print("Trade is closed! Can't be modified!")
                pass
            else:
                if self.mod_query["side"].values == "BUY":
                    self.side = "SELL"
                else:
                    self.side = "BUY"

                self.insert_query = """insert into trade (trade_id, date, trade_num, portfolio_code, 
                                                                  strategy_code, side, quantity, trade_price, 
                                                                  leverage, status, sl, sl_level,
                                                                  sec_id, leverage_perc, action)
        
                                               values ('{trade_id}',  '{date}', 
                                                       '{trade_num}','{portfolio_code}', 
                                                       '{strategy_code}',  '{side}',
                                                       '{quantity}', '{trade_price}',
                                                       '{leverage}', '{status}',
                                                       '{sl}', '{sl_level}',
                                                       '{sec_id}', '{leverage_perc}',
                                                       '{action}')""".format(trade_id=int(self.id) + 1,
                                                                             date=date,
                                                                             trade_num=int(self.mod_query["trade_num"]),
                                                                             portfolio_code=self.mod_query["portfolio_code"][0],
                                                                             strategy_code=self.mod_query["strategy_code"][0],
                                                                             side=self.side,
                                                                             quantity=quantity,
                                                                             trade_price=trade_price,
                                                                             leverage=self.mod_query["leverage"][0],
                                                                             status="CLOSE",
                                                                             sl="No",
                                                                             sl_level=self.mod_query["sl_level"][0],
                                                                             sec_id=self.mod_query["sec_id"][0],
                                                                             leverage_perc=self.mod_query["leverage_perc"][0],
                                                                             action="CLOSED")

                self.insert_data(self.insert_query)
                self.close_connection()

                print("Trade was modified successfully !")

        else:

            self.insert_data("""update trade set status = 'CLOSE', action = 'CLOSED', close_price = {cl_price}
                                where trade_id = {trd_id}""".format(cl_price=last_price,
                                                                    trd_id=trade_id))

            self.close_connection()

            print("Trd id: "+str(trade_id)+" is closed !")

    def port_group(self, parent, sleve, sleve_type):

        """
        Portfolio group entry
        :param parent:
        :param sleve:
        :param sleve_type:
        :return:
        """

        self.id = len(self.select_data("""select connection_id
                                                  from portfolio_group""")["connection_id"])

        self.insert_query = """insert into portfolio_group (connection_id, parent, sleve, sleve_type) 
                               values ('{id}','{parent}', '{sleve}', '{sleve_type}')""".format(id=int(self.id)+1,
                                                                                               parent=parent,
                                                                                               sleve=sleve,
                                                                                               sleve_type=sleve_type)

        self.insert_data(self.insert_query)
        self.close_connection()

        print("Portfolio connection was created successfully!")

    def positions(self, date, portfolio_code, strategy_code, open_bal, close_bal, sec_id):

        """
        Positions entry
        :param date:
        :param portfolio_code:
        :param strategy_code:
        :param quantity:
        :param trade_price:
        :param sec_id:
        :return:
        """

        self.id = list(self.select_data("""select pos_id from positions""")["pos_id"])

        if len(self.id) < 1:
            self.pos_id = 1
        else:
            self.pos_id = list(self.id)[-1] + 1

        self.insert_query = """insert into positions (pos_id, date, portfolio_code, strategy_code, 
                                                      open_bal, close_bal, sec_id) 
                                       values ('{pos_id}','{date}', '{portfolio_code}', '{strategy_code}', 
                                       '{open_bal}', '{close_bal}', '{sec_id}')""".format(pos_id=self.pos_id,
                                                                                          date=date,
                                                                                          portfolio_code=portfolio_code,
                                                                                          strategy_code=strategy_code,
                                                                                          open_bal=open_bal,
                                                                                          close_bal=close_bal,
                                                                                          sec_id=sec_id)

        self.insert_data(self.insert_query)
        self.close_connection()


if __name__ == "__main__":

    x = OnlineData(ticker="AAPL").last_eq_price()
    print(x)

