from FFM_SYSTEM.FFM_GUI.entries import *
from datetime import date


class MainWindow(object):

    def __init__(self):

        self.user_name = None
        self.password = None
        self.db = None
        self.login()

    def login(self):

        self.login_dialog = QtWidgets.QDialog()
        self.login_dialog.setObjectName("Dialog")
        self.login_dialog.resize(334, 170)

        self.buttonBox = QtWidgets.QDialogButtonBox(self.login_dialog)
        self.buttonBox.setGeometry(QtCore.QRect(80, 120, 171, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.env_box = QtWidgets.QComboBox(self.login_dialog)
        self.env_box.setGeometry(QtCore.QRect(170, 80, 121, 25))
        self.env_box.setObjectName("comboBox")
        self.env_box.addItems(["Developer", "Live"])

        self.user_name_label = QtWidgets.QLabel(self.login_dialog)
        self.user_name_label.setGeometry(QtCore.QRect(20, 20, 131, 21))
        self.user_name_label.setObjectName("label")

        self.password_label = QtWidgets.QLabel(self.login_dialog)
        self.password_label.setGeometry(QtCore.QRect(20, 50, 131, 21))
        self.password_label.setObjectName("label_2")

        self.environment_label = QtWidgets.QLabel(self.login_dialog)
        self.environment_label.setGeometry(QtCore.QRect(20, 80, 131, 21))
        self.environment_label.setObjectName("label_3")

        self.user_name_line = QtWidgets.QLineEdit(self.login_dialog)
        self.user_name_line.setGeometry(QtCore.QRect(170, 20, 121, 25))
        self.user_name_line.setObjectName("lineEdit")

        self.password_line = QtWidgets.QLineEdit(self.login_dialog)
        self.password_line.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_line.setGeometry(QtCore.QRect(170, 50, 121, 25))
        self.password_line.setObjectName("lineEdit_2")

        self.buttonBox.accepted.connect(self.login_accept)
        self.buttonBox.rejected.connect(self.login_reject)

        self.login_dialog.setWindowTitle("Login")
        self.user_name_label.setText("User Name")
        self.password_label.setText("Password")
        self.environment_label.setText("Environment")

        self.login_dialog.show()
        self.login_dialog.exec()

    def login_accept(self):

        self.user_name = self.user_name_line.text()
        self.password = self.password_line.text()

        if len(self.user_name) < 5:
            MsgBoxes().info_box(message="Incorrect User Name!", title="Notification")
        elif len(self.password) < 5:
            MsgBoxes().info_box(message="Incorrect Password!", title="Notification")
        else:
            if self.env_box.currentText() == "Developer":
                self.db = "dev_ffm_sys"
            elif self.env_box.currentText() == "Live":
                self.db = "ffm_sys"

            self.login_dialog.close()

        self.load_port_list = SQL(data_base=self.db,
                                  user_name=self.user_name,
                                  password=self.password).select_data("select*from portfolios")

    def login_reject(self):

        sys.exit(self)

    def start_window(self, main_window):

        self.main_window = main_window
        self.main_window.setObjectName("MainWindow")
        self.main_window.resize(800, 600)

        if self.env_box.currentText() == "Developer":
            self.main_window.setWindowTitle("Fractal Fund Manager 1.0 - " + "Developer Environment")
        elif self.env_box.currentText() == "Live":
            self.main_window.setWindowTitle("Fractal Fund Manager 1.0 - " + "Live Environment")

        self.toolBar = QtWidgets.QToolBar(self.main_window)
        self.toolBar.setObjectName("toolBar")
        self.main_window.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.main_window.insertToolBarBreak(self.toolBar)

        self.centralwidget = QtWidgets.QWidget(self.main_window)
        self.centralwidget.setObjectName("centralwidget")
        self.main_window.setCentralWidget(self.centralwidget)

        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")

        # Portfolio search bar
        self.portfolio_frame = QtWidgets.QFrame(self.centralwidget)
        self.portfolio_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.portfolio_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.portfolio_frame.setObjectName("portfolio_frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.portfolio_frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.port_tex_label = QtWidgets.QLabel(self.portfolio_frame)
        self.port_tex_label.setObjectName("port_tex_label")
        self.horizontalLayout.addWidget(self.port_tex_label)

        self.port_search_line = QtWidgets.QLineEdit(self.portfolio_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.port_search_line.sizePolicy().hasHeightForWidth())
        self.port_search_line.setSizePolicy(sizePolicy)
        self.port_search_line.setObjectName("port_search_line")
        self.horizontalLayout.addWidget(self.port_search_line)

        self.port_completer = QtWidgets.QCompleter(list(self.load_port_list["portfolio_name"]))
        self.port_search_line.setCompleter(self.port_completer)

        self.port_date_label = QtWidgets.QLabel(self.portfolio_frame)
        self.port_date_label.setObjectName("port_date_label")
        self.horizontalLayout.addWidget(self.port_date_label)
        self.port_date_edit = QtWidgets.QDateEdit(self.portfolio_frame)
        self.port_date_edit.setDate(QtCore.QDate(date.today().year, date.today().month, date.today().day))
        self.port_date_edit.setObjectName("port_date_edit")
        self.horizontalLayout.addWidget(self.port_date_edit)

        self.port_import_button = QtWidgets.QPushButton(self.portfolio_frame)
        self.port_import_button.setObjectName("port_import_button")
        self.horizontalLayout.addWidget(self.port_import_button)
        self.port_import_button.clicked.connect(self.import_portfolio_data)

        self.trade_button = QtWidgets.QPushButton(self.portfolio_frame)
        self.trade_button.setObjectName("trade_button")
        self.horizontalLayout.addWidget(self.trade_button)
        self.trade_button.setText("Trade")
        self.trade_button.clicked.connect(self.trade_entry)

        self.port_full_name_label = QtWidgets.QLabel(self.portfolio_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.port_full_name_label.sizePolicy().hasHeightForWidth())
        self.port_full_name_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("FreeSerif")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.port_full_name_label.setFont(font)
        self.port_full_name_label.setObjectName("label")
        self.horizontalLayout.addWidget(self.port_full_name_label)

        self.gridLayout_2.addWidget(self.portfolio_frame, 0, 0, 1, 1)

        # Empty frame currently
        self.frame_4 = QtWidgets.QFrame(self.centralwidget)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.gridLayout_2.addWidget(self.frame_4, 0, 1, 1, 1)

        # Portfolio Management MDI Area
        self.mdiArea_2 = QtWidgets.QMdiArea(self.centralwidget)
        self.mdiArea_2.setMinimumSize(QtCore.QSize(0, 631))
        self.mdiArea_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.mdiArea_2.setViewMode(QtWidgets.QMdiArea.SubWindowView)
        self.mdiArea_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.mdiArea_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.mdiArea_2.setObjectName("mdiArea_2")
        self.gridLayout_2.addWidget(self.mdiArea_2, 1, 0, 1, 1)

        # Second MDI Area
        self.mdiArea_3 = QtWidgets.QMdiArea(self.centralwidget)
        self.mdiArea_3.setViewMode(QtWidgets.QMdiArea.SubWindowView)
        self.mdiArea_3.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.mdiArea_3.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.mdiArea_3.setObjectName("mdiArea_3")
        self.gridLayout_2.addWidget(self.mdiArea_3, 1, 1, 1, 1)
        self.port_tex_label.setText("Portfolio")
        self.port_date_label.setText("Date")
        self.port_import_button.setText("Run")

        # Menu bar object definition
        self.menubar = QtWidgets.QMenuBar(self.main_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        self.main_window.setMenuBar(self.menubar)

# ========== Status bar object definition
        self.statusbar = QtWidgets.QStatusBar(self.main_window)
        self.statusbar.setObjectName("statusbar")
        self.main_window.setStatusBar(self.statusbar)

# ========== File
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuFile.setTitle("File")
        self.menubar.addAction(self.menuFile.menuAction())

        self.menuDatabase = QtWidgets.QMenu(self.menuFile)
        self.menuDatabase.setObjectName("menuDatabase")
        self.menuDatabase.setTitle("Database")
        self.menuFile.addAction(self.menuDatabase.menuAction())

        self.actionExport_Data = QtWidgets.QAction(self.main_window)
        self.actionExport_Data.setObjectName("actionExport_Data")
        self.actionExport_Data.setText("Export Data")
        self.menuDatabase.addAction(self.actionExport_Data)

        self.actionImport_Data = QtWidgets.QAction(self.main_window)
        self.actionImport_Data.setObjectName("actionImport_Data")
        self.actionImport_Data.setText("Import Data")
        self.menuDatabase.addAction(self.actionImport_Data)

        # Actions

# ========== Portfolio Management
        self.menuPort_Management = QtWidgets.QMenu(self.main_window)
        self.menuPort_Management.setObjectName("menuWidgets")
        self.menuPort_Management.setTitle("Portfolio Management")
        self.menubar.addAction(self.menuPort_Management.menuAction())

        self.actionCharts = QtWidgets.QMenu(self.menuPort_Management)
        self.actionCharts.setObjectName("actionCharts")
        self.actionCharts.setTitle("Charts")
        self.menuPort_Management.addAction(self.actionCharts.menuAction())

        self.actionHolding_chart = QtWidgets.QAction(self.main_window)
        self.actionHolding_chart.setObjectName("actionHolding_chart")
        self.actionHolding_chart.setText("Portfolio Holdings")
        self.actionCharts.addAction(self.actionHolding_chart)

        self.actionReturn_analysis = QtWidgets.QAction(self.main_window)
        self.actionReturn_analysis.setObjectName("actionReturn_analysis")
        self.actionReturn_analysis.setText("Return Analysis")
        self.actionCharts.addAction(self.actionReturn_analysis)

        self.actionPortfolio_Termination = QtWidgets.QAction(self.main_window)
        self.actionPortfolio_Termination.setObjectName("actionPortfolio_Termination")
        self.actionPortfolio_Termination.setText("Portfolio Termination")
        self.menuPort_Management.addAction(self.actionPortfolio_Termination)

        self.actionIntraday_Data = QtWidgets.QAction(self.main_window)
        self.actionIntraday_Data.setObjectName("actionIntraday_Data")
        self.actionIntraday_Data.setText("Intraday Data")
        self.menuPort_Management.addAction(self.actionIntraday_Data)

        # Actions

        self.actionHolding_chart.triggered.connect(self.sub_port_holding)
        self.actionReturn_analysis.triggered.connect(self.sub_port_return)

# ========== Environments
        self.menuEnvironment = QtWidgets.QMenu(self.menubar)
        self.menuEnvironment.setObjectName("menuEnvironment")
        self.menuEnvironment.setTitle("Environment")
        self.menubar.addAction(self.menuEnvironment.menuAction())

        self.actionDev = QtWidgets.QAction(self.main_window)
        self.actionDev.setObjectName("actionDev")
        self.actionDev.setText("Dev")
        self.menuEnvironment.addAction(self.actionDev)

        self.actionLive = QtWidgets.QAction(self.main_window)
        self.actionLive.setObjectName("actionLive")
        self.actionLive.setText("Live")
        self.menuEnvironment.addAction(self.actionLive)

        # Actions
        self.actionDev.triggered.connect(self.dev_env)
        self.actionLive.triggered.connect(self.live_env)

# ========== Entries
        self.menuEntry = QtWidgets.QMenu(self.menubar)
        self.menuEntry.setObjectName("menuEntry")
        self.menuEntry.setTitle("Entry")
        self.menubar.addAction(self.menuEntry.menuAction())

        self.actionPortfolio = QtWidgets.QAction(self.main_window)
        self.actionPortfolio.setObjectName("actionPortfolio")
        self.actionPortgroup = QtWidgets.QAction(self.main_window)
        self.actionPortgroup.setObjectName("actionPortgroup")
        self.actionStrategy_Model = QtWidgets.QAction(self.main_window)
        self.actionStrategy_Model.setObjectName("actionStrategy_Model")
        self.actionStrategy = QtWidgets.QAction(self.main_window)
        self.actionStrategy.setObjectName("actionStrategy")
        self.actionTrade = QtWidgets.QAction(self.main_window)
        self.actionTrade.setObjectName("actionTrade")
        self.actionCash = QtWidgets.QAction(self.main_window)
        self.actionCash.setObjectName("actionCash")
        self.actionSecurity = QtWidgets.QAction(self.main_window)
        self.actionSecurity.setObjectName("actionSecurity")
        self.menuEntry.addAction(self.actionPortfolio)
        self.menuEntry.addAction(self.actionPortgroup)
        self.menuEntry.addAction(self.actionStrategy_Model)
        self.menuEntry.addAction(self.actionStrategy)
        self.menuEntry.addAction(self.actionTrade)
        self.menuEntry.addAction(self.actionCash)
        self.menuEntry.addAction(self.actionSecurity)
        self.actionPortfolio.setText("Portfolio")
        self.actionPortgroup.setText("Portfolio Group")
        self.actionStrategy_Model.setText("Strategy Model")
        self.actionStrategy.setText("Strategy")
        self.actionTrade.setText("Trade")
        self.actionCash.setText("Cash")
        self.actionSecurity.setText("Security")

        # Actions
        self.actionPortfolio.triggered.connect(self.port_entry)
        self.actionStrategy_Model.triggered.connect(self.strat_model_entry)
        self.actionStrategy.triggered.connect(self.strat_entry)
        self.actionCash.triggered.connect(self.cash_entry)
        self.actionSecurity.triggered.connect(self.security_entry)
        self.actionPortgroup.triggered.connect(self.port_group_entry)

# ========== Data
        self.menuData = QtWidgets.QMenu(self.menubar)
        self.menuData.setObjectName("menuData")
        self.menuData.setTitle("Data")
        self.menubar.addAction(self.menuData.menuAction())

        self.menuFX = QtWidgets.QMenu(self.menuData)
        self.menuFX.setObjectName("menuFX")
        self.menuFX.setTitle("FX")
        self.menuData.addAction(self.menuFX.menuAction())

        self.menuEquity = QtWidgets.QMenu(self.menuData)
        self.menuEquity.setObjectName("menuEquity")
        self.menuEquity.setTitle("Equity")
        self.menuData.addAction(self.menuEquity.menuAction())

        self.menuReports = QtWidgets.QMenu(self.menuData)
        self.menuReports.setObjectName("menuReports")
        self.menuReports.setTitle("Reports")
        self.menuData.addAction(self.menuReports.menuAction())

        self.actionSEC_gov = QtWidgets.QAction(self.main_window)
        self.actionSEC_gov.setObjectName("actionSEC_gov")
        self.actionSEC_gov.setText("SEC.gov")
        self.menuReports.addAction(self.actionSEC_gov)

        # Actions

# ========== Process
        self.menuProcess = QtWidgets.QMenu(self.menubar)
        self.menuProcess.setObjectName("menuProcess")
        self.menuProcess.setTitle("Process")
        self.menubar.addAction(self.menuProcess.menuAction())

        self.menuCalculations = QtWidgets.QMenu(self.menuProcess)
        self.menuCalculations.setObjectName("menuCalculations")
        self.menuCalculations.setTitle("Portfolio Calculations")
        self.menuProcess.addAction(self.menuCalculations.menuAction())

        self.actionPortfolio_Positions = QtWidgets.QAction(self.main_window)
        self.actionPortfolio_Positions.setObjectName("actionPortfolio_Positions")
        self.actionPortfolio_Positions.setText("Portfolio Positions")
        self.menuCalculations.addAction(self.actionPortfolio_Positions)

        self.actionPortfolio_NAV = QtWidgets.QAction(self.main_window)
        self.actionPortfolio_NAV.setObjectName("actionPortfolio_NAV")
        self.actionPortfolio_NAV.setText("Portfolio NAV")
        self.menuCalculations.addAction(self.actionPortfolio_NAV)

        self.actionPortfolio_Holding = QtWidgets.QAction(self.main_window)
        self.actionPortfolio_Holding.setObjectName("actionPortfolio_Holding")
        self.actionPortfolio_Holding.setText("Portfolio Holdings")
        self.menuCalculations.addAction(self.actionPortfolio_Holding)

        self.actionPortfolio_Return = QtWidgets.QAction(self.main_window)
        self.actionPortfolio_Return.setObjectName("actionPortfolio_Return")
        self.actionPortfolio_Return.setText("Portfolio Returns")
        self.menuCalculations.addAction(self.actionPortfolio_Return)

        self.menuCalculations2 = QtWidgets.QMenu(self.menuProcess)
        self.menuCalculations2.setObjectName("menuCalculations2")
        self.menuCalculations2.setTitle("Security Calculations")
        self.menuProcess.addAction(self.menuCalculations2.menuAction())

        # Actions

    def sub_port_holding(self):

        self.subwindow = QtWidgets.QWidget()
        self.subwindow.setObjectName("Portfolio Holding Analysis")
        self.mdiArea_2.addSubWindow(self.subwindow)
        self.subwindow.show()

    def sub_port_return(self):

        self.subwindow = QtWidgets.QWidget()
        self.subwindow.setObjectName("Portfolio Return Analysis")
        self.mdiArea_2.addSubWindow(self.subwindow)
        self.subwindow.show()

    def import_portfolio_data(self):

        self.get_port_data = SQL(data_base=self.db,
                                 user_name=self.user_name,
                                 password=self.password).select_data("""select full_name, portfolio_type 
                                                                        from portfolios 
                                where portfolio_name = '{port_name}'""".format(port_name=self.port_search_line.text()))

        self.port_full_name_label.setText(str(self.get_port_data["full_name"][0]) +
                                          " - " + str(self.get_port_data["portfolio_type"][0]))

    def port_entry(self):

        Dialog = QtWidgets.QDialog()
        entry_window = EntryWindows(Dialog, table_entry="portfolios",
                                    data_base=self.db, user_name=self.user_name, password=self.password)
        entry_window.portfolio_entry()
        entry_window.create_button.clicked.connect(entry_window.create)
        Dialog.show()
        Dialog.exec_()

    def strat_model_entry(self):

        Dialog = QtWidgets.QDialog()
        entry_window = EntryWindows(Dialog, table_entry="strategy_modell",
                                    data_base=self.db, user_name=self.user_name, password=self.password)
        entry_window.strat_modell_entry()
        entry_window.create_button.clicked.connect(entry_window.create)
        Dialog.show()
        Dialog.exec_()

    def strat_entry(self):

        Dialog = QtWidgets.QDialog()
        entry_window = EntryWindows(Dialog, table_entry="strategy",
                                    data_base=self.db, user_name=self.user_name, password=self.password)
        entry_window.strategy_entry()
        entry_window.create_button.clicked.connect(entry_window.create)
        Dialog.show()
        Dialog.exec_()

    def cash_entry(self):

        Dialog = QtWidgets.QDialog()
        entry_window = EntryWindows(Dialog, table_entry="cash flow",
                                    data_base=self.db, user_name=self.user_name, password=self.password)
        entry_window.cash_flow()
        entry_window.create_button.clicked.connect(entry_window.create)
        Dialog.show()
        Dialog.exec_()

    def security_entry(self):

        Dialog = QtWidgets.QDialog()
        entry_window = EntryWindows(Dialog, table_entry="security",
                                    data_base=self.db, user_name=self.user_name, password=self.password)
        entry_window.security()
        entry_window.create_button.clicked.connect(entry_window.create)
        Dialog.show()
        Dialog.exec_()

    def trade_entry(self):

        if len(self.port_search_line.text()) < 1:
            MsgBoxes().info_box(message="Portfolio Name is empty !", title="Notification")
        else:

            self.get_port_data = SQL(data_base=self.db,
                                     user_name=self.user_name,
                                     password=self.password).select_data("""select * from portfolios 
                                            where portfolio_name = '{port_name}'""".format(
                                                                                port_name=self.port_search_line.text()))

            if list(self.get_port_data["portfolio_group"])[0] == "Yes":
                MsgBoxes().info_box(message="Trading activity is not allowed on portfolio groups!",
                                    title="Notification")
            else:

                self.get_strat_data = SQL(data_base=self.db,
                                          user_name=self.user_name,
                                          password=self.password).select_data(select_query="""select*from strategy 
                                                        where portfolio_code in (select portfolio_id from portfolios 
                      where portfolio_name = '{portfolio_name}')""".format(portfolio_name=self.port_search_line.text()))

                if len(list(self.get_strat_data["strategy_name"])) == 0:
                    MsgBoxes().info_box(message="Portfolio does not include any strategies! ", title="Notification")
                else:
                    Dialog = QtWidgets.QDialog()
                    trade_event = TradeEntry(Dialog, data_base=self.db,
                                       user_name=self.user_name,
                                       password=self.password,
                                       portfolio_name=self.port_search_line.text())
                    trade_event.cbox_1.currentIndexChanged.connect(trade_event.load_securities)
                    trade_event.cbox_3.currentIndexChanged.connect(trade_event.load_strat_desc)

                    Dialog.show()
                    Dialog.exec_()

    def port_group_entry(self):

        Dialog = QtWidgets.QDialog()
        port_group_window = PortGroupEditor(Dialog, data_base=self.db, user_name=self.user_name, password=self.password)
        Dialog.show()
        Dialog.exec_()

    def dev_env(self):

        self.login()
        self.main_window.setWindowTitle("Fractal Fund Manager 1.0 - " + "Developer Environment")
        MsgBoxes().info_box(message="Connected to Developer Environment", title="Notification")

    def live_env(self):

        self.login()
        self.main_window.setWindowTitle("Fractal Fund Manager 1.0 - " + "Live Environment")
        MsgBoxes().info_box(message="Connected to Live Environment", title="Notification")


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

    import sys
    app = QtWidgets.QApplication(sys.argv)
    Window = QtWidgets.QMainWindow()
    gui = MainWindow()
    gui.start_window(Window)
    Window.show()
    sys.exit(app.exec_())

