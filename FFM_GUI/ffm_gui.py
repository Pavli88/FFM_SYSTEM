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
        self.env_box.addItems(["Demo", "Developer", "Live"])

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
            else:
                self.db = "demo"

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
        else:
            self.main_window.setWindowTitle("Fractal Fund Manager 1.0 - " + "Demo Environment")

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
        self.mdiArea_2.setObjectName("mdiArea_2")
        self.gridLayout_2.addWidget(self.mdiArea_2, 1, 0, 1, 1)

        # Second MDI Area
        self.mdiArea_3 = QtWidgets.QMdiArea(self.centralwidget)
        self.mdiArea_3.setViewMode(QtWidgets.QMdiArea.SubWindowView)
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

        # Status bar object definition
        self.statusbar = QtWidgets.QStatusBar(self.main_window)
        self.statusbar.setObjectName("statusbar")
        self.main_window.setStatusBar(self.statusbar)

        # File
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuFile.setTitle("File")

        # Environments
        self.menuEnvironment = QtWidgets.QMenu(self.menubar)
        self.menuEnvironment.setObjectName("menuEnvironment")
        self.actionDev = QtWidgets.QAction(self.main_window)
        self.actionDev.setObjectName("actionDev")
        self.actionLive = QtWidgets.QAction(self.main_window)
        self.actionLive.setObjectName("actionLive")
        self.actionDemo = QtWidgets.QAction(self.main_window)
        self.actionDemo.setObjectName("actionDemo")
        self.menuEnvironment.addAction(self.actionDemo)
        self.menuEnvironment.addAction(self.actionDev)
        self.menuEnvironment.addAction(self.actionLive)
        self.menuEnvironment.setTitle("Environment")
        self.actionDev.setText("Dev")
        self.actionLive.setText("Live")
        self.actionDemo.setText("Demo")
        self.actionDev.triggered.connect(self.dev_env)
        self.actionLive.triggered.connect(self.live_env)
        self.actionDemo.triggered.connect(self.demo_env)

        # Entries
        self.menuEntry = QtWidgets.QMenu(self.menubar)
        self.menuEntry.setObjectName("menuEntry")
        self.actionPortfolio = QtWidgets.QAction(self.main_window)
        self.actionPortfolio.setObjectName("actionPortfolio")
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
        self.menuEntry.addAction(self.actionStrategy_Model)
        self.menuEntry.addAction(self.actionStrategy)
        self.menuEntry.addAction(self.actionTrade)
        self.menuEntry.addAction(self.actionCash)
        self.menuEntry.addAction(self.actionSecurity)
        self.menuEntry.setTitle("Entry")
        self.actionPortfolio.setText("Portfolio")
        self.actionStrategy_Model.setText("Strategy Model")
        self.actionStrategy.setText("Strategy")
        self.actionTrade.setText("Trade")
        self.actionCash.setText("Cash")
        self.actionSecurity.setText("Security")

        # Portfolio Management
        self.menuPort_Management = QtWidgets.QMenu(self.main_window)
        self.menuPort_Management.setObjectName("menuWidgets")
        self.actionIntraday_Data = QtWidgets.QAction(self.main_window)
        self.actionIntraday_Data.setObjectName("actionIntraday_Data")
        self.menuPort_Management.addAction(self.actionIntraday_Data)
        self.menubar.addAction(self.menuPort_Management.menuAction())
        self.menuPort_Management.setTitle("Portfolio Management")

        self.actionIntraday_Data.setText("Intraday Data")

        # Entry actions
        self.actionPortfolio.triggered.connect(self.port_entry)
        self.actionStrategy_Model.triggered.connect(self.strat_model_entry)
        self.actionStrategy.triggered.connect(self.strat_entry)
        self.actionCash.triggered.connect(self.sub)

        # Menu bar elements adding action
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEnvironment.menuAction())
        self.menubar.addAction(self.menuEntry.menuAction())

    def sub(self):

        self.subwindow = QtWidgets.QWidget()
        self.subwindow.setObjectName("subwindow")
        self.mdiArea.addSubWindow(self.subwindow)
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

    def dev_env(self):

        self.login()
        self.main_window.setWindowTitle("Fractal Fund Manager 1.0 - " + "Developer Environment")
        MsgBoxes().info_box(message="Connected to Developer Environment", title="Notification")

    def live_env(self):

        self.login()
        self.main_window.setWindowTitle("Fractal Fund Manager 1.0 - " + "Live Environment")
        MsgBoxes().info_box(message="Connected to Live Environment", title="Notification")

    def demo_env(self):

        self.login()
        self.main_window.setWindowTitle("Fractal Fund Manager 1.0 - " + "Demo Environment")
        MsgBoxes().info_box(message="Connected to Demo Environment", title="Notification")


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

