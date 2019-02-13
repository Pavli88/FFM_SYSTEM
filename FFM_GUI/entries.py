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


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()

    ui = EntryWindows()
    ui.security()
    MainWindow.show()

    sys.exit(app.exec_())
