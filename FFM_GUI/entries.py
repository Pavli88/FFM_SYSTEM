from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QHBoxLayout, QVBoxLayout, QAction
from PyQt5.QtGui import QIcon
import sys
from FFM_SYSTEM.ffm_data import *
import datetime
from datetime import date
from pandas.tseries.offsets import BDay
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import os


class ProcessManager:

    def __init__(self, dialog, data_base, user_name, password):

        self.Dialog = dialog
        self.data_base = data_base
        self.user_name = user_name
        self.password = password

    def portfolio_holding_calculator(self):

        self.get_port_data = SQL(data_base=self.data_base,
                                 user_name=self.user_name,
                                 password=self.password).select_data("""select portfolio_name, inception_date 
                                                                        from portfolios 
                                                                        where portfolio_group = 'No'
                                                                        and portfolio_type != 'SAVING'""")

        self.Dialog.setObjectName("Dialog")
        self.Dialog.resize(360, 137)

        self.pushButton = QtWidgets.QPushButton(self.Dialog)
        self.pushButton.setGeometry(QtCore.QRect(30, 110, 151, 21))
        self.pushButton.setObjectName("pushButton")

        self.widget = QtWidgets.QWidget(self.Dialog)
        self.widget.setGeometry(QtCore.QRect(10, 10, 195, 91))
        self.widget.setObjectName("widget")

        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.comboBox = QtWidgets.QComboBox(self.widget)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItems(list(self.get_port_data["portfolio_name"]))

        self.gridLayout.addWidget(self.comboBox, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.dateEdit = QtWidgets.QDateEdit(self.widget)
        self.dateEdit.setObjectName("dateEdit")
        self.dateEdit.setDate(QtCore.QDate(date.today().year, date.today().month, date.today().day))

        self.gridLayout.addWidget(self.dateEdit, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)

        self.dateEdit_2 = QtWidgets.QDateEdit(self.widget)
        self.dateEdit_2.setObjectName("dateEdit_2")
        self.dateEdit_2.setDate(QtCore.QDate(date.today().year, date.today().month, date.today().day))

        self.gridLayout.addWidget(self.dateEdit_2, 2, 1, 1, 1)

        self.checkBox = QtWidgets.QCheckBox(self.Dialog)
        self.checkBox.setGeometry(QtCore.QRect(220, 10, 121, 16))
        self.checkBox.setObjectName("checkBox")
        self.checkBox_2 = QtWidgets.QCheckBox(self.Dialog)
        self.checkBox_2.setGeometry(QtCore.QRect(220, 30, 121, 16))
        self.checkBox_2.setObjectName("checkBox_2")
        self.checkBox_3 = QtWidgets.QCheckBox(self.Dialog)
        self.checkBox_3.setGeometry(QtCore.QRect(220, 50, 121, 16))
        self.checkBox_3.setObjectName("checkBox_3")
        self.checkBox_4 = QtWidgets.QCheckBox(self.Dialog)
        self.checkBox_4.setGeometry(QtCore.QRect(220, 70, 141, 16))
        self.checkBox_4.setObjectName("checkBox_4")
        self.checkBox_5 = QtWidgets.QCheckBox(self.Dialog)
        self.checkBox_5.setGeometry(QtCore.QRect(220, 90, 141, 16))
        self.checkBox_5.setObjectName("checkBox_5")
        self.checkBox_6 = QtWidgets.QCheckBox(self.Dialog)
        self.checkBox_6.setGeometry(QtCore.QRect(220, 110, 141, 16))
        self.checkBox_6.setObjectName("checkBox_6")

        self.checkBox.setText("All Process")
        self.checkBox_2.setText("Positions")
        self.checkBox_3.setText("NAV")
        self.checkBox_4.setText("Portfolio Holding")
        self.checkBox_5.setText("VAR")
        self.checkBox_6.setText("Drawdown")

        self.Dialog.setWindowTitle("Process Manager")
        self.pushButton.setText("Calculate")
        self.label.setText("Portfolio")
        self.label_2.setText("Start Date")
        self.label_3.setText("End Date")

    def calc_holding(self):

        if self.dateEdit.date() > self.dateEdit_2.date():
            print("Start date is larger than End date. Calculation is stopped")
        else:
            self.get_port_data = self.get_port_data[self.get_port_data["portfolio_name"] == self.comboBox.currentText()]

            if list(self.get_port_data["inception_date"])[0] > self.dateEdit.date():
                print("Holding start calculation date is less than portfolio inception date. Calculation is stopped")
            else:

                self.start_date = self.dateEdit.text().replace(". ", "-").replace(".", "")
                self.start_date = datetime.datetime.strptime(self.start_date, '%Y-%m-%d')

                self.end_date = self.dateEdit_2.text().replace(". ", "-").replace(".", "")
                self.end_date = datetime.datetime.strptime(self.end_date, '%Y-%m-%d')

                while self.start_date <= self.end_date:

                    if self.data_base == "dev_ffm_sys":
                        self.env = "dev"
                    else:
                        self.env = "live"

                    pos_cmd = """/home/apavlics/Developement/FFM_DEV/bin/python3.6 /home/apavlics/Developement/FFM_DEV/Codes/FFM_SYSTEM/ffm_process.py --db_user_name {user_name} --db_password {password} --env {env} --pos_calc Yes --portfolio {port} --rundate {date}""".format(user_name=self.user_name, password=self.password, port=self.comboBox.currentText(), date=str(self.start_date)[0:10].replace("-", ""), env=self.env)

                    if self.checkBox_2.isChecked():

                        os.system(pos_cmd)

                    nav_cmd = """/home/apavlics/Developement/FFM_DEV/bin/python3.6 /home/apavlics/Developement/FFM_DEV/Codes/FFM_SYSTEM/ffm_process.py --db_user_name {user_name} --db_password {password} --env {env} --nav_calc Yes --portfolio {port} --rundate {date}""".format(
                                user_name=self.user_name, password=self.password, port=self.comboBox.currentText(),
                                date=str(self.start_date)[0:10].replace("-", ""), env=self.env)

                    if self.checkBox_3.isChecked():

                        os.system(nav_cmd)

                    hold_cmd = """/home/apavlics/Developement/FFM_DEV/bin/python3.6 /home/apavlics/Developement/FFM_DEV/Codes/FFM_SYSTEM/ffm_process.py --db_user_name {user_name} --db_password {password} --env {env} --hold_calc Yes --portfolio {port} --rundate {date}""".format(
                                user_name=self.user_name, password=self.password, port=self.comboBox.currentText(),
                                date=str(self.start_date)[0:10].replace("-", ""), env=self.env)

                    if self.checkBox_4.isChecked():

                        os.system(hold_cmd)

                    var_cmd = """/home/apavlics/Developement/FFM_DEV/bin/python3.6 /home/apavlics/Developement/FFM_DEV/Codes/FFM_SYSTEM/ffm_risk_metrics.py --var Yes --db {db} --user_name {user_name} --password {password}  --port {port} --date {date} --save Yes""".format(db=self.data_base, user_name=self.user_name, password=self.password, port=self.comboBox.currentText(), date=str(self.start_date)[0:10].replace("-", ""))

                    if self.checkBox_5.isChecked():

                        os.system(var_cmd)

                    dd_cmd = """/home/apavlics/Developement/FFM_DEV/bin/python3.6 /home/apavlics/Developement/FFM_DEV/Codes/FFM_SYSTEM/ffm_risk_metrics.py --dd Yes --db {db} --user_name {user_name} --password {password}  --port {port} --date {date} --save Yes""".format(db=self.data_base, user_name=self.user_name, password=self.password, port=self.comboBox.currentText(), date=str(self.start_date)[0:10].replace("-", ""))

                    if self.checkBox_6.isChecked():

                        os.system(dd_cmd)

                    if self.checkBox.isChecked():

                        os.system(pos_cmd)
                        os.system(nav_cmd)
                        os.system(hold_cmd)
                        os.system(var_cmd)
                        os.system(dd_cmd)

                    self.start_date = self.start_date + BDay(1)


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
            self.create_button.setGeometry(QtCore.QRect(280, 100, 121, 51))
            self.create_button.setObjectName("pushButton")
        elif self.table_entry == "strategy_modell":
            self.create_button.setGeometry(QtCore.QRect(340, 70, 71, 21))
            self.create_button.setObjectName("create_button")
        elif self.table_entry == "strategy":
            self.create_button.setGeometry(QtCore.QRect(310, 130, 101, 21))
            self.create_button.setObjectName("create_button")
        elif self.table_entry == "cash flow":
            self.create_button.setGeometry(QtCore.QRect(310, 110, 101, 61))
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

        self.checkBox = QtWidgets.QCheckBox(self.Dialog)
        self.checkBox.setGeometry(QtCore.QRect(280, 70, 131, 23))
        self.checkBox.setObjectName("checkBox")

        self.port_name.setText("Portfolio Name")
        self.port_type.setText("Portfolio Type")
        self.currency.setText("Currency")
        self.full_name.setText("Full Name")
        self.inc_date.setText("Inception Date")
        self.create_button.setText("Create")
        self.checkBox.setText("Portfolio Group")

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

        self.Dialog.resize(428, 192)
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
        self.create_button.setGeometry(QtCore.QRect(310, 160, 101, 21))
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
        self.cbox_2.addItems(list(self.entry_connection.select_data("""select*from portfolios 
                                                                    where portfolio_group = 'No' 
                                                                  and portfolio_type != 'SAVING'""")["portfolio_name"]))

        self.cbox_3 = QtWidgets.QComboBox(self.Dialog)
        self.cbox_3.setGeometry(QtCore.QRect(180, 130, 231, 21))
        self.cbox_3.setObjectName("cbox_3")
        self.cbox_3.addItems(["MECHANIC", "DISCRETIONARY"])

        self.label_5 = QtWidgets.QLabel(self.Dialog)
        self.label_5.setGeometry(QtCore.QRect(20, 160, 151, 21))
        self.label_5.setObjectName("label_5")

        self.label_6 = QtWidgets.QLabel(self.Dialog)
        self.label_6.setGeometry(QtCore.QRect(20, 130, 151, 21))
        self.label_6.setObjectName("label_6")

        self.dateEdit = QtWidgets.QDateEdit(self.Dialog)
        self.dateEdit.setGeometry(QtCore.QRect(180, 160, 117, 26))
        self.dateEdit.setDate(QtCore.QDate(date.today().year, date.today().month, date.today().day))
        self.dateEdit.setObjectName("dateEdit")

        self.label_1.setText("Strategy Name")
        self.label_2.setText("Strategy Descreption")
        self.create_button.setText("Create")
        self.label_3.setText("Strategy Model")
        self.label_4.setText("Portfolio Name")
        self.label_5.setText("Start Date")
        self.label_6.setText("Strategy Type")

    def cash_flow(self):

        self.Dialog.resize(424, 220)
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
        self.cbox_1.addItems(list(self.entry_connection.select_data("""select*from portfolios 
                                                                    where portfolio_group = 'No'""")["portfolio_name"]))
        self.cbox_1.currentIndexChanged.connect(self.show_portfolio_currency)

        self.label_2 = QtWidgets.QLabel(self.Dialog)
        self.label_2.setGeometry(QtCore.QRect(20, 40, 151, 21))
        self.label_2.setObjectName("label_2")

        self.cbox_2 = QtWidgets.QComboBox(self.Dialog)
        self.cbox_2.setGeometry(QtCore.QRect(180, 40, 231, 21))
        self.cbox_2.setObjectName("cbox_2")
        self.cbox_2.addItems(["INFLOW", "OUTFLOW", "FUNDING"])

        self.label_4 = QtWidgets.QLabel(self.Dialog)
        self.label_4.setGeometry(QtCore.QRect(20, 100, 121, 21))
        self.label_4.setObjectName("label_4")

        self.label_6 = QtWidgets.QLabel(self.Dialog)
        self.label_6.setGeometry(QtCore.QRect(20, 130, 121, 21))
        self.label_6.setObjectName("label_6")

        self.label_7 = QtWidgets.QLabel(self.Dialog)
        self.label_7.setGeometry(QtCore.QRect(20, 160, 151, 21))
        self.label_7.setObjectName("label_7")
        self.label_7.setText("Client")

        self.label_8 = QtWidgets.QLabel(self.Dialog)
        self.label_8.setGeometry(QtCore.QRect(20, 190, 151, 21))
        self.label_8.setObjectName("label_8")
        self.label_8.setText("Comment")

        self.dateEdit = QtWidgets.QDateEdit(self.Dialog)
        self.dateEdit.setGeometry(QtCore.QRect(180, 100, 117, 26))
        self.dateEdit.setDate(QtCore.QDate(date.today().year, date.today().month, date.today().day))
        self.dateEdit.setObjectName("dateEdit")

        self.text_input_2 = QtWidgets.QLineEdit(self.Dialog)
        self.text_input_2.setGeometry(QtCore.QRect(180, 160, 121, 21))
        self.text_input_2.setObjectName("text_input_2")

        self.text_input_3 = QtWidgets.QLineEdit(self.Dialog)
        self.text_input_3.setGeometry(QtCore.QRect(180, 190, 231, 21))
        self.text_input_3.setObjectName("text_input_3")

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
        self.cbox_1.addItems(["BOND", "CRYPTO", "EQUITY", "FX", "FUTURES", "LOAN", "OPTION"])
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
        elif self.cbox_1.currentText() == "LOAN":
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

                if self.checkBox.isChecked():
                    self.port_group = "Yes"
                else:
                    self.port_group = "No"

                self.entry_connection.portfolios(portfolio_name=self.port_name_line.text(),
                                                 portfolio_type=self.port_type_cbox.currentText(),
                                                 currency=self.currency_line.text(),
                                                 full_name=self.full_name_line.text(),
                                                 inception_date=self.dateEdit.text().replace(". ", "").replace(".", ""),
                                                 portfolio_group=self.port_group)

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
                                                   port_name=self.cbox_2.currentText()))["portfolio_id"].values)[0],
                                               strat_type=self.cbox_3.currentText())

                self.Dialog.close()

        elif self.table_entry == "cash flow":

            if len(self.text_input_1.text()) < 2:

                self.msg_box(message="Cash Flow field is empty !", title="Notification", )

            else:

                if self.cbox_2.currentText() == "OUTFLOW":

                    self.cash_flow_ammount = float(self.text_input_1.text())*-1
                else:
                    self.cash_flow_ammount = self.text_input_1.text()

                self.port_code = list(self.entry_connection.select_data("""select*from portfolios 
                                                                  where portfolio_name = '{port_name}'""".format(
                                                            port_name=self.cbox_1.currentText()))["portfolio_id"])[0]

                self.entry_connection.cash_flow(port_code=self.port_code,
                                                ammount=self.cash_flow_ammount,
                                                cft=self.cbox_2.currentText(),
                                                date=self.dateEdit.text().replace(". ", "").replace(".", ""),
                                                currency=self.label_5.text(),
                                                comment=self.text_input_3.text(),
                                                client=self.text_input_2.text())

                if self.cbox_2.currentText() == "FUNDING":

                    self.id = SQL(data_base=self.db,
                                  user_name=self.user_name,
                                  password=self.password).select_data(select_query="""select nav_id from portfolio_nav""")

                    self.id = list(self.id["nav_id"])

                    if len(self.id) < 1:
                        self.nav_id = 1
                    else:
                        self.nav_id = list(self.id)[-1] + 1

                    SQL(data_base=self.db,
                        user_name=self.user_name,
                        password=self.password).insert_data(insert_query="""insert into portfolio_nav (date, 
                                                                            portfolio_code, nav_id, cash_balance) 
                                                                            values ('{date}', '{port_code}', '{nav_id}', 
                                '{cash_bal}')""".format(date=self.dateEdit.text().replace(". ", "").replace(".", ""),
                                                        port_code=self.port_code,
                                                        cash_bal=self.cash_flow_ammount,
                                                        nav_id=self.nav_id))

                self.msg_box(message="""{ammount} {currency} was booked for {port}""".format(ammount=self.text_input_1.text(),
                                                                                             currency=self.label_5.text(),
                                                                                             port=self.cbox_1.currentText()), title="Notification", )

                self.Dialog.close()

        elif self.table_entry == "security":

            if len(self.text_input_1.text()) < 2:

                self.msg_box(message="Security Name field is empty !", title="Notification", )

            else:

                if (self.cbox_1.currentText() == "FX") or (self.cbox_1.currentText() == "CRYPTO") or (self.cbox_1.currentText() == "LOAN"):

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

        pd.set_option('display.max_rows', 500)
        pd.set_option('display.max_columns', 500)
        pd.set_option('display.width', 1000)

        self.dialog = Dialog
        self.data_base = data_base
        self.user_name = user_name
        self.password = password
        self.portfolio_name = portfolio_name

        self.db_connection = SQL(data_base=self.data_base, user_name=self.user_name, password=self.password)
        self.strategy_query = self.db_connection.select_data(select_query="""select*from strategy 
        where portfolio_code in (select portfolio_id from portfolios 
                                 where portfolio_name = '{portfolio_name}')""".format(portfolio_name=portfolio_name))
        self.portfolio_data = self.db_connection.select_data(select_query="""select*from portfolios 
                                               where portfolio_name = '{portfolio}'""".format(portfolio=portfolio_name))

        self.collaterals = self.db_connection.select_data(select_query="""select*from sec_info 
                                                                          where type = 'LOAN' 
                                                                          and ticker in ('MRGN', 'CLTR')""")

        self.cash_flow_data = self.db_connection.select_data(select_query="""select*from cash_flow 
                                                                             where portfolio_code = {port_code}
                                                                             """.format(
                                                              port_code=list(self.portfolio_data["portfolio_id"])[0]))

        self.db_connection.close_connection()

        Dialog.setObjectName("Dialog")
        Dialog.resize(1191, 899)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setWindowTitle("Trade Entry - " + portfolio_name)

        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(9, 9, 580, 271))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName("groupBox")

        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_4.setObjectName("gridLayout_4")

        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")

        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")

        self.gridLayout_7 = QtWidgets.QGridLayout()
        self.gridLayout_7.setObjectName("gridLayout_7")

        self.label_1 = QtWidgets.QLabel(self.groupBox)
        self.label_1.setObjectName("label_1")
        self.gridLayout.addWidget(self.label_1, 0, 0, 1, 1)

        self.cbox_1 = QtWidgets.QComboBox(self.groupBox)
        self.cbox_1.setObjectName("cbox_1")
        self.cbox_1.addItems(["BOND", "CRYPTO", "EQUITY", "FUTURES", "FX", "OPTION"])
        self.gridLayout.addWidget(self.cbox_1, 0, 1, 1, 1)

        self.listWidget = QtWidgets.QListWidget(self.groupBox)
        self.listWidget.setObjectName("listWidget")
        self.listWidget.itemSelectionChanged.connect(self.get_last_price)

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
        self.gridLayout_2.addWidget(self.cbox_3, 0, 1, 1, 3)

        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 1, 0, 1, 1)

        self.text_input_2 = QtWidgets.QLineEdit(self.groupBox)
        self.text_input_2.setObjectName("text_input_2")
        self.text_input_2.textChanged.connect(self.calculate_notional)
        self.gridLayout_2.addWidget(self.text_input_2, 1, 1, 1, 3)

        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setObjectName("label_6")

        self.label_15 = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_15.setFont(font)
        self.label_15.setAlignment(QtCore.Qt.AlignCenter)
        self.label_15.setObjectName("label_15")
        self.gridLayout_2.addWidget(self.label_15, 2, 2, 1, 1)

        self.gridLayout_2.addWidget(self.label_6, 2, 0, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.groupBox)
        self.label_10.setObjectName("label_10")
        self.gridLayout_2.addWidget(self.label_10, 4, 0, 1, 1)

        self.text_input_3 = QtWidgets.QLineEdit(self.groupBox)
        self.text_input_3.setObjectName("text_input_3")
        self.gridLayout_2.addWidget(self.text_input_3, 4, 1, 1, 3)

        self.text_input_4 = QtWidgets.QLineEdit(self.groupBox)
        self.text_input_4.setObjectName("text_input_4")
        self.gridLayout_2.addWidget(self.text_input_4, 3, 2, 1, 2)

        self.label_7 = QtWidgets.QLabel(self.groupBox)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 5, 0, 1, 1)

        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.doubleSpinBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.doubleSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.doubleSpinBox.setMaximum(100.0)
        self.doubleSpinBox.setSingleStep(5.0)
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.gridLayout_2.addWidget(self.doubleSpinBox, 5, 1, 1, 2)
        self.doubleSpinBox.valueChanged.connect(self.calculate_margin)

        self.create_button = QtWidgets.QPushButton(self.groupBox)
        self.create_button.setObjectName("create_button")
        self.create_button.clicked.connect(lambda: self.enter_trade(side="BUY"))
        self.gridLayout_2.addWidget(self.create_button, 5, 3, 1, 1)

        self.label_8 = QtWidgets.QLabel(self.groupBox)
        self.label_8.setObjectName("label_8")
        self.gridLayout_2.addWidget(self.label_8, 6, 0, 1, 1)

        self.dateEdit = QtWidgets.QDateEdit(self.groupBox)
        self.dateEdit.setObjectName("dateEdit")
        self.dateEdit.setDate(QtCore.QDate(date.today().year, date.today().month, date.today().day))
        self.gridLayout_2.addWidget(self.dateEdit, 6, 1, 1, 2)

        self.create_button_2 = QtWidgets.QPushButton(self.groupBox)
        self.create_button_2.setObjectName("create_button_2")
        self.create_button_2.clicked.connect(lambda: self.enter_trade(side="SELL"))
        self.gridLayout_2.addWidget(self.create_button_2, 6, 3, 1, 1)

        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 1, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_3, 0, 0, 1, 1)

        self.groupBox_2 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_2.setGeometry(QtCore.QRect(9, 286, 1171, 236))
        self.groupBox_2.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.groupBox_2.setFlat(False)
        self.groupBox_2.setObjectName("groupBox_2")

        self.widget = QtWidgets.QWidget(self.groupBox_2)
        self.widget.setGeometry(QtCore.QRect(10, 32, 1001, 221))
        self.widget.setObjectName("widget")

        self.checkBox = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox.setObjectName("checkBox")
        self.gridLayout_2.addWidget(self.checkBox, 3, 0, 1, 2)
        self.checkBox.setText("Backdated Price")

        self.tableWidget = QtWidgets.QTableWidget(self.groupBox_2)
        self.tableWidget.setGeometry(QtCore.QRect(119, 32, 1041, 192))
        self.tableWidget.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.tableWidget.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(10)
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

        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText("Trade ID")
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText("Security")
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText("Side")
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText("Quantity")
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText("Trade Price")
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText("Leverage")
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText("Leverage %")
        item = self.tableWidget.horizontalHeaderItem(7)
        item.setText("SL")
        item = self.tableWidget.horizontalHeaderItem(8)
        item.setText("SL Level")
        item = self.tableWidget.horizontalHeaderItem(9)
        item.setText("Open Date")

        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.setSortingEnabled(__sortingEnabled)

        self.gridLayout_7.addWidget(self.groupBox, 0, 0, 1, 1)

        # Modify buttons

        self.widget2 = QtWidgets.QWidget(self.groupBox_2)
        self.widget2.setGeometry(QtCore.QRect(10, 30, 101, 197))
        self.widget2.setObjectName("widget2")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget2)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.create_button_4 = QtWidgets.QPushButton(self.widget2)
        self.create_button_4.setObjectName("create_button_4")
        self.verticalLayout.addWidget(self.create_button_4)
        self.create_button_4.setText("Close Trade")
        self.create_button_4.clicked.connect(self.close_trade)

        self.label = QtWidgets.QLabel(self.widget2)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label.setText("Stop Level")

        self.text_input_5 = QtWidgets.QLineEdit(self.widget2)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.text_input_5.setFont(font)
        self.text_input_5.setObjectName("text_input_5")
        self.verticalLayout.addWidget(self.text_input_5)

        self.create_button_5 = QtWidgets.QPushButton(self.widget2)
        self.create_button_5.setObjectName("create_button_5")
        self.verticalLayout.addWidget(self.create_button_5)
        self.create_button_5.setText("->")
        self.create_button_5.clicked.connect(self.stop_button)

        self.label_4 = QtWidgets.QLabel(self.widget2)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.label_4.setText("Quantity")

        self.text_input_6 = QtWidgets.QLineEdit(self.widget2)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.text_input_6.setFont(font)
        self.text_input_6.setObjectName("text_input_6")
        self.verticalLayout.addWidget(self.text_input_6)

        self.create_button_6 = QtWidgets.QPushButton(self.widget2)
        self.create_button_6.setObjectName("create_button_6")
        self.verticalLayout.addWidget(self.create_button_6)
        self.create_button_6.setText("->")

        # =====================================================


        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(10, 530, 70, 21))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_3.setText("Start Date")

        self.dateEdit_2 = QtWidgets.QDateEdit(Dialog)
        self.dateEdit_2.setGeometry(QtCore.QRect(87, 526, 117, 26))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.dateEdit_2.setFont(font)
        self.dateEdit_2.setObjectName("dateEdit_2")

        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(210, 526, 80, 25))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("Refresh")
        self.pushButton.clicked.connect(self.get_last_price)

        self.groupBox_3 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_3.setGeometry(QtCore.QRect(595, 9, 584, 271))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.groupBox_3.setFont(font)
        self.groupBox_3.setFlat(False)
        self.groupBox_3.setObjectName("groupBox_3")

        self.label_9 = QtWidgets.QLabel(self.groupBox_3)
        self.label_9.setGeometry(QtCore.QRect(10, 170, 141, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")

        self.label_11 = QtWidgets.QLabel(self.groupBox_3)
        self.label_11.setGeometry(QtCore.QRect(10, 30, 291, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_11.setFont(font)
        self.label_11.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.label_11.setObjectName("label_11")

        self.label_13 = QtWidgets.QLabel(self.groupBox_3)
        self.label_13.setGeometry(QtCore.QRect(10, 50, 401, 61))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(True)
        self.label_13.setFont(font)
        self.label_13.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_13.setObjectName("label_13")
        self.label_14 = QtWidgets.QLabel(self.groupBox_3)
        self.label_14.setGeometry(QtCore.QRect(320, 50, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(True)
        self.label_14.setFont(font)
        self.label_14.setObjectName("label_14")
        self.label_14.setText("Full Name:")

        self.label_16 = QtWidgets.QLabel(self.groupBox_3)
        self.label_16.setGeometry(QtCore.QRect(320, 30, 211, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_16.setFont(font)
        self.label_16.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.label_16.setObjectName("label_16")
        self.label_17 = QtWidgets.QLabel(self.groupBox_3)
        self.label_17.setGeometry(QtCore.QRect(320, 70, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(True)
        self.label_17.setFont(font)
        self.label_17.setObjectName("label_17")
        self.label_18 = QtWidgets.QLabel(self.groupBox_3)
        self.label_18.setGeometry(QtCore.QRect(320, 90, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(True)
        self.label_18.setFont(font)
        self.label_18.setObjectName("label_18")
        self.label_19 = QtWidgets.QLabel(self.groupBox_3)
        self.label_19.setGeometry(QtCore.QRect(320, 110, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(True)
        self.label_19.setFont(font)
        self.label_19.setObjectName("label_19")
        self.label_20 = QtWidgets.QLabel(self.groupBox_3)
        self.label_20.setGeometry(QtCore.QRect(320, 130, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(True)
        self.label_20.setFont(font)
        self.label_20.setObjectName("label_20")
        self.label_21 = QtWidgets.QLabel(self.groupBox_3)
        self.label_21.setGeometry(QtCore.QRect(320, 150, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(True)
        self.label_21.setFont(font)
        self.label_21.setObjectName("label_21")
        self.label_22 = QtWidgets.QLabel(self.groupBox_3)
        self.label_22.setGeometry(QtCore.QRect(320, 170, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(True)
        self.label_22.setFont(font)
        self.label_22.setObjectName("label_22")
        self.label_23 = QtWidgets.QLabel(self.groupBox_3)
        self.label_23.setGeometry(QtCore.QRect(10, 190, 111, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(True)
        self.label_23.setFont(font)
        self.label_23.setObjectName("label_23")
        self.label_24 = QtWidgets.QLabel(self.groupBox_3)
        self.label_24.setGeometry(QtCore.QRect(10, 210, 111, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(True)
        self.label_24.setFont(font)
        self.label_24.setObjectName("label_24")
        self.label_25 = QtWidgets.QLabel(self.groupBox_3)
        self.label_25.setGeometry(QtCore.QRect(10, 230, 111, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(True)
        self.label_25.setFont(font)
        self.label_25.setObjectName("label_25")

        self.label_27 = QtWidgets.QLabel(self.groupBox_3)
        self.label_27.setGeometry(QtCore.QRect(420, 70, 131, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(True)
        self.label_27.setFont(font)
        self.label_27.setObjectName("label_27")
        self.label_27.setText(str(list(self.portfolio_data["inception_date"])[0]))

        self.label_28 = QtWidgets.QLabel(self.groupBox_3)
        self.label_28.setGeometry(QtCore.QRect(420, 90, 131, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(True)
        self.label_28.setFont(font)
        self.label_28.setObjectName("label_28")
        self.label_28.setText(str(list(self.cash_flow_data["date"])[0]))

        self.label_29 = QtWidgets.QLabel(self.groupBox_3)
        self.label_29.setGeometry(QtCore.QRect(420, 110, 131, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(True)
        self.label_29.setFont(font)
        self.label_29.setObjectName("label_29")
        self.label_29.setText(str(list(self.cash_flow_data["ammount"])[0]))

        self.label_30 = QtWidgets.QLabel(self.groupBox_3)
        self.label_30.setGeometry(QtCore.QRect(420, 130, 131, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(True)
        self.label_30.setFont(font)
        self.label_30.setObjectName("label_30")
        self.label_30.setText(list(self.portfolio_data["portfolio_type"])[0])

        self.label_31 = QtWidgets.QLabel(self.groupBox_3)
        self.label_31.setGeometry(QtCore.QRect(420, 150, 131, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(True)
        self.label_31.setFont(font)
        self.label_31.setObjectName("label_31")
        self.label_31.setText(list(self.cash_flow_data["currency"])[0])

        self.label_32 = QtWidgets.QLabel(self.groupBox_3)
        self.label_32.setGeometry(QtCore.QRect(420, 170, 131, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(True)
        self.label_32.setFont(font)
        self.label_32.setObjectName("label_32")
        self.label_32.setText(str(sum(list(self.cash_flow_data["ammount"]))))

        self.label_33 = QtWidgets.QLabel(self.groupBox_3)
        self.label_33.setGeometry(QtCore.QRect(420, 50, 131, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(True)
        self.label_33.setFont(font)
        self.label_33.setObjectName("label_33")
        self.label_33.setText(str(list(self.portfolio_data["full_name"])[0]))

        self.label_34 = QtWidgets.QLabel(self.groupBox_3)
        self.label_34.setGeometry(QtCore.QRect(130, 190, 181, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(True)
        self.label_34.setFont(font)
        self.label_34.setObjectName("label_34")

        self.label_35 = QtWidgets.QLabel(self.groupBox_3)
        self.label_35.setGeometry(QtCore.QRect(130, 210, 181, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(True)
        self.label_35.setFont(font)
        self.label_35.setObjectName("label_35")
        self.label_36 = QtWidgets.QLabel(self.groupBox_3)
        self.label_36.setGeometry(QtCore.QRect(130, 230, 181, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(True)
        self.label_36.setFont(font)
        self.label_36.setObjectName("label_36")
        self.gridLayout_7.addWidget(self.groupBox_3, 0, 1, 1, 1)

        self.label_26 = QtWidgets.QLabel(self.groupBox_3)
        self.label_26.setGeometry(QtCore.QRect(10, 250, 111, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(True)
        self.label_26.setFont(font)
        self.label_26.setObjectName("label_26")
        self.label_26.setText("Trade Ammount:")

        self.label_37 = QtWidgets.QLabel(self.groupBox_3)
        self.label_37.setGeometry(QtCore.QRect(130, 250, 131, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(True)
        self.label_37.setFont(font)
        self.label_37.setObjectName("label_37")

        self.label_38 = QtWidgets.QLabel(self.groupBox_3)
        self.label_38.setGeometry(QtCore.QRect(280, 230, 111, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(True)
        self.label_38.setFont(font)
        self.label_38.setObjectName("label_38")
        self.label_38.setText("Margin %")

        self.label_39 = QtWidgets.QLabel(self.groupBox_3)
        self.label_39.setGeometry(QtCore.QRect(280, 250, 131, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(True)
        self.label_39.setFont(font)
        self.label_39.setObjectName("label_39")

        self.label_16.setText("Portfolio Description:")
        self.label_17.setText("Inception Date:")
        self.label_18.setText("Funding Date:")
        self.label_19.setText( "Initial Funding:")
        self.label_20.setText("Type:")
        self.label_21.setText("Currency:")
        self.label_22.setText( "Cash Balance:")
        self.label_23.setText("Notional:")
        self.label_24.setText("Money at Risk:")
        self.label_25.setText("Margin Ammount:")

        self.label_35.setText("i")

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
        self.groupBox_3.setTitle(_translate("Dialog", "Info"))
        self.label_9.setText(_translate("Dialog", "Trade Descreption :"))
        self.label_11.setText(_translate("Dialog", "Strategy Description:"))

    def stop_button(self):

        print(self.tableWidget.selectedItems()[0].text())

        print(self.tableWidget.selectedItems()[1].text())

    def load_chart(self, chart_date, Dialog, ticker):

        # Chart Frame

        try:
            self.frame = QtWidgets.QFrame(Dialog)
            self.frame.setGeometry(QtCore.QRect(10, 560, 1171, 331))
            self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
            self.frame.setObjectName("frame")

            self.start_date = chart_date.replace(". ", "").replace(".", "")
            print(self.start_date)

            self.dpi = 100
            self.fig = Figure((10.0, 5.0), dpi=self.dpi)
            self.canvas = FigureCanvas(self.fig)
            self.canvas.setParent(self.frame)

            self.ax = self.fig.add_subplot(111)

            x = StockData(stock_list=[ticker], start_date=date(year=int(self.start_date[0:4]),
                                                               month=int(self.start_date[4:6]),
                                                               day=int(self.start_date[6:]))).stock_data_frame()

            opens = np.asarray(x['Open'])
            lows = np.asarray(x['Low'])
            highs = np.asarray(x['High'])
            closes = np.asarray(x['Close'])
            candlestick2_ohlc(self.ax, opens, highs, lows, closes, width=0.6, colorup='green', colordown='r')

            # Layout with box sizers

            hbox = QHBoxLayout()
            vbox = QVBoxLayout()
            vbox.addWidget(self.canvas)
            vbox.addLayout(hbox)

            self.frame.setLayout(vbox)
            self.frame.show()
        except:
            print("Error while downloading data")

    def calculate_margin(self):

        try:
            if self.checkBox.isChecked():
                self.trd_price = self.text_input_4.text()
            else:
                self.trd_price = self.label_15.text()

            print("Trade Price:", self.trd_price)

            self.label_36.setText(str(float(self.doubleSpinBox.value())/100*round(float(self.text_input_2.text()) * float(self.trd_price), 2)))
            self.trade_cash = round(float(self.text_input_2.text()) * float(self.trd_price), 2)-(float(self.doubleSpinBox.value())/100*round(float(self.text_input_2.text()) * float(self.trd_price), 2))
            self.label_37.setText(str(self.trade_cash))
            self.label_39.setText(str(round((float(self.doubleSpinBox.value()) / 100 * round(
                float(self.text_input_2.text()) * float(self.trd_price), 2) / self.trade_cash), 2) * 100) + " %")
        except:
            pass

    def calculate_notional(self):

        try:
            if self.checkBox.isChecked():
                self.trd_price = self.text_input_4.text()
            else:
                self.trd_price = self.label_15.text()

            print("Trade Price:", self.trd_price)

            self.label_34.setText(str(round(float(self.text_input_2.text()) * float(self.trd_price), 2)))
            self.trade_cash = round(float(self.text_input_2.text()) * float(self.trd_price), 2)-(float(self.doubleSpinBox.value())/100*round(float(self.text_input_2.text()) * float(self.trd_price), 2))
            self.label_37.setText(str(self.trade_cash))
            self.label_39.setText(str(round((float(self.doubleSpinBox.value()) / 100 * round(
                float(self.text_input_2.text()) * float(self.trd_price), 2) / self.trade_cash), 2) * 100) + " %")
        except:
            pass

    def close_trade(self):

        self.db_connection = SQL(data_base=self.data_base, user_name=self.user_name, password=self.password)
        self.sec_data = self.db_connection.select_data(select_query="""select * from trade 
                               where trade_id = '{trd_id}'""".format(trd_id=self.tableWidget.selectedItems()[0].text()))

        # Updating trade status to closed
        self.db_connection.insert_data(insert_query="""update trade set status = 'CLOSED' 
                                     where trade_id = {trade_id}""".format(trade_id=list(self.sec_data["trade_id"])[0]))
        self.db_connection.close_connection()

        print(self.sec_data)

        self.last_price = OnlineData(ticker=list(self.sec_data["ticker"])[0]).last_eq_price()
        self.last_price = list(self.last_price["price"])[0]

        if list(self.sec_data["side"])[0] == "BUY":

            self.side = "SELL"
            self.action = "SELL_TO_CLOSE"

        elif list(self.sec_data["side"])[0] == "SELL":

            self.side = "BUY"
            self.action = "BUY_TO_CLOSE"

        if self.checkBox.isChecked():
            self.trd_price = self.text_input_4.text()
        else:
            self.trd_price = self.last_price

        print("Close Price:", self.trd_price)

        self.quantity = list(self.sec_data["quantity"])[0] * -1
        self.margin = list(self.sec_data["margin_bal"])[0] * -1
        self.coll = self.sec_data["collateral"][0] * -1

        Entries(data_base=self.data_base,
                user_name=self.user_name,
                password=self.password).trade(date=self.dateEdit.text().replace(". ", "").replace(".", ""),
                                              portfolio_code=list(self.sec_data["portfolio_code"])[0],
                                              strategy_code=list(self.sec_data["strategy_code"])[0],
                                              side=self.side,
                                              quantity=self.quantity,
                                              trade_price=float(self.trd_price),
                                              leverage="No",
                                              sl="No",
                                              sl_level=0,
                                              sec_id=list(self.sec_data["sec_id"])[0],
                                              leverage_perc=0,
                                              ticker=list(self.sec_data["ticker"])[0],
                                              margin_bal=self.margin,
                                              collateral=self.coll,
                                              action=self.action,
                                              status="CLOSED")

        # Cashflow

        Entries(data_base=self.data_base,
                user_name=self.user_name,
                password=self.password).cash_flow(port_code=list(self.sec_data["portfolio_code"])[0],
                                                  ammount=(list(self.sec_data["quantity"])[0] * float(self.trd_price))-self.margin,
                                                  cft="INFLOW",
                                                  date=self.dateEdit.text().replace(". ", "").replace(".", ""),
                                                  currency=list(self.portfolio_data["currency"])[0],
                                                  comment="Trade",
                                                  client=self.user_name)

        MsgBoxes().info_box(message="Trade has been closed !", title="Notification")

        self.load_strat_desc()

        self.cash_flow_data = SQL(data_base=self.data_base,
                                  user_name=self.user_name,
                                  password=self.password).select_data(select_query="""select*from cash_flow 
                                                                                      where portfolio_code = {port_code}
                                                                                                             """.format(
                                                                port_code=list(self.portfolio_data["portfolio_id"])[0]))

        self.label_32.setText(str(sum(list(self.cash_flow_data["ammount"]))))

        # Updating trade_analysis table

    def enter_trade(self, side):

        if self.trade_cash > float(self.label_32.text()):
            MsgBoxes().info_box(message="Position is too large. There is not enough cash in the portfolio !", title="Notification")
        else:

            self.trd_date = self.dateEdit.text().replace(". ", "-").replace(".", "")
            self.trd_date = datetime.datetime.strptime(self.trd_date, '%Y-%m-%d')

            self.nav_date = str(self.trd_date + BDay(-1)).replace("-", "")[0:8]

            self.db_connection = SQL(data_base=self.data_base, user_name=self.user_name, password=self.password)

            self.port_nav = self.db_connection.select_data(select_query="""select pn.total_nav 
                                                                           from portfolio_nav pn, portfolios p
                                                                           where pn.portfolio_code = p.portfolio_id
                                                                           and p.portfolio_name = '{port_name}'
                                                                           and pn.date = '{nav_date}'""".format(
                port_name=self.portfolio_name,
                nav_date=self.nav_date))

            if len(self.port_nav["total_nav"]) == 0:
                MsgBoxes().info_box(message="NAV data is missing as of " + str(self.nav_date) + " !",
                                    title="Notification")
            else:

                self.strat_code_query = self.db_connection.select_data(select_query="""select*from strategy 
                                           where strategy_name = '{strat_name}'""".format(strat_name=self.cbox_3.currentText()))
                self.db_connection.close_connection()

                if self.doubleSpinBox.value() > 0.00:
                    self.leverage = "Yes"
                else:
                    self.leverage = "No"

                print("Leverage", self.leverage)

                if self.checkBox.isChecked():
                    self.trd_price = self.text_input_4.text()
                else:
                    self.trd_price = self.label_15.text()

                print("Trade Price:", self.trd_price)

                if side == "SELL":
                    self.quantity = int(self.text_input_2.text()) * -1
                    self.collateral_bal = self.quantity * float(self.trd_price)*-2
                    self.action = "SELL_TO_OPEN"

                else:
                    self.quantity = int(self.text_input_2.text())
                    self.collateral_bal = 0
                    self.action = "BUY_TO_OPEN"

                print("Trade Action:", self.action)

                if self.leverage == "Yes":

                    self.margin = int(self.text_input_2.text())*float(self.trd_price)*-1*(float(self.doubleSpinBox.value())/100)

                    self.cash_flow_ammount = int(self.text_input_2.text()) * float(self.trd_price) * -1 * \
                                             ((100 - float(self.doubleSpinBox.value())) / 100)
                else:
                    self.margin = 0

                    self.cash_flow_ammount = int(self.text_input_2.text()) * float(self.trd_price) * -1

                print("Margin:", self.margin)
                print("Cash Flow Ammount:", self.cash_flow_ammount)

                if len(self.text_input_3.text()) > 0:
                    self.sl = "Yes"
                    self.sl_level = self.text_input_3.text()

                    if (side == "BUY") and (float(self.trd_price) < float(self.sl_level)):
                        MsgBoxes().info_box(message="BUY Trade. SL Price is larger than trade price !", title="Notification")
                    elif (side == "SELL") and (float(self.trd_price) > float(self.sl_level)):
                        MsgBoxes().info_box(message="SELL Trade. SL Price is smaller than trade price !", title="Notification")
                    else:

                        # Trade Entry

                        self.trd_id = Entries(data_base=self.data_base,
                                user_name=self.user_name,
                                password=self.password).trade(date=self.dateEdit.text().replace(". ", "").replace(".", ""),
                                                              portfolio_code=list(self.strat_code_query["portfolio_code"])[0],
                                                              strategy_code=list(self.strat_code_query["strategy_code"])[0],
                                                              side=side,
                                                              quantity=self.quantity,
                                                              trade_price=float(self.trd_price),
                                                              leverage=self.leverage,
                                                              sl=self.sl,
                                                              sl_level=float(self.sl_level),
                                                              sec_id=list(self.sec_data["sec_id"])[0],
                                                              leverage_perc=self.doubleSpinBox.value(),
                                                              ticker=list(self.sec_data["ticker"])[0],
                                                              margin_bal=self.margin,
                                                              collateral=self.collateral_bal,
                                                              action=self.action,
                                                              status="OPEN")


                        Entries(data_base=self.data_base,
                                user_name=self.user_name,
                                password=self.password).cash_flow(port_code=list(self.strat_code_query["portfolio_code"])[0],
                                                                  ammount=self.cash_flow_ammount,
                                                                  cft="OUTFLOW",
                                                                  date=self.dateEdit.text().replace(". ", "").replace(".", ""),
                                                                  currency=list(self.portfolio_data["currency"])[0],
                                                                  comment="Trade",
                                                                  client=self.user_name)

                        MsgBoxes().info_box(message="Trade was booked successfully !", title="Notification")

                        self.load_strat_desc()

                else:
                    self.sl = "No"
                    self.sl_level = 0

                    # Trade Entry

                    self.trd_id =Entries(data_base=self.data_base,
                            user_name=self.user_name,
                            password=self.password).trade(date=self.dateEdit.text().replace(". ", "").replace(".", ""),
                                                          portfolio_code=list(self.strat_code_query["portfolio_code"])[0],
                                                          strategy_code=list(self.strat_code_query["strategy_code"])[0],
                                                          side=side,
                                                          quantity=self.quantity,
                                                          trade_price=float(self.trd_price),
                                                          leverage=self.leverage,
                                                          sl=self.sl,
                                                          sl_level=float(self.sl_level),
                                                          sec_id=list(self.sec_data["sec_id"])[0],
                                                          leverage_perc=self.doubleSpinBox.value(),
                                                          ticker=list(self.sec_data["ticker"])[0],
                                                          margin_bal=int(self.text_input_2.text())*float(self.trd_price)*-1*(float(self.doubleSpinBox.value())/100),
                                                          collateral=self.collateral_bal,
                                                          action=self.action,
                                                          status="OPEN")

                    # Cash flow side of the trade

                    Entries(data_base=self.data_base,
                            user_name=self.user_name,
                            password=self.password).cash_flow(port_code=list(self.strat_code_query["portfolio_code"])[0],
                                                              ammount=self.cash_flow_ammount,
                                                              cft="OUTFLOW",
                                                              date=self.dateEdit.text().replace(". ", "").replace(".", ""),
                                                              currency=list(self.portfolio_data["currency"])[0],
                                                              comment="Trade",
                                                              client=self.user_name)

                    MsgBoxes().info_box(message="Trade was booked successfully !", title="Notification")


                    self.load_strat_desc()

                self.cash_flow_data = SQL(data_base=self.data_base,
                                          user_name=self.user_name,
                                          password=self.password).select_data(select_query="""select*from cash_flow 
                                                                                        where portfolio_code = {port_code}
                                                                                                         """.format(
                                                                    port_code=list(self.portfolio_data["portfolio_id"])[0]))

                self.label_32.setText(str(sum(list(self.cash_flow_data["ammount"]))))

                # Updating trade_analysis table

                self.trd_id_an = SQL(data_base=self.data_base,
                                     user_name=self.user_name,
                                     password=self.password).select_data(select_query="""SELECT MAX(id) AS 'max_id' FROM trade_analysis""")

                self.sl_cost = abs((self.quantity * float(self.sl_level)) - (self.quantity * float(self.trd_price))) * -1

                if list(self.trd_id_an["max_id"])[0] is None:
                    self.trd_id_an = 1
                else:
                    self.trd_id_an = list(self.trd_id_an["max_id"])[0]+1

                self.sl_cost_nav = abs(self.sl_cost)/list(self.port_nav["total_nav"])[0]

                SQL(data_base=self.data_base,
                    user_name=self.user_name,
                    password=self.password).insert_data(insert_query="""insert into trade_analysis 
                                                                                        (trade_id, open_date, portfolio_id, strategy_id,
                                                                                         trd_price, quantity, sl, cost, sl_cost, status, sl_cost_to_nav, id) 
    
                                                                                        values ('{trd_id}', '{open_date}', 
                                                                                        '{portfolio_id}', '{strat_id}', '{trd_price}', 
                                                                                        '{quantity}', '{sl}', '{cost}', '{sl_cost}', 'OPEN', '{slcn}','{id}')""".format(
                    trd_id=self.trd_id,
                    open_date=self.dateEdit.text().replace(". ", "").replace(".", ""),
                    portfolio_id=list(self.strat_code_query["portfolio_code"])[0],
                    strat_id=list(self.strat_code_query["strategy_code"])[0],
                    trd_price=float(self.trd_price),
                    quantity=self.quantity,
                    sl=float(self.sl_level),
                    cost=self.cash_flow_ammount,
                    sl_cost=self.sl_cost,
                    slcn=self.sl_cost_nav,
                    id=self.trd_id_an))

    def get_last_price(self):

        self.db_connection = SQL(data_base=self.data_base,
                                 user_name=self.user_name,
                                 password=self.password)
        self.sec_data = self.db_connection.select_data(select_query="""select * from sec_info 
                                     where name = '{sec_name}'""".format(sec_name=self.listWidget.currentItem().text()))
        self.db_connection.close_connection()

        # Here comes later the price load of the particular security type like loading price for bond fx etc...

        self.last_price = OnlineData(list(self.sec_data["ticker"])[0]).last_eq_price()
        self.last_price = list(self.last_price["price"])[0]
        self.label_15.setText(str(self.last_price))

        self.load_chart(chart_date=self.dateEdit_2.text(),
                        Dialog=self.dialog,
                        ticker=list(self.sec_data["ticker"])[0])

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

        # Loading positions for the selected strategy
        self.db_connection = SQL(data_base=self.data_base, user_name=self.user_name, password=self.password)
        self.pos_query = self.db_connection.select_data(select_query="""select*from trade p1, sec_info p2 
                                                          where p1.sec_id = p2.sec_id 
                                                          and p1.status = 'OPEN' 
                                                          and p1.strategy_code = {strat_code}""".format(strat_code=list(self.strategy_desc["strategy_code"])[0]))
        self.db_connection.close_connection()
        self.tableWidget.setRowCount(len(self.pos_query["trade_id"]))

        for i, trd_id, name, side, quantity, price, leverage, lev_per, sl, sl_lev, dt in \
                zip(range(len(self.pos_query["trade_id"])),
                    list(self.pos_query["trade_id"]),
                    list(self.pos_query["name"]),
                    list(self.pos_query["side"]),
                    list(self.pos_query["quantity"]),
                    list(self.pos_query["trade_price"]),
                    list(self.pos_query["leverage"]),
                    list(self.pos_query["leverage_perc"]),
                    list(self.pos_query["sl"]),
                    list(self.pos_query["sl_level"]),
                    list(self.pos_query["date"])):

            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(i, 0, item)
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(i, 1, item)
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(i, 2, item)
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(i, 3, item)
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(i, 4, item)
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(i, 5, item)
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(i, 6, item)
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(i, 7, item)
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(i, 8, item)
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(i, 9, item)

            item = self.tableWidget.item(i, 0)
            item.setText(str(trd_id))
            item = self.tableWidget.item(i, 1)
            item.setText(str(name))
            item = self.tableWidget.item(i, 2)
            item.setText(str(side))
            item = self.tableWidget.item(i, 3)
            item.setText(str(quantity))
            item = self.tableWidget.item(i, 4)
            item.setText(str(price))
            item = self.tableWidget.item(i, 5)
            item.setText(str(leverage))
            item = self.tableWidget.item(i, 6)
            item.setText(str(lev_per))
            item = self.tableWidget.item(i, 7)
            item.setText(str(sl))
            item = self.tableWidget.item(i, 8)
            item.setText(str(sl_lev))
            item = self.tableWidget.item(i, 9)
            item.setText(str(dt))


class PortGroupEditor(object):

    def __init__(self, Dialog, data_base, user_name, password,):

        self.data_base = data_base
        self.user_name = user_name
        self.password = password

        self.load_port_list = SQL(data_base=self.data_base,
                                  user_name=self.user_name,
                                  password=self.password).select_data("select*from portfolios")

        self.port_groups = self.load_port_list[self.load_port_list["portfolio_group"] == "Yes"]

        Dialog.setObjectName("Dialog")
        Dialog.resize(434, 503)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.gridLayout_2 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")

        self.treeWidget = QtWidgets.QTreeWidget(Dialog)
        self.treeWidget.setAnimated(False)
        self.treeWidget.setColumnCount(1)
        self.treeWidget.setObjectName("treeWidget")

        self.gridLayout.addWidget(self.treeWidget, 0, 0, 1, 3)

        self.label_1 = QtWidgets.QLabel(Dialog)
        self.label_1.setObjectName("label_1")
        self.gridLayout.addWidget(self.label_1, 1, 0, 1, 1)

        self.comboBox = QtWidgets.QComboBox(Dialog)
        self.comboBox.setObjectName("comboBox")
        self.gridLayout.addWidget(self.comboBox, 1, 1, 1, 1)
        self.comboBox.addItems(list(self.port_groups["portfolio_name"]))

        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)

        self.port_search_line = QtWidgets.QLineEdit(Dialog)
        self.port_search_line.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.port_search_line, 2, 1, 1, 1)
        self.port_completer = QtWidgets.QCompleter(list(self.load_port_list["portfolio_name"]))
        self.port_search_line.setCompleter(self.port_completer)

        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 2, 2, 1, 1)
        self.pushButton.setText("Add")
        self.pushButton.clicked.connect(self.add_connection)

        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 1, 2, 1, 1)
        self.pushButton_2.setText("Load")
        self.pushButton_2.clicked.connect(self.load_port_group)

        self.gridLayout_2.addLayout(self.gridLayout, 2, 2, 1, 1)

        Dialog.setWindowTitle("Portfolio Group Editor")

        __sortingEnabled = self.treeWidget.isSortingEnabled()
        self.treeWidget.setSortingEnabled(False)
        self.treeWidget.setSortingEnabled(__sortingEnabled)
        self.label_1.setText("Portfolio Group")
        self.label_2.setText("Portfolio")

    def add_connection(self):

        self.load_port = SQL(data_base=self.data_base,
                             user_name=self.user_name,
                             password=self.password).select_data("""select*from portfolios 
                  where portfolio_name = '{port_name}'""".format(port_name=self.treeWidget.selectedItems()[0].text(0)))

        if list(self.load_port["portfolio_group"])[0] == "No":
            MsgBoxes().info_box(message=str(self.treeWidget.selectedItems()[0].text(0)) + " is a portfolio. " +
            "Portfolios can only be added to portfolio groups!", title="Notification")
        else:
            self.sleve_type = self.load_port_list[self.load_port_list["portfolio_name"] == self.port_search_line.text()]

            if list(self.sleve_type["portfolio_group"])[0] == "Yes":
                self.sleve_type = "p"

            else:
                self.sleve_type = "s"

            Entries(data_base=self.data_base,
                    user_name=self.user_name,
                    password=self.password).port_group(parent=self.treeWidget.selectedItems()[0].text(0),
                                                       sleve=self.port_search_line.text(),
                                                       sleve_type=self.sleve_type)

            MsgBoxes().info_box(message=str(self.port_search_line.text()) + " is added to " + str(self.treeWidget.selectedItems()[0].text(0)), title="Notification")


    def load_port_group(self):

        self.treeWidget.clear()
        self.treeWidget.headerItem().setText(0, "Portfolio Group")
        self.create_tree([self.comboBox.currentText()], [self.treeWidget])


    def create_tree(self, port_group, parent_object):

        self.parent = QtWidgets.QTreeWidgetItem(parent_object[0])
        self.treeWidget.topLevelItem(0).setText(0, port_group[0])
        round_ = 0

        while len(port_group) > 0:

            for pg, obj in zip(port_group, parent_object):

                self.port_group_list = SQL(data_base=self.data_base,
                                           user_name=self.user_name,
                                           password=self.password).select_data(select_query="""
                                           select*from portfolio_group
                                           where parent = '{port_group}'""".format(port_group=pg))

                print(self.port_group_list)

                self.parent_list = []
                self.parent_object_list = []

                for port, type, level in zip(list(self.port_group_list["sleve"]),
                                             list(self.port_group_list["sleve_type"]),
                                             range(len(list(self.port_group_list["sleve_type"])))):

                    print("port", port, " type", type, " level", level)

                    if round_ == 0:
                        obj = self.parent

                    self.item_obj = QtWidgets.QTreeWidgetItem(obj)
                    self.item_obj.setText(0, port)

                    if type == "p":
                        self.parent_list.append(port)
                        self.parent_object_list.append(self.item_obj)

            port_group = self.parent_list
            parent_object = self.parent_object_list
            round_ = + 1

            print(port_group)
            print(parent_object)
            print(len(port_group))


class MsgBoxes:

    def __init__(self):

        self.msg = None

    def info_box(self, message, title):

        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Information)
        self.msg.setText(message)
        self.msg.setWindowTitle(title)
        self.msg.setStandardButtons(QMessageBox.Ok)
        self.msg.exec_()


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = PortGroupEditor(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
