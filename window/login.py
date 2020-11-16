from PyQt5 import QtWidgets

from ui.login import Ui_LoginWindow
from database import Database
from utils import *
from window.main import Main


class Login(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.mainWindow = None

        self.ui = Ui_LoginWindow()
        self.ui.setupUi(self)

        # Subscribe events
        self.ui.btnLogin.clicked.connect(self.login)
        self.ui.btnCancel.clicked.connect(self.close)
        # Detects if user presses ENTER inside password field
        self.ui.txtPassword.returnPressed.connect(self.login)

    def login(self):
        """
        This method is called when user presses login button.
        """
        user = self.ui.txtUser.text()
        password = self.ui.txtPassword.text()
        host = self.ui.txtServer.text()
        port = self.ui.txtPort.text()
        database = self.ui.txtDb.text()

        connection = Database.createConnection(user, password, host, port, database)
        if connection is not None:
            self.mainWindow = Main(self)
            self.mainWindow.show()
        else:
            showError(self, "Error de conexión")

    def register(self):
        """
        Method called when user presses cancel button. Closes login window
        """
        self.close()
