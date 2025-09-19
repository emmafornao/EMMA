from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1024, 640)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(parent=self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(5, 5, 999, 534))
        self.tabWidget.setObjectName("tabWidget")
        self.tab_installed = QtWidgets.QWidget()
        self.tab_installed.setObjectName("tab_installed")
        self.tableView_installed = QtWidgets.QTableView(parent=self.tab_installed)
        self.tableView_installed.setGeometry(QtCore.QRect(0, 0, 999, 534))
        self.tableView_installed.setObjectName("tableView_installed")
        self.tableView_installed.installEventFilter(self)
        self.tabWidget.addTab(self.tab_installed, "")
        self.tab_favourites = QtWidgets.QWidget()
        self.tab_favourites.setObjectName("tab_favourites")
        self.tableView_favourites = QtWidgets.QTableView(parent=self.tab_favourites)
        self.tableView_favourites.setGeometry(QtCore.QRect(0, 0, 999, 534))
        self.tableView_favourites.setObjectName("tableView_favourites")
        self.tableView_favourites.installEventFilter(self)
        self.tabWidget.addTab(self.tab_favourites, "")
        self.pushButton_removeMods = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton_removeMods.setGeometry(QtCore.QRect(20, 549, 100, 25))
        self.pushButton_removeMods.setObjectName("pushButton_removeMods")
        self.pushButton_reinstallMods = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton_reinstallMods.setGeometry(QtCore.QRect(130, 549, 100, 25))
        self.pushButton_reinstallMods.setObjectName("pushButton_reinstallMods")
        self.pushButton_clearDynamicDownloads = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton_clearDynamicDownloads.setGeometry(QtCore.QRect(240, 549, 180, 25))
        self.pushButton_clearDynamicDownloads.setObjectName("pushButton_clearDynamicDownloads")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 20))
        self.file_menu = self.menubar.addMenu("File")
        self.file_menu.addAction("Select Ark Folder...")
        self.file_menu.addAction("Settings")
        self.file_menu.addAction("About")
        MainWindow.setMenuBar(self.menubar)
        """ self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar) """

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "EMMA (Emma's Mod Manager for Ark: Survival Ascended)"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_installed), _translate("MainWindow", "Installed"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_favourites), _translate("MainWindow", "Favourites"))
        self.pushButton_removeMods.setText(_translate("MainWindow", "Remove Mods"))
        self.pushButton_reinstallMods.setText(_translate("MainWindow", "Reinstall Mods"))
        # self.pushButton_ToggleFavourite.setText(_translate("MainWindow", "Toggle Favourite"))
        self.pushButton_clearDynamicDownloads.setText(_translate("MainWindow", "Clear Dynamic Downloads"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
