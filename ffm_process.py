import argparse
import time
from FFM_SYSTEM.ffm_data import *
from datetime import date
from datetime import timedelta
from _datetime import datetime

# ----------------- #
#    ARGUMENTS      #
# ----------------- #

parser = argparse.ArgumentParser()

# General data points

parser.add_argument("--rundate", help="Specifies on which date to run production. Switch: specific")
parser.add_argument("--equity_ticker", help="Defining the list of equity tickers or single ticker to "
                                     "produce data. Switches: ALL - All tickers; Specific ticker code",)
# Database related switches

parser.add_argument("--db_user_name", help="User name for database login. Switch: username")
parser.add_argument("--db_password", help="Password for database login. Switch: password")
parser.add_argument("--env", help="Environment switch. Default:prod; Switches: dev ")

# Process related switches

parser.add_argument("--ied_download", help="Intraday equity data download. Switch: Yes")

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
        pass

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

    if args.ied_download == "Yes":

        ffm_process.intraday_equity_price_download()

    ffm_process.close_process()