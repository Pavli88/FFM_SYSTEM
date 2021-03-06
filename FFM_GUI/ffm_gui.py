from FFM_SYSTEM.FFM_GUI.entries import *
from FFM_SYSTEM.ffm_risk_metrics import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from datetime import date
import time
from datetime import timedelta


class MainWindow(object):

    def __init__(self):

        self.user_name = None
        self.password = None
        self.db = None
        self.login()

        self.begtime = time.strftime("%H:%M:%S")
        self.today = date.today()

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

        self.db_connection = SQL(data_base=self.db,
                                  user_name=self.user_name,
                                  password=self.password)

        self.load_port_list = self.db_connection.select_data("select*from portfolios")

        # Path variables

        self.load_settings = self.db_connection.select_data("select*from settings where id = 1")

        self.icon_path = str(self.load_settings["main_folder"][0]) + "/FFM_GUI/Icons/"

        print(self.icon_path)

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

        # Toolbar

        self.toolBar = QtWidgets.QToolBar(self.main_window)
        self.toolBar.setObjectName("toolBar")
        self.main_window.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.main_window.insertToolBarBreak(self.toolBar)

        testAction = QAction(QIcon(self.icon_path + 'graph.png'), 'Flee the Scene', self.toolBar)
        #extractAction.triggered.connect(self.close_application)

        #self.toolBar = self.addToolBar("Extraction")
        self.toolBar.addAction(testAction)

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

        self.port_date_label_2 = QtWidgets.QLabel(self.portfolio_frame)
        self.port_date_label_2.setObjectName("port_date_label_2")
        self.gridLayout_2.addWidget(self.port_date_label_2, 0, 2, 1, 1)
        self.horizontalLayout.addWidget(self.port_date_label_2)
        self.port_date_label_2.setText("Start Date")

        self.port_date_edit_2 = QtWidgets.QDateEdit(self.portfolio_frame)
        self.port_date_edit_2.setDate(QtCore.QDate(self.portdate.year, self.portdate.month, self.portdate.day))
        self.port_date_edit_2.setObjectName("port_date_edit_2")
        self.gridLayout_2.addWidget(self.port_date_edit_2, 0, 3, 1, 1)
        self.horizontalLayout.addWidget(self.port_date_edit_2)

        self.port_date_label = QtWidgets.QLabel(self.portfolio_frame)
        self.port_date_label.setObjectName("port_date_label")
        self.gridLayout_2.addWidget(self.port_date_label, 0, 4, 1, 1)
        self.horizontalLayout.addWidget(self.port_date_label)

        self.port_date_edit = QtWidgets.QDateEdit(self.portfolio_frame)
        self.port_date_edit.setDate(QtCore.QDate(self.portdate.year, self.portdate.month, self.portdate.day))
        self.port_date_edit.setObjectName("port_date_edit")
        self.gridLayout_2.addWidget(self.port_date_edit, 0, 5, 1, 1)
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
        font.setFamily("Ubuntu")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.port_full_name_label.setFont(font)
        self.port_full_name_label.setObjectName("label")
        self.horizontalLayout.addWidget(self.port_full_name_label)

        self.gridLayout_2.addWidget(self.portfolio_frame, 0, 0, 1, 1)

        # Portfolio Management MDI Area
        self.mdiArea_2 = QtWidgets.QMdiArea(self.centralwidget)
        self.mdiArea_2.setMinimumSize(QtCore.QSize(0, 631))
        self.mdiArea_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.mdiArea_2.setViewMode(QtWidgets.QMdiArea.SubWindowView)
        self.mdiArea_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.mdiArea_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.mdiArea_2.setObjectName("mdiArea_2")
        self.gridLayout_2.addWidget(self.mdiArea_2, 1, 0, 1, 1)

        self.port_tex_label.setText("Portfolio")
        self.port_date_label.setText("End Date")
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
        self.statusbar.showMessage("This is a status bar")

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

        self.actionSettings = QtWidgets.QAction(self.menuFile)
        self.actionSettings.setObjectName("actionSettings")
        self.actionSettings.setText("Settings")
        self.menuFile.addAction(self.actionSettings)

        # Actions
        self.actionSettings.triggered.connect(self.settings_window)

# ========== Portfolio Management
        self.menuPort_Management = QtWidgets.QMenu(self.main_window)
        self.menuPort_Management.setObjectName("menuWidgets")
        self.menuPort_Management.setTitle("Portfolio Management")
        self.menubar.addAction(self.menuPort_Management.menuAction())

        self.actionCharts = QtWidgets.QMenu(self.menuPort_Management)
        self.actionCharts.setObjectName("actionCharts")
        self.actionCharts.setTitle("Charts")
        self.menuPort_Management.addAction(self.actionCharts.menuAction())

        self.actionChart = QtWidgets.QAction(self.main_window)
        self.actionChart.setObjectName("actionChart")
        self.actionChart.setText("Portfolio Chart")
        self.actionCharts.addAction(self.actionChart)

        self.actionCash_Flow = QtWidgets.QAction(self.main_window)
        self.actionCash_Flow.setObjectName("actionCash_Flow")
        self.actionCash_Flow.setText("Portfolio Cash Flow")
        self.actionCharts.addAction(self.actionCash_Flow)

        self.actionNAV_chart = QtWidgets.QAction(self.main_window)
        self.actionNAV_chart.setObjectName("actionNAV_chart")
        self.actionNAV_chart.setText("Portfolio NAV")
        self.actionCharts.addAction(self.actionNAV_chart)

        self.actionAUMDD_chart = QtWidgets.QAction(self.main_window)
        self.actionAUMDD_chart.setObjectName("actionAUMDD_chart")
        self.actionAUMDD_chart.setText("Portfolio AUM Drawdown")
        self.actionCharts.addAction(self.actionAUMDD_chart)

        self.actionDD_chart = QtWidgets.QAction(self.main_window)
        self.actionDD_chart.setObjectName("actionDD_chart")
        self.actionDD_chart.setText("Portfolio NAV Drawdown")
        self.actionCharts.addAction(self.actionDD_chart)

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

        self.actionChart.triggered.connect(self.sub_port_chart)
        self.actionCash_Flow.triggered.connect(self.sub_port_chf)
        self.actionNAV_chart.triggered.connect(self.sub_port_nav)
        self.actionDD_chart.triggered.connect(self.sub_port_dd)
        self.actionAUMDD_chart.triggered.connect(self.sub_port_aum_dd)
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

        self.actionPortfolio = QtWidgets.QAction(QIcon(self.icon_path + 'pie-chart.png'), "Portfolio", self.main_window)
        self.actionPortfolio.setObjectName("actionPortfolio")
        self.actionPortgroup = QtWidgets.QAction(QIcon(self.icon_path + 'tree-structure.png'), "Portfolio Group", self.main_window)
        self.actionPortgroup.setObjectName("actionPortgroup")
        self.actionStrategy_Model = QtWidgets.QAction(QIcon(self.icon_path + 'strat-mod.png'), "Strategy Model",self.main_window)
        self.actionStrategy_Model.setObjectName("actionStrategy_Model")
        self.actionStrategy = QtWidgets.QAction(QIcon(self.icon_path + 'chess.png'), "Strategy",self.main_window)
        self.actionStrategy.setObjectName("actionStrategy")
        self.actionCash = QtWidgets.QAction(QIcon(self.icon_path + 'money.png'), "Cash", self.main_window)
        self.actionCash.setObjectName("actionCash")
        self.actionSecurity = QtWidgets.QAction(QIcon(self.icon_path + 'certificate.png'), "Security", self.main_window)
        self.actionSecurity.setObjectName("actionSecurity")
        self.actionSecurityMap = QtWidgets.QAction("Security Mapping", self.main_window)
        self.actionSecurityMap.setObjectName("actionSecurity")
        self.menuEntry.addAction(self.actionPortfolio)
        self.menuEntry.addAction(self.actionPortgroup)
        self.menuEntry.addAction(self.actionStrategy_Model)
        self.menuEntry.addAction(self.actionStrategy)
        self.menuEntry.addAction(self.actionCash)
        self.menuEntry.addAction(self.actionSecurity)
        self.menuEntry.addAction(self.actionSecurityMap)
        self.actionPortfolio.setText("Portfolio")
        self.actionPortgroup.setText("Portfolio Group")
        self.actionStrategy_Model.setText("Strategy Model")
        self.actionStrategy.setText("Strategy")
        self.actionCash.setText("Cash")
        self.actionSecurity.setText("Security")
        self.actionSecurityMap.setText("Security Mapping")

        # Actions
        self.actionPortfolio.triggered.connect(self.port_entry)
        self.actionStrategy_Model.triggered.connect(self.strat_model_entry)
        self.actionStrategy.triggered.connect(self.strat_entry)
        self.actionCash.triggered.connect(self.cash_entry)
        self.actionSecurity.triggered.connect(self.security_entry)
        self.actionPortgroup.triggered.connect(self.port_group_entry)
        self.actionSecurityMap.triggered.connect(self.security_mapping)

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

        self.actionProcess_Manager = QtWidgets.QAction(self.main_window)
        self.actionProcess_Manager.setObjectName("actionProcess_Manager")
        self.actionProcess_Manager.setText("Process Manager")
        self.menuCalculations.addAction(self.actionProcess_Manager)

        self.menuCalculations2 = QtWidgets.QMenu(self.menuProcess)
        self.menuCalculations2.setObjectName("menuCalculations2")
        self.menuCalculations2.setTitle("Security Calculations")
        self.menuProcess.addAction(self.menuCalculations2.menuAction())

        # Actions
        self.actionProcess_Manager.triggered.connect(self.port_hold_calc)

    def port_hold_calc(self):

        Dialog = QtWidgets.QDialog()
        proc_man = ProcessManager(dialog=Dialog,
                                  data_base=self.db,
                                  user_name=self.user_name,
                                  password=self.password)

        proc_man.portfolio_holding_calculator()
        proc_man.pushButton.clicked.connect(proc_man.calc_holding)
        Dialog.show()
        Dialog.exec_()

    def sub_port_chart(self):

        self.subwindow = QtWidgets.QWidget()
        self.subwindow.setObjectName("Portfolio_NAV_Analysis")
        self.subwindow.setWindowTitle("Portfolio NAV History")
        self.subwindow.setMinimumSize(QtCore.QSize(600, 300))
        self.mdiArea_2.addSubWindow(self.subwindow)

        self.dpi = 100
        self.fig = Figure((10.0, 5.0), dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.subwindow)

        self.ax = self.fig.add_subplot(111)

        x = StockData(stock_list=['AAPL'], start_date=date(year=2019, month=3, day=20)).stock_data_frame()
        print(x)

        opens = np.asarray(x['Open'])  #
        lows = np.asarray(x['Low'])  #
        highs = np.asarray(x['High'])  #
        closes = np.asarray(x['Close'])  #
        candlestick2_ohlc(self.ax, opens, highs, lows, closes, width=0.6, colorup='green', colordown='r')

        # Layout with box sizers

        hbox = QHBoxLayout()
        vbox = QVBoxLayout()
        vbox.addWidget(self.canvas)
        vbox.addLayout(hbox)

        self.subwindow.setLayout(vbox)
        self.subwindow.show()

    def sub_port_chf(self):

        self.chf = SQL(data_base=self.db,
                       user_name=self.user_name,
                       password=self.password).select_data(select_query="""select*from cash_flow cf, portfolios p 
                                                                           where p.portfolio_id = cf.portfolio_code 
                                                                           and p.portfolio_name = '{port}' 
                                                                           and cf.date between '{start_date}'
                                                                           and '{end_date}'""".format(
            port=self.port_search_line.text(),
            start_date=self.port_date_edit_2.text().replace(". ", ""),
            end_date=self.port_date_edit.text().replace(". ", "")))

        self.cf_bal = SQL(data_base=self.db,
                       user_name=self.user_name,
                       password=self.password).select_data(select_query="""select pn.cash_balance
                                                                           from portfolio_nav pn, portfolios p
                                                                           where pn.portfolio_code = p.portfolio_id 
                                                                           and p.portfolio_name = '{port}' 
                                                                           and pn.date between '{start_date}' 
                                                                           and '{end_date}'""".format(
                                                                                    port=self.port_search_line.text(),
                                                            start_date=self.port_date_edit_2.text().replace(". ", ""),
                                                            end_date=self.port_date_edit.text().replace(". ", "")))

        self.start_date = self.port_date_edit_2.text().replace(". ", "").replace(".", "")
        self.end_date = self.port_date_edit.text().replace(". ", "").replace(".", "")

        self.start_date = date(year=int(self.start_date[0:4]),
                               month=int(self.start_date[4:6]),
                               day=int(self.start_date[6:]))

        self.end_date = date(year=int(self.end_date[0:4]),
                             month=int(self.end_date[4:6]),
                             day=int(self.end_date[6:]))

        self.cf_list = []

        while self.start_date <= self.end_date:
            self.chf_frame = self.chf[self.chf["date"] == self.start_date]
            self.net_chf = sum(list(self.chf_frame["ammount"]))
            print(self.net_chf, self.start_date)
            self.cf_list.append(self.net_chf)
            self.start_date = self.start_date + BDay(1)
            self.start_date = self.start_date.date()

        self.subwindow = QtWidgets.QWidget()
        self.subwindow.setObjectName("Portfolio_CF_Analysis")
        self.subwindow.setWindowTitle("Portfolio Cash Flow History")
        self.subwindow.setMinimumSize(QtCore.QSize(600, 300))
        self.mdiArea_2.addSubWindow(self.subwindow)

        self.dpi = 100
        self.fig = Figure((10.0, 5.0), dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.subwindow)

        self.ax = self.fig.add_subplot(111)
        self.ax.bar(np.arange(len(self.cf_list)), self.cf_list)
        self.ax.axhline(y=0, color='black')
        self.ax.plot(list(self.cf_bal["cash_balance"]), color='red')

        self.ax.legend(['Net Cash Flow'])

        # Layout with box sizers

        hbox = QHBoxLayout()
        vbox = QVBoxLayout()
        vbox.addWidget(self.canvas)
        vbox.addLayout(hbox)

        self.subwindow.setLayout(vbox)
        self.subwindow.show()

    def sub_port_nav(self):

        self.get_port_data = SQL(data_base=self.db,
                                 user_name=self.user_name,
                                 password=self.password).select_data("""select*from portfolio_nav pn, portfolios p 
                                                                                    where pn.portfolio_code = p.portfolio_id 
                                                                                    and p.portfolio_name = '{port_name}' 
                                                                                    and pn.date between '{start_date}' 
                                                                                    and'{end_date}'""".format(
            port_name=self.port_search_line.text(),
            start_date=self.port_date_edit_2.text().replace(". ", ""),
            end_date=self.port_date_edit.text().replace(". ", "")))

        print(self.get_port_data)

        self.subwindow = QtWidgets.QWidget()
        self.subwindow.setObjectName("Portfolio_NAV_Analysis")
        self.subwindow.setWindowTitle("Portfolio NAV History")
        self.subwindow.setMinimumSize(QtCore.QSize(600, 300))
        self.mdiArea_2.addSubWindow(self.subwindow)

        self.dpi = 100
        self.fig = Figure((10.0, 5.0), dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.subwindow)

        self.ax = self.fig.add_subplot(111)
        self.ax.plot(self.get_port_data["total_nav"])
        self.ax.plot(self.get_port_data["aum"])
        self.get_port_data["port_lev_perc"].plot(ax=self.ax, style='--', secondary_y=True)
        self.ax.legend(['NAV', 'AUM', 'LEV %'])

        # Layout with box sizers

        hbox = QHBoxLayout()
        vbox = QVBoxLayout()
        vbox.addWidget(self.canvas)
        vbox.addLayout(hbox)

        self.subwindow.setLayout(vbox)
        self.subwindow.show()

    def sub_port_dd(self):

        self.get_port_data = SQL(data_base=self.db,
                                 user_name=self.user_name,
                                 password=self.password).select_data("""select*from portfolio_nav pn, portfolios p 
                                                                                            where pn.portfolio_code = p.portfolio_id 
                                                                                            and p.portfolio_name = '{port_name}' 
                                                                                            and pn.date between '{start_date}' 
                                                                                            and'{end_date}'""".format(
            port_name=self.port_search_line.text(),
            start_date=self.port_date_edit_2.text().replace(". ", ""),
            end_date=self.port_date_edit.text().replace(". ", "")))

        print(self.get_port_data)

        self.subwindow = QtWidgets.QWidget()
        self.subwindow.setObjectName("Portfolio_NAVDD_Analysis")
        self.subwindow.setWindowTitle("Portfolio NAV Drawdown History")
        self.subwindow.setMinimumSize(QtCore.QSize(600, 300))
        self.mdiArea_2.addSubWindow(self.subwindow)

        self.dpi = 100
        self.fig = Figure((10.0, 5.0), dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.subwindow)

        self.ax = self.fig.add_subplot(111)
        self.ax.plot(self.get_port_data["nav_dd"])
        self.ax.legend(['NAV Drawdown'])

        # Layout with box sizers

        hbox = QHBoxLayout()
        vbox = QVBoxLayout()
        vbox.addWidget(self.canvas)
        vbox.addLayout(hbox)

        self.subwindow.setLayout(vbox)
        self.subwindow.show()

    def sub_port_aum_dd(self):

        self.get_port_data = SQL(data_base=self.db,
                                 user_name=self.user_name,
                                 password=self.password).select_data("""select*from portfolio_nav pn, portfolios p 
                                                                                            where pn.portfolio_code = p.portfolio_id 
                                                                                            and p.portfolio_name = '{port_name}' 
                                                                                            and pn.date between '{start_date}' 
                                                                                            and'{end_date}'""".format(
            port_name=self.port_search_line.text(),
            start_date=self.port_date_edit_2.text().replace(". ", ""),
            end_date=self.port_date_edit.text().replace(". ", "")))

        print(self.get_port_data)

        self.subwindow = QtWidgets.QWidget()
        self.subwindow.setObjectName("Portfolio_AUMDD_Analysis")
        self.subwindow.setWindowTitle("Portfolio AUM Drawdown History")
        self.subwindow.setMinimumSize(QtCore.QSize(600, 300))
        self.mdiArea_2.addSubWindow(self.subwindow)

        self.dpi = 100
        self.fig = Figure((10.0, 5.0), dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.subwindow)

        self.ax = self.fig.add_subplot(111)
        self.ax.plot(self.get_port_data["aum_dd"])
        self.ax.legend(['AUM Drawdown'])

        # Layout with box sizers

        hbox = QHBoxLayout()
        vbox = QVBoxLayout()
        vbox.addWidget(self.canvas)
        vbox.addLayout(hbox)

        self.subwindow.setLayout(vbox)
        self.subwindow.show()

    def sub_port_return(self):

        self.subwindow = QtWidgets.QWidget()
        self.subwindow.setObjectName("Portfolio Return Analysis")
        self.subwindow.setWindowTitle("Portfolio Return Analysis")
        self.subwindow.setMinimumSize(QtCore.QSize(600, 300))
        self.mdiArea_2.addSubWindow(self.subwindow)

        self.dpi = 100
        self.fig = Figure((10.0, 5.0), dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.subwindow)

        self.ax = self.fig.add_subplot(111)

        # Layout with box sizers

        hbox = QHBoxLayout()
        vbox = QVBoxLayout()
        vbox.addWidget(self.canvas)
        vbox.addLayout(hbox)

        self.subwindow.setLayout(vbox)
        self.subwindow.show()

    def import_portfolio_data(self):

        if len(self.port_search_line.text()) == 0:
            MsgBoxes().info_box(message="Portfolio is not selected!", title="Notification")
        else:
            self.get_port_data = SQL(data_base=self.db,
                                     user_name=self.user_name,
                                     password=self.password).select_data("""select*from portfolio_nav pn, portfolios p 
                                                                            where pn.portfolio_code = p.portfolio_id 
                                                                            and p.portfolio_name = '{port_name}' 
                                                                            and pn.date = '{date}'""".format(
                                                                                port_name=self.port_search_line.text(),
                                                                                date=self.port_date_edit.text().replace(". ", "")))

            if len(list(self.get_port_data["portfolio_code"])) == 0:
                MsgBoxes().info_box(message="Portfolio Holding data was not yet calculated!", title="Notification")
            else:
                print(self.get_port_data)

                # Portfolio Var calculation, running with VAR95 parameter

                if (list(self.get_port_data["portfolio_type"])[0] == "TRADE") or \
                        (list(self.get_port_data["portfolio_type"])[0] == "INVESTMENT"):

                    self.nav_dd = list(self.get_port_data["nav_dd"])[0]
                    self.aum_dd = list(self.get_port_data["aum_dd"])[0]

                    self.port_full_name_label.setText(str(self.get_port_data["full_name"][0]) +
                                                      " - " + str(self.get_port_data["portfolio_type"][0]) +
                                                      "   VAR 95%: "+ str(round(list(self.get_port_data["d_var_95_p"])[0]*100, 2)) + "%" +
                                                      "   NAV Drawdown: " + str(self.nav_dd) + " %   AUM Drawdown: " +
                                                      str(self.aum_dd) + " %")

                    # Widget update

    def settings_window(self):

        Dialog = QtWidgets.QDialog()

        entry_window = EntryWindows(Dialog, table_entry="settings",
                                    data_base=self.db, user_name=self.user_name, password=self.password)

        entry_window.settings()
        entry_window.create_button.clicked.connect(entry_window.create)

        Dialog.show()
        Dialog.exec_()

    def port_entry(self):

        Dialog = QtWidgets.QDialog()
        entry_window = EntryWindows(Dialog, table_entry="portfolios",
                                    data_base=self.db, user_name=self.user_name, password=self.password)
        entry_window.portfolio_entry()

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

    def security_mapping(self):

        Dialog = QtWidgets.QDialog()
        entry_window = EntryWindows(Dialog, table_entry="security map",
                                    data_base=self.db, user_name=self.user_name, password=self.password)
        entry_window.security_map()
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
            self.cash_flow_check = SQL(data_base=self.db,
                                     user_name=self.user_name,
                                     password=self.password).select_data("""select*from cash_flow 
                                                                            where portfolio_code = {port_code} 
                                                                            and cash_flow_type = 'FUNDING'""".format(
                                                                       port_code=self.get_port_data["portfolio_id"][0]))

            if list(self.get_port_data["portfolio_group"])[0] == "Yes":
                MsgBoxes().info_box(message="Trading activity is not allowed on portfolio groups!",
                                    title="Notification")
            elif len(self.cash_flow_check["cash_id"]) == 0:
                MsgBoxes().info_box(message="Portfolio is not funded. Please place the initial funding!",
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

