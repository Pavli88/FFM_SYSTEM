from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import sys
from FFM_SYSTEM.ffm_data import *


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
        self.port_type_cbox.addItems(["TEST", "TRADE", "INVESTMENT", "SAVING"])

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
        self.dateEdit.setDate(QtCore.QDate(2019, 1, 1))
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
        self.dateEdit.setDate(QtCore.QDate(2019, 1, 1))
        self.dateEdit.setObjectName("dateEdit")

        self.label_1.setText("Strategy Name")
        self.label_2.setText("Strategy Descreption")
        self.create_button.setText("Create")
        self.label_3.setText("Strategy Model")
        self.label_4.setText("Portfolio Code")
        self.label_5.setText("Start Date")

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
    ui.strategy_entry()
    MainWindow.show()

    sys.exit(app.exec_())
