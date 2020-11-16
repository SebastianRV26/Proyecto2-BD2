import sys

from PyQt5 import QtWidgets

from window.login import Login

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    loginWindow = Login()
    loginWindow.show()
    sys.exit(app.exec_())
