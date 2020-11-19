import json
import os
import sys

import psycopg2
from PyQt5 import QtWidgets

from database import Database
from ui.main import Ui_MainWindow
from utils import *
from window.privileges import Privileges


class Main(QtWidgets.QMainWindow):
    """"
    Main window class.
    """

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
            self.showPlan(Database.connection, self.ui.txtCode.toPlainText(), "verbose true", False)
        # Estimado simple
        elif self.ui.cbPlan.currentIndex() == 1:
            self.showPlan(Database.connection, self.ui.txtCode.toPlainText(), "verbose false", False)
        # Real detallado
        elif self.ui.cbPlan.currentIndex() == 2:
            self.showPlan(Database.connection, self.ui.txtCode.toPlainText(), "verbose true", True)
        # Real simple
        elif self.ui.cbPlan.currentIndex() == 3:
            self.showPlan(Database.connection, self.ui.txtCode.toPlainText(), "verbose false", True)

    def showPlan(self, conn, text, context, realPlan):
        """
        This method shows execution plan.
        """
        try:
            cursor = conn.cursor()
            if realPlan:
                cursor.execute("explain (format JSON, analyze true, " + context + ")" + text)
            else:
                cursor.execute("explain (format JSON, " + context + ")" + text)
            result = cursor.fetchone()

            if "false" in context:
                cursor = conn.cursor()
                cursor.execute("explain (format JSON, " + context.replace("false", "true") + ")" + text)
                tmpResult = cursor.fetchone()
                result[0][0]["Plan"]["Indexes usage"] = \
                    self.getIndexesUsage(tmpResult[0][0]["Plan"]["Plans"][0]["Plans"])
            else:
                result[0][0]["Plan"]["Indexes usage"] = \
                    self.getIndexesUsage(result[0][0]["Plan"]["Plans"][0]["Plans"])

            file = open(r"explain.json", "wt")
            file.write(json.dumps(result[0]))
            file.close()
            os.system("python json_viewer.py explain.json")
        except (Exception, psycopg2.Error) as error:
            showError(self, "Error al obtener y guardar el plan de ejecución")

    def getIndexesUsage(self, data):
        tables = []
        indexes = []

        for plan in data:
            if "Schema" in plan and "Relation Name" in plan:
                tables.append((plan["Schema"], plan["Relation Name"]))
            if "Index Name" in plan:
                indexes.append(plan["Index Name"])

        indexesUsage = {}
        for tableIndexes in self.getTablesIndexes(tables):
            temp = {}
            for idx in tableIndexes[1].split(','):
                temp[idx] = "Used" if idx in indexes else "Not used"
            indexesUsage[tableIndexes[0]] = temp

        return indexesUsage

    def getTablesIndexes(self, tables):
        where = ""

        for table in tables:
            where += """(schemaname = '""" + table[0] + """' AND tablename = '""" + table[1] + """') OR """

        where = where[:-3]

        try:
            cursor = Database.connection.cursor()
            cursor.execute("""SELECT schemaname || '.' || tablename AS table,
                                    string_agg(indexname, ',' order by indexname) as indexes
                                FROM pg_indexes
                                WHERE """ + where + """
                                GROUP BY tablename, schemaname
                                ORDER BY tablename;""")
            result = cursor.fetchall()
            return result
        except (Exception, psycopg2.Error) as error:
            showError(self, "Error al obtener la información de indices")
            return None

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
