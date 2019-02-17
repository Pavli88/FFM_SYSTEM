from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import sys
from FFM_SYSTEM.ffm_data import *
from datetime import date


class EntryWindows:

    def __init__(self, dialog, table_entry, data_base, user_name, password):

        self.table_entry = table_entry
        self.Dialog = dialog
        self.Dialog.setObjectName("Dialog")
        self.sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.sizePolicy.setHorizontalStretch(0)
        self.sizePolicy.setVerticalStretch(0)
        self.sizePolicy.setHeightForWidth(self.Dialog.sizePolicy().hasHeightForWidth())
        self.Dialog.setSizePolicy(self.sizePolicy)

        self.msg = None
        self.db = data_base
        self.password = password
        self.user_name = user_name
        self.entry_connection = Entries(data_base=self.db,
                                        user_name=self.user_name,
                                        password=self.password)

        self.cbox_1 = ""
        self.cbox_2 = ""
        self.text_input_1 = ""
        self.text_input_2 = ""
        self.label_1 = ""
        self.label_2 = ""
        self.label_3 = ""
        self.label_4 = ""
        self.label_5 = ""

        self.create_button = QtWidgets.QPushButton(self.Dialog)

        if self.table_entry == "portfolios":
            self.create_button.setGeometry(QtCore.QRect(280, 90, 121, 51))
            self.create_button.setObjectName("pushButton")
        elif self.table_entry == "strategy_modell":
            self.create_button.setGeometry(QtCore.QRect(340, 70, 71, 21))
            self.create_button.setObjectName("create_button")
        elif self.table_entry == "strategy":
            self.create_button.setGeometry(QtCore.QRect(310, 130, 101, 21))
            self.create_button.setObjectName("create_button")
        elif self.table_entry == "cash flow":
            self.create_button.setGeometry(QtCore.QRect(310, 110, 101, 31))
            self.create_button.setObjectName("create_button")
        elif self.table_entry == "security":
            self.create_button.setGeometry(QtCore.QRect(480, 20, 101, 21))
            self.create_button.setObjectName("create_button")

    def portfolio_entry(self):

        self.Dialog.resize(427, 170)
        self.Dialog.setFixedSize(self.Dialog.size())
        self.Dialog.setWindowTitle("Portfolio Entry - " + str(self.db))

        self.port_name_line = QtWidgets.QLineEdit(self.Dialog)
        self.port_name_line.setGeometry(QtCore.QRect(140, 10, 271, 21))
        self.port_name_line.setObjectName("port_name_line")

        self.port_name = QtWidgets.QLabel(self.Dialog)
        self.port_name.setGeometry(QtCore.QRect(20, 10, 111, 21))
        self.port_name.setObjectName("port_name")

        self.port_type = QtWidgets.QLabel(self.Dialog)
        self.port_type.setGeometry(QtCore.QRect(20, 70, 111, 21))
        self.port_type.setObjectName("port_type")

        self.port_type_cbox = QtWidgets.QComboBox(self.Dialog)
        self.port_type_cbox.setGeometry(QtCore.QRect(140, 70, 121, 21))
        self.port_type_cbox.setObjectName("port_type_cbox")
        self.port_type_cbox.addItems(["TEST", "TRADE", "INVESTMENT", "SAVING", "BUSINESS"])

        self.currency = QtWidgets.QLabel(self.Dialog)
        self.currency.setGeometry(QtCore.QRect(20, 100, 111, 21))
        self.currency.setObjectName("currency")

        self.currency_line = QtWidgets.QLineEdit(self.Dialog)
        self.currency_line.setGeometry(QtCore.QRect(140, 100, 121, 21))
        self.currency_line.setObjectName("currency_line")

        self.full_name = QtWidgets.QLabel(self.Dialog)
        self.full_name.setGeometry(QtCore.QRect(20, 40, 111, 21))
        self.full_name.setObjectName("full_name")

        self.full_name_line = QtWidgets.QLineEdit(self.Dialog)
        self.full_name_line.setGeometry(QtCore.QRect(140, 40, 271, 21))
        self.full_name_line.setObjectName("full_name_line")

        self.dateEdit = QtWidgets.QDateEdit(self.Dialog)
        self.dateEdit.setGeometry(QtCore.QRect(140, 130, 121, 26))
        self.dateEdit.setDate(QtCore.QDate(date.today().year, date.today().month, date.today().day))
        self.dateEdit.setObjectName("dateEdit")

        self.inc_date = QtWidgets.QLabel(self.Dialog)
        self.inc_date.setGeometry(QtCore.QRect(20, 130, 111, 21))
        self.inc_date.setObjectName("inc_date")

        self.port_name.setText("Portfolio Name")
        self.port_type.setText("Portfolio Type")
        self.currency.setText("Currency")
        self.full_name.setText("Full Name")
        self.inc_date.setText("Inception Date")
        self.create_button.setText("Create")

    def strat_modell_entry(self):

        self.Dialog.resize(425, 105)
        self.Dialog.setFixedSize(self.Dialog.size())
        self.Dialog.setWindowTitle("Strategy Model Entry - " + str(self.db))

        self.model_name_line = QtWidgets.QLineEdit(self.Dialog)
        self.model_name_line.setGeometry(QtCore.QRect(170, 10, 241, 21))
        self.model_name_line.setObjectName("model_name_line")

        self.model_name = QtWidgets.QLabel(self.Dialog)
        self.model_name.setGeometry(QtCore.QRect(20, 10, 111, 21))
        self.model_name.setObjectName("model_name")

        self.model_desc = QtWidgets.QLabel(self.Dialog)
        self.model_desc.setGeometry(QtCore.QRect(20, 40, 141, 21))
        self.model_desc.setObjectName("model_desc")

        self.model_desc_line = QtWidgets.QLineEdit(self.Dialog)
        self.model_desc_line.setGeometry(QtCore.QRect(170, 40, 241, 21))
        self.model_desc_line.setObjectName("model_desc_line")

        self.port_type_2 = QtWidgets.QLabel(self.Dialog)
        self.port_type_2.setGeometry(QtCore.QRect(20, 70, 111, 21))
        self.port_type_2.setObjectName("port_type_2")

        self.model_type_cbox = QtWidgets.QComboBox(self.Dialog)
        self.model_type_cbox.setGeometry(QtCore.QRect(170, 70, 151, 21))
        self.model_type_cbox.setObjectName("db_cbox_2")
        self.model_type_cbox.addItems(["INTRADAY", "TRADE", "INVESTMENT"])

        self.model_name.setText("Model Name")
        self.model_desc.setText("Model Descreption")
        self.create_button.setText("Create")
        self.port_type_2.setText("Model Type")

    def strategy_entry(self):

        self.Dialog.resize(427, 168)
        self.Dialog.setWindowTitle("Strategy Entry - " + str(self.db))
        self.Dialog.setFixedSize(self.Dialog.size())

        self.text_input_1 = QtWidgets.QLineEdit(self.Dialog)
        self.text_input_1.setGeometry(QtCore.QRect(180, 10, 231, 21))
        self.text_input_1.setObjectName("text_input_1")

        self.label_1 = QtWidgets.QLabel(self.Dialog)
        self.label_1.setGeometry(QtCore.QRect(20, 10, 111, 21))
        self.label_1.setObjectName("label_1")

        self.label_2 = QtWidgets.QLabel(self.Dialog)
        self.label_2.setGeometry(QtCore.QRect(20, 40, 151, 21))
        self.label_2.setObjectName("label_2")

        self.text_input_2 = QtWidgets.QLineEdit(self.Dialog)
        self.text_input_2.setGeometry(QtCore.QRect(180, 40, 231, 21))
        self.text_input_2.setObjectName("text_input_2")

        self.create_button = QtWidgets.QPushButton(self.Dialog)
        self.create_button.setGeometry(QtCore.QRect(310, 130, 101, 21))
        self.create_button.setObjectName("create_button")

        self.label_3 = QtWidgets.QLabel(self.Dialog)
        self.label_3.setGeometry(QtCore.QRect(20, 70, 151, 21))
        self.label_3.setObjectName("label_3")

        self.cbox_1 = QtWidgets.QComboBox(self.Dialog)
        self.cbox_1.setGeometry(QtCore.QRect(180, 70, 231, 21))
        self.cbox_1.setObjectName("cbox_1")
        self.cbox_1.addItems(list(self.entry_connection.select_data("select*from strategy_modell")["modell_name"]))

        self.label_4 = QtWidgets.QLabel(self.Dialog)
        self.label_4.setGeometry(QtCore.QRect(20, 100, 151, 21))
        self.label_4.setObjectName("label_4")

        self.cbox_2 = QtWidgets.QComboBox(self.Dialog)
        self.cbox_2.setGeometry(QtCore.QRect(180, 100, 231, 21))
        self.cbox_2.setObjectName("cbox_2")
        self.cbox_2.addItems(list(self.entry_connection.select_data("select*from portfolios")["portfolio_name"]))

        self.label_5 = QtWidgets.QLabel(self.Dialog)
        self.label_5.setGeometry(QtCore.QRect(20, 130, 151, 21))
        self.label_5.setObjectName("label_5")

        self.dateEdit = QtWidgets.QDateEdit(self.Dialog)
        self.dateEdit.setGeometry(QtCore.QRect(180, 130, 117, 26))
        self.dateEdit.setDate(QtCore.QDate(date.today().year, date.today().month, date.today().day))
        self.dateEdit.setObjectName("dateEdit")

        self.label_1.setText("Strategy Name")
        self.label_2.setText("Strategy Descreption")
        self.create_button.setText("Create")
        self.label_3.setText("Strategy Model")
        self.label_4.setText("Portfolio Code")
        self.label_5.setText("Start Date")

    def cash_flow(self):

        self.Dialog.resize(422, 161)
        self.Dialog.setWindowTitle("Cash Flow Entry - " + str(self.db))
        self.Dialog.setFixedSize(self.Dialog.size())

        self.label_3 = QtWidgets.QLabel(self.Dialog)
        self.label_3.setGeometry(QtCore.QRect(20, 70, 111, 21))
        self.label_3.setObjectName("label_3")
        self.label_5 = QtWidgets.QLabel(self.Dialog)

        self.label_5.setGeometry(QtCore.QRect(180, 130, 121, 20))
        self.label_5.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")

        self.text_input_1 = QtWidgets.QLineEdit(self.Dialog)
        self.text_input_1.setGeometry(QtCore.QRect(180, 70, 231, 21))
        self.text_input_1.setObjectName("text_input_1")

        self.label_1 = QtWidgets.QLabel(self.Dialog)
        self.label_1.setGeometry(QtCore.QRect(20, 10, 151, 21))
        self.label_1.setObjectName("label_1")

        self.cbox_1 = QtWidgets.QComboBox(self.Dialog)
        self.cbox_1.setGeometry(QtCore.QRect(180, 10, 231, 21))
        self.cbox_1.setObjectName("cbox_1")
        self.cbox_1.addItems(list(self.entry_connection.select_data("select*from portfolios")["portfolio_name"]))
        self.cbox_1.currentIndexChanged.connect(self.show_portfolio_currency)

        self.label_2 = QtWidgets.QLabel(self.Dialog)
        self.label_2.setGeometry(QtCore.QRect(20, 40, 151, 21))
        self.label_2.setObjectName("label_2")

        self.cbox_2 = QtWidgets.QComboBox(self.Dialog)
        self.cbox_2.setGeometry(QtCore.QRect(180, 40, 231, 21))
        self.cbox_2.setObjectName("cbox_2")
        self.cbox_2.addItems(["INFLOW", "OUTFLOW"])

        self.label_4 = QtWidgets.QLabel(self.Dialog)
        self.label_4.setGeometry(QtCore.QRect(20, 100, 121, 21))
        self.label_4.setObjectName("label_4")

        self.label_6 = QtWidgets.QLabel(self.Dialog)
        self.label_6.setGeometry(QtCore.QRect(20, 130, 121, 21))
        self.label_6.setObjectName("label_6")

        self.dateEdit = QtWidgets.QDateEdit(self.Dialog)
        self.dateEdit.setGeometry(QtCore.QRect(180, 100, 117, 26))
        self.dateEdit.setDate(QtCore.QDate(date.today().year, date.today().month, date.today().day))
        self.dateEdit.setObjectName("dateEdit")

        self.label_3.setText("Ammount")
        self.create_button.setText("Create")
        self.label_1.setText("Portfolio")
        self.label_2.setText("Cash Flow Type")
        self.label_6.setText("Currency")
        self.label_4.setText("Date")

    def security(self):

        self.Dialog.resize(590, 65)
        self.Dialog.setWindowTitle("Security Entry - " + str(self.db))
        #self.Dialog.setFixedSize(self.Dialog.size())

        self.label_4 = QtWidgets.QLabel(self.Dialog)
        self.label_5 = QtWidgets.QLabel(self.Dialog)
        self.label_7 = QtWidgets.QLabel(self.Dialog)
        self.label_6 = QtWidgets.QLabel(self.Dialog)
        self.cbox_2 = QtWidgets.QComboBox(self.Dialog)
        self.cbox_3 = QtWidgets.QComboBox(self.Dialog)
        self.cbox_4 = QtWidgets.QComboBox(self.Dialog)
        self.text_input_3 = QtWidgets.QLineEdit(self.Dialog)

        self.text_input_1 = QtWidgets.QLineEdit(self.Dialog)
        self.text_input_1.setGeometry(QtCore.QRect(140, 10, 331, 21))
        self.text_input_1.setObjectName("text_input_1")

        self.label_1 = QtWidgets.QLabel(self.Dialog)
        self.label_1.setGeometry(QtCore.QRect(20, 10, 111, 21))
        self.label_1.setObjectName("label_1")

        self.label_2 = QtWidgets.QLabel(self.Dialog)
        self.label_2.setGeometry(QtCore.QRect(250, 40, 101, 21))
        self.label_2.setObjectName("label_2")

        self.text_input_2 = QtWidgets.QLineEdit(self.Dialog)
        self.text_input_2.setGeometry(QtCore.QRect(140, 40, 101, 21))
        self.text_input_2.setObjectName("text_input_2")

        self.label_3 = QtWidgets.QLabel(self.Dialog)
        self.label_3.setGeometry(QtCore.QRect(20, 40, 151, 21))
        self.label_3.setObjectName("label_3")

        self.cbox_1 = QtWidgets.QComboBox(self.Dialog)
        self.cbox_1.setGeometry(QtCore.QRect(350, 40, 121, 21))
        self.cbox_1.setObjectName("cbox_1")
        self.cbox_1.addItems(["BOND", "CRYPTO", "EQUITY", "FX", "FUTURES", "OPTION"])
        self.cbox_1.currentIndexChanged.connect(self.security_options)

        self.label_1.setText("Security Name")
        self.label_2.setText("Security Type")
        self.create_button.setText("Create")
        self.label_3.setText("Ticker")

    def security_options(self):

        if self.cbox_1.currentText() == "EQUITY":

            self.Dialog.resize(590, 159)

            self.label_4.setGeometry(QtCore.QRect(20, 70, 121, 21))
            self.label_4.setObjectName("label_4")
            self.label_4.setText("Industry")

            self.label_5.setGeometry(QtCore.QRect(20, 100, 121, 21))
            self.label_5.setObjectName("label_5")
            self.label_5.setText("Sector")

            self.label_7.setGeometry(QtCore.QRect(20, 130, 121, 21))
            self.label_7.setObjectName("label_7")
            self.label_7.setText("Country")

            self.label_6.setGeometry(QtCore.QRect(250, 130, 61, 21))
            self.label_6.setObjectName("label_6")
            self.label_6.setText("Website")

            self.cbox_2.setGeometry(QtCore.QRect(140, 70, 331, 21))
            self.cbox_2.setObjectName("cbox_2")
            self.cbox_2.addItems(['Aerospace & Defense', 'Airlines','Application Software',
                                  'Asset Management', 'Autos', 'Banks', 'Beverages - Alcoholic',
                                  'Beverages - Non-Alcoholic', 'Biotechnology', 'Brokers & Exchanges',
                                  'Building Materials', 'Business Services', 'Chemicals', 'Communication Equipment',
                                  'Communication Services', 'Computer Hardware', 'Consumer Packaged Goods',
                                  'Credit Services', 'Drug Manufacturers', 'Engineering & Construction',
                                  'Entertainment', 'Farm & Construction Machinery', 'Forest Products',
                                  'Health Care Plans', 'Homebuilding & Construction', 'Industrial Products',
                                  'Insurance', 'Insurance - Life', 'Insurance - Property & Casualty',
                                  'Manufacturing - Apparel & Furniture', 'Medical Devices',
                                  'Medical Diagnostics & Research', 'Medical Distribution',
                                  'Medical Instruments & Equipment', 'Metals & Mining', 'Oil & Gas - E&P',
                                  'Oil & Gas - Integrated', 'Oil & Gas - Midstream', 'Oil & Gas - Refining & Marketing',
                                  'Oil & Gas - Services', 'Online Media', 'Packaging & Containers',
                                  'REITs', 'Restaurants', 'Retail - Apparel & Specialty', 'Retail - Defensive',
                                  'Semiconductors', 'Tobacco Products', 'Transportation & Logistics',
                                  'Travel & Leisure', 'Utilities - Regulated', 'Waste Management'])

            self.cbox_3.setGeometry(QtCore.QRect(140, 100, 331, 21))
            self.cbox_3.setObjectName("cbox_3")
            self.cbox_3.addItems(['Basic Materials', 'Communication Services', 'Consumer Cyclical',
                                  'Consumer Defensive', 'Energy', 'Financial Services', 'Healthcare',
                                  'Industrials', 'Real Estate', 'Technology', 'Utilities'])

            self.cbox_4.setGeometry(QtCore.QRect(140, 130, 101, 21))
            self.cbox_4.setObjectName("cbox_4")
            self.cbox_4.addItems(["CA", "DE", "HU", "JP", "US", "UK"])

            self.text_input_3.setGeometry(QtCore.QRect(320, 130, 151, 21))
            self.text_input_3.setObjectName("text_input_3")

        elif self.cbox_1.currentText() == "FX":
            self.Dialog.resize(590, 69)

        elif self.cbox_1.currentText() == "CRYPTO":
            self.Dialog.resize(590, 69)

        elif self.cbox_1.currentText() == "FUTURES":
            self.Dialog.resize(590, 69)


    def show_portfolio_currency(self):

        self.label_5.setText(list(self.entry_connection.select_data("""select*from portfolios 
                                                                       where portfolio_name = '{port_name}'""".format(
                                                                  port_name=self.cbox_1.currentText()))["currency"])[0])

    def create(self):

        if self.table_entry == "portfolios":

            if len(self.port_name_line.text()) < 1:

                self.msg_box(message="Portfolio name is too short !", title="Notification", )

            elif len(self.full_name_line.text()) < 1:

                self.msg_box(message="Portfolio full name is too short !", title="Notification", )

            else:

                self.entry_connection.portfolios(portfolio_name=self.port_name_line.text(),
                                                 portfolio_type=self.port_type_cbox.currentText(),
                                                 currency=self.currency_line.text(),
                                                 full_name=self.full_name_line.text(),
                                                 inception_date=self.dateEdit.text().replace(". ", "").replace(".", ""))

                self.msg_box(message="""{port} was entered successfully into {db}""".format(port=self.port_name_line.text(),
                                                                                            db=self.db),
                             title="Notification")

            self.Dialog.close()

        elif self.table_entry == "strategy_modell":

            if len(self.model_desc_line.text()) > 44:

                self.msg_box(message="Strategy Model Descreption is too long !", title="Notification", )

            elif len(self.model_desc_line.text()) < 2:

                self.msg_box(message="Strategy Model Descreption is too short !", title="Notification", )

            elif len(self.model_name_line.text()) < 2:

                self.msg_box(message="Strategy Model Name is too short !", title="Notification", )

            else:

                self.entry_connection.strategy_modell(modell_name=self.model_name_line.text(),
                                                      modell_type=self.model_type_cbox.currentText(),
                                                      modell_desc=self.model_desc_line.text())

                self.msg_box(message="""New strategy model was entered successfully into {db}""".format(db=self.db),
                             title="Strategy Model Entry Confirmation", )

            self.Dialog.close()

        elif self.table_entry == "strategy":

            if len(self.text_input_1.text()) < 2:

                self.msg_box(message="Strategy Name is too short !", title="Notification", )

            elif len(self.text_input_2.text()) < 2:

                self.msg_box(message="Strategy Descreption is too short !", title="Notification", )

            else:

                self.entry_connection.strategy(strat_name=self.text_input_1.text(),
                                               strat_desc=self.text_input_2.text(),
                                               start_date=self.dateEdit.text().replace(". ", "").replace(".", ""),
                                               smcode=list(self.entry_connection.select_data("""
                                               select * from strategy_modell 
                                               where modell_name = '{model_name}'""".format(
                                                   model_name=self.cbox_1.currentText()))["modell_code"].values)[0],
                                               port_code=list(self.entry_connection.select_data("""
                                               select * from portfolios 
                                               where portfolio_name = '{port_name}'""".format(
                                                   port_name=self.cbox_2.currentText()))["portfolio_id"].values)[0])

                self.Dialog.close()

        elif self.table_entry == "cash flow":

            if len(self.text_input_1.text()) < 2:

                self.msg_box(message="Cash Flow field is empty !", title="Notification", )

            else:

                self.entry_connection.cash_flow(port_code=list(
                                                self.entry_connection.select_data("""select*from portfolios 
                                                                  where portfolio_name = '{port_name}'""".format(
                                                            port_name=self.cbox_1.currentText()))["portfolio_id"])[0],
                                                ammount=self.text_input_1.text(),
                                                cft=self.cbox_2.currentText(),
                                                date=self.dateEdit.text().replace(". ", "").replace(".", ""))

                self.Dialog.close()

        elif self.table_entry == "security":

            if len(self.text_input_1.text()) < 2:

                self.msg_box(message="Security Name field is empty !", title="Notification", )

            else:

                if (self.cbox_1.currentText() == "FX") or (self.cbox_1.currentText() == "CRYPTO"):

                    self.entry_connection.sec_info(name=self.text_input_1.text(),
                                                   type=self.cbox_1.currentText(),
                                                   ticker=self.text_input_2.text())
                elif self.cbox_1.currentText() == "EQUITY":

                    self.entry_connection.sec_info(name=self.text_input_1.text(),
                                                   type=self.cbox_1.currentText(),
                                                   ticker=self.text_input_2.text(),
                                                   industry=self.cbox_2.currentText(),
                                                   sector=self.cbox_3.currentText(),
                                                   website=self.text_input_3.text(),
                                                   country=self.cbox_4.currentText())

                self.Dialog.close()

    def db_radio_button(self, button, table=None, cbox=None, col_name=None):

        if button == "dev":
            self.db = "dev_ffm_sys"
        else:
            self.db = "ffm_sys"

        if table is None:
            pass
        else:
            try:
                self.db_query = SQL(data_base=self.db,
                                    user_name=self.user_name_line.text(),
                                    password=self.password_line.text()).select_data("""select*from 
                                                                                       {table}""".format(table=table))

                cbox.addItems(list(self.db_query[col_name]))

            except:

                self.msg_box(message="Password or User Name is missing !", title="Notification", )

    def msg_box(self, message, title):

        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Information)
        self.msg.setText(message)
        self.msg.setWindowTitle(title)
        self.msg.setStandardButtons(QMessageBox.Ok)
        self.msg.exec_()


class TradeEntry(object):

    def __init__(self, Dialog, data_base, user_name, password, portfolio_name):

        self.data_base = data_base
        self.user_name = user_name
        self.password = password

        self.db_connection = SQL(data_base=self.data_base, user_name=self.user_name, password=self.password)
        self.strategy_query = self.db_connection.select_data(select_query="""select*from strategy 
        where portfolio_code in (select portfolio_id from portfolios 
                                 where portfolio_name = '{portfolio_name}')""".format(portfolio_name=portfolio_name))
        self.db_connection.close_connection()

        Dialog.setObjectName("Dialog")
        Dialog.resize(1061, 511)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setWindowTitle("Trade Entry - " + portfolio_name)

        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(20, 10, 591, 211))
        self.groupBox.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBox.setObjectName("groupBox")

        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_4.setObjectName("gridLayout_4")

        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")

        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")

        self.label_1 = QtWidgets.QLabel(self.groupBox)
        self.label_1.setObjectName("label_1")
        self.gridLayout.addWidget(self.label_1, 0, 0, 1, 1)

        self.cbox_1 = QtWidgets.QComboBox(self.groupBox)
        self.cbox_1.setObjectName("cbox_1")
        self.cbox_1.addItems(["BOND", "CRYPTO", "EQUITY", "FUTURES", "FX", "OPTION"])
        self.gridLayout.addWidget(self.cbox_1, 0, 1, 1, 1)

        self.listWidget = QtWidgets.QListWidget(self.groupBox)
        self.listWidget.setObjectName("listWidget")

        self.gridLayout.addWidget(self.listWidget, 1, 0, 1, 2)
        self.gridLayout_3.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)

        self.cbox_3 = QtWidgets.QComboBox(self.groupBox)
        self.cbox_3.setObjectName("cbox_3")
        self.cbox_3.addItems(list(self.strategy_query["strategy_name"]))


        self.gridLayout_2.addWidget(self.cbox_3, 0, 1, 1, 2)
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 1, 0, 1, 1)
        self.text_input_2 = QtWidgets.QLineEdit(self.groupBox)
        self.text_input_2.setObjectName("text_input_2")
        self.gridLayout_2.addWidget(self.text_input_2, 1, 1, 1, 2)
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 2, 0, 1, 3)
        self.label_10 = QtWidgets.QLabel(self.groupBox)
        self.label_10.setObjectName("label_10")
        self.gridLayout_2.addWidget(self.label_10, 3, 0, 1, 1)
        self.text_input_3 = QtWidgets.QLineEdit(self.groupBox)
        self.text_input_3.setObjectName("text_input_3")
        self.gridLayout_2.addWidget(self.text_input_3, 3, 1, 1, 2)
        self.label_7 = QtWidgets.QLabel(self.groupBox)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 4, 0, 1, 1)
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.doubleSpinBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.doubleSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.doubleSpinBox.setMaximum(100.0)
        self.doubleSpinBox.setSingleStep(5.0)
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.gridLayout_2.addWidget(self.doubleSpinBox, 4, 1, 1, 1)
        self.create_button = QtWidgets.QPushButton(self.groupBox)
        self.create_button.setObjectName("create_button")
        self.gridLayout_2.addWidget(self.create_button, 4, 2, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.groupBox)
        self.label_8.setObjectName("label_8")
        self.gridLayout_2.addWidget(self.label_8, 5, 0, 1, 1)

        self.dateEdit = QtWidgets.QDateEdit(self.groupBox)
        self.dateEdit.setObjectName("dateEdit")
        self.dateEdit.setDate(QtCore.QDate(date.today().year, date.today().month, date.today().day))

        self.gridLayout_2.addWidget(self.dateEdit, 5, 1, 1, 1)
        self.create_button_2 = QtWidgets.QPushButton(self.groupBox)
        self.create_button_2.setObjectName("create_button_2")
        self.gridLayout_2.addWidget(self.create_button_2, 5, 2, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 1, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_3, 0, 0, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_2.setGeometry(QtCore.QRect(20, 230, 1021, 261))
        self.groupBox_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBox_2.setFlat(False)
        self.groupBox_2.setObjectName("groupBox_2")
        self.widget = QtWidgets.QWidget(self.groupBox_2)
        self.widget.setGeometry(QtCore.QRect(10, 32, 1001, 221))
        self.widget.setObjectName("widget")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.create_button_3 = QtWidgets.QPushButton(self.widget)
        self.create_button_3.setObjectName("create_button_3")
        self.gridLayout_5.addWidget(self.create_button_3, 0, 0, 1, 1)
        self.create_button_4 = QtWidgets.QPushButton(self.widget)
        self.create_button_4.setObjectName("create_button_4")
        self.gridLayout_5.addWidget(self.create_button_4, 1, 0, 1, 1)
        self.create_button_5 = QtWidgets.QPushButton(self.widget)
        self.create_button_5.setObjectName("create_button_5")
        self.gridLayout_5.addWidget(self.create_button_5, 2, 0, 1, 1)
        self.gridLayout_6.addLayout(self.gridLayout_5, 0, 0, 1, 1)
        self.tableWidget = QtWidgets.QTableWidget(self.widget)
        self.tableWidget.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.tableWidget.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(10)
        self.tableWidget.setRowCount(1)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(0, 2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(0, 3, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(0, 4, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(0, 5, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(0, 6, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(0, 7, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(0, 8, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(0, 9, item)
        self.gridLayout_6.addWidget(self.tableWidget, 0, 1, 1, 1)
        self.groupBox_3 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_3.setGeometry(QtCore.QRect(620, 10, 421, 211))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.groupBox_3.setFont(font)
        self.groupBox_3.setFlat(False)
        self.groupBox_3.setObjectName("groupBox_3")
        self.label_9 = QtWidgets.QLabel(self.groupBox_3)
        self.label_9.setGeometry(QtCore.QRect(10, 110, 401, 21))
        self.label_9.setObjectName("label_9")
        self.label_11 = QtWidgets.QLabel(self.groupBox_3)
        self.label_11.setGeometry(QtCore.QRect(10, 30, 401, 21))
        self.label_11.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(self.groupBox_3)
        self.label_12.setGeometry(QtCore.QRect(10, 130, 221, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(True)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.label_13 = QtWidgets.QLabel(self.groupBox_3)
        self.label_13.setGeometry(QtCore.QRect(10, 50, 401, 61))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(True)
        self.label_13.setFont(font)
        self.label_13.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_13.setObjectName("label_13")
        self.label_14 = QtWidgets.QLabel(self.groupBox_3)
        self.label_14.setGeometry(QtCore.QRect(230, 130, 181, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(True)
        self.label_14.setFont(font)
        self.label_14.setObjectName("label_14")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):

        _translate = QtCore.QCoreApplication.translate

        self.groupBox.setTitle(_translate("Dialog", "New Trade"))
        self.label_1.setText(_translate("Dialog", "Security Type"))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        self.listWidget.setSortingEnabled(__sortingEnabled)
        self.label_2.setText(_translate("Dialog", "Strategy"))
        self.label_5.setText(_translate("Dialog", "Quantity"))
        self.label_6.setText(_translate("Dialog", "Price"))
        self.label_10.setText(_translate("Dialog", "SL"))
        self.label_7.setText(_translate("Dialog", "Leverage %"))
        self.create_button.setText(_translate("Dialog", "BUY"))
        self.label_8.setText(_translate("Dialog", "Date"))
        self.create_button_2.setText(_translate("Dialog", "SELL"))
        self.groupBox_2.setTitle(_translate("Dialog", "Open Positions"))
        self.create_button_3.setText(_translate("Dialog", "Refresh"))
        self.create_button_4.setText(_translate("Dialog", "Close Trade"))
        self.create_button_5.setText(_translate("Dialog", "Amend Trade"))
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("Dialog", "1"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Trade ID"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "Security"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "Side"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Dialog", "Quantity"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("Dialog", "Trade Price"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("Dialog", "Leverage"))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("Dialog", "Leverage %"))
        item = self.tableWidget.horizontalHeaderItem(7)
        item.setText(_translate("Dialog", "SL"))
        item = self.tableWidget.horizontalHeaderItem(8)
        item.setText(_translate("Dialog", "SL Level"))
        item = self.tableWidget.horizontalHeaderItem(9)
        item.setText(_translate("Dialog", "Open Date"))
        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        item = self.tableWidget.item(0, 0)
        item.setText(_translate("Dialog", "1"))
        item = self.tableWidget.item(0, 1)
        item.setText(_translate("Dialog", "Apple Inc"))
        item = self.tableWidget.item(0, 2)
        item.setText(_translate("Dialog", "BUY"))
        item = self.tableWidget.item(0, 3)
        item.setText(_translate("Dialog", "100"))
        item = self.tableWidget.item(0, 4)
        item.setText(_translate("Dialog", "120"))
        item = self.tableWidget.item(0, 5)
        item.setText(_translate("Dialog", "No"))
        item = self.tableWidget.item(0, 6)
        item.setText(_translate("Dialog", "0.00"))
        item = self.tableWidget.item(0, 7)
        item.setText(_translate("Dialog", "Yes"))
        item = self.tableWidget.item(0, 8)
        item.setText(_translate("Dialog", "100"))
        item = self.tableWidget.item(0, 9)
        item.setText(_translate("Dialog", "2019.02.10"))
        self.tableWidget.setSortingEnabled(__sortingEnabled)
        self.groupBox_3.setTitle(_translate("Dialog", "Info"))
        self.label_9.setText(_translate("Dialog", "Trade Descreption :"))
        self.label_11.setText(_translate("Dialog", "Strategy Description:"))
        self.label_12.setText(_translate("Dialog", " Notional Value:"))

        self.label_14.setText(_translate("Dialog", " Notional Value:"))

    def load_securities(self):

        self.db_connection = SQL(data_base=self.data_base, user_name=self.user_name, password=self.password)
        self.securities = self.db_connection.select_data(select_query="""select name from sec_info 
                                               where type = '{sec_type}'""".format(sec_type=self.cbox_1.currentText()))
        self.db_connection.close_connection()
        self.listWidget.clear()

        for sec, num in zip(list(self.securities["name"]), range(len(self.securities))):
            item = QtWidgets.QListWidgetItem()
            self.listWidget.addItem(item)
            item = self.listWidget.item(num)
            item.setText(str(sec))

    def load_strat_desc(self):

        self.strategy_desc = self.strategy_query[self.strategy_query.strategy_name == self.cbox_3.currentText()]
        self.label_13.setText(str(list(self.strategy_desc["strategy_desc"])[0]))


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = TradeEntry()
    ui.main_window(Dialog)
    Dialog.show()
    sys.exit(app.exec_())