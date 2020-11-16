import json
import os
import sys

from PyQt5 import QtWidgets

from database import Database
from ui.main import Ui_MainWindow
from window.privileges import Privileges


class Main(QtWidgets.QMainWindow):
    def __init__(self, loginWindow=None, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)

        self.loginWindow = loginWindow
        self.loginWindow.hide()
        self.privilegesWindow = None
        self.signoffClose = False

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Subscribe events
        self.ui.btnShowPlan.clicked.connect(self.onShowPlanPress)
        self.ui.btnSignoff.clicked.connect(self.signoff)
        self.ui.btnShowPrivileges.clicked.connect(self.showPrivileges)

    def onShowPlanPress(self):
        """
        This method is called when user presses show plan.
        """

        # Estimado detallado
        if self.ui.cbPlan.currentIndex() == 0:
            self.showPlan(Database.connection, self.ui.txtCode.toPlainText(), "verbose true")
        # Estimado simple
        elif self.ui.cbPlan.currentIndex() == 1:
            self.showPlan(Database.connection, self.ui.txtCode.toPlainText(), "verbose false")
        # Real detallado
        elif self.ui.cbPlan.currentIndex() == 2:
            self.showPlan(Database.connection, self.ui.txtCode.toPlainText(), "analyze true")
        # Real simple
        elif self.ui.cbPlan.currentIndex() == 3:
            self.showPlan(Database.connection, self.ui.txtCode.toPlainText(), "analyze false")

    def showPlan(self, conn, text, context):
        """
        This method shows execution plan.
        """
        cursor = conn.cursor()
        cursor.execute("explain (format JSON, " + context + ")" + text)
        result = cursor.fetchone()
        file = open(r"explain.json", "wt")
        file.write(json.dumps(result[0]))
        file.close()
        os.system("python json_viewer.py explain.json")

    def signoff(self):
        if self.loginWindow is not None:
            self.loginWindow.show()
            self.signoffClose = True
        self.close()

    def showPrivileges(self):
        self.privilegesWindow = Privileges(self)
        self.privilegesWindow.show()

    def closeEvent(self, event):
        if not self.signoffClose:
            sys.exit(0)
        event.accept()
