import psycopg2
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem

from database import Database
from ui.privileges import Ui_PrivilegesWindow
from utils import showError


class Privileges(QtWidgets.QMainWindow):
    """"
    Privileges window
    """

    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.mainWindow = None

        self.ui = Ui_PrivilegesWindow()
        self.ui.setupUi(self)

        # Subscribe events
        self.ui.cbTables.currentIndexChanged.connect(self.tableSelected)

        # Load tables
        self.loadTables()

    def loadTables(self):
        """
        This method is called to load table info into the combobox.
        """
        try:
            cursor = Database.connection.cursor()
            # Get scheme.tables
            cursor.execute("""SELECT table_schema || '.' || table_name AS table_name
                    FROM information_schema.tables
                    WHERE table_type = 'BASE TABLE'
                        AND table_schema NOT IN ('pg_catalog', 'information_schema');""")
            result = cursor.fetchall()

            if result:
                for table in result:
                    self.ui.cbTables.addItem(table[0])
        except (Exception, psycopg2.Error) as error:
            showError(self, "Error cargando información de tablas")

    def tableSelected(self):
        """
        This method is called when user chooses a table.
        """
        data = self.ui.cbTables.currentText().split('.')
        schema = data[0]
        table = data[1]

        self.loadTablePrivileges(schema, table)
        self.loadAttributePrivileges(schema, table)

    def loadTablePrivileges(self, schema, table):
        """"
        Loads an shows the privileges of a table
        """
        try:
            cursor = Database.connection.cursor()
            cursor.execute("""SELECT privilege_type, is_grantable
                    FROM information_schema.table_privileges
                    WHERE table_schema = '""" + schema + """' AND table_name = '""" + table + """'
                        AND grantee = '""" + Database.globalUser + """' ORDER BY privilege_type;""")
            result = cursor.fetchall()

            if result:
                self.ui.lblDelete.setText("Delete: " + result[0][1])
                self.ui.lblInsert.setText("Insert: " + result[1][1])
                self.ui.lblReferences.setText("References: " + result[2][1])
                self.ui.lblSelect.setText("Select: " + result[3][1])
                self.ui.lblTrigger.setText("Trigger: " + result[4][1])
                self.ui.lblTruncate.setText("Truncate: " + result[5][1])
                self.ui.lblUpdate.setText("Update: " + result[6][1])
            else:
                self.ui.lblDelete.setText("Delete: --")
                self.ui.lblInsert.setText("Insert: --")
                self.ui.lblReferences.setText("References: --")
                self.ui.lblSelect.setText("Select: --")
                self.ui.lblTrigger.setText("Trigger: --")
                self.ui.lblTruncate.setText("Truncate: --")
                self.ui.lblUpdate.setText("Update: --")
        except (Exception, psycopg2.Error) as error:
            showError(self, "Error cargando información de privilegos de la tabla")

    def loadAttributePrivileges(self, schema, table):
        """
        This method is called to load attributes privileges into the table.
        """
        # Clean table
        self.ui.tblAttributes.setRowCount(0)

        try:
            cursor = Database.connection.cursor()
            cursor.execute("""SELECT column_name,
                                string_agg(privilege_type || ':' || is_grantable, ','
                                        order by privilege_type) as privileges
                            FROM information_schema.column_privileges
                            WHERE table_schema = '""" + schema + """' AND table_name = '""" + table + """'
                                AND grantee = '""" + Database.globalUser + """'
                            GROUP BY column_name
                            ORDER BY column_name;""")
            result = cursor.fetchall()

            if result:
                for attributeData in result:
                    privileges = attributeData[1].split(',')
                    rowPosition = self.ui.tblAttributes.rowCount()
                    self.ui.tblAttributes.insertRow(rowPosition)

                    # Insert columns
                    self.ui.tblAttributes.setItem(rowPosition, 0, QTableWidgetItem(attributeData[0]))
                    self.ui.tblAttributes.setItem(rowPosition, 1, QTableWidgetItem(privileges[2].split(':')[1]))
                    self.ui.tblAttributes.setItem(rowPosition, 2, QTableWidgetItem(privileges[0].split(':')[1]))
                    self.ui.tblAttributes.setItem(rowPosition, 3, QTableWidgetItem(privileges[3].split(':')[1]))
                    self.ui.tblAttributes.setItem(rowPosition, 4, QTableWidgetItem(privileges[1].split(':')[1]))
        except (Exception, psycopg2.Error) as error:
            showError(self, "Error cargando los privilegios de los atributos")
