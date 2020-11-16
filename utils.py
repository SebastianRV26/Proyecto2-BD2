from PyQt5.QtWidgets import QMessageBox

def showError(window, message):
    errorMsg = QMessageBox(window)
    errorMsg.setIcon(QMessageBox.Critical)
    errorMsg.setText(message)
    errorMsg.setWindowTitle("Error")
    errorMsg.show()


def showInfo(window, message):
    infoMsg = QMessageBox(window)
    infoMsg.setIcon(QMessageBox.Information)
    infoMsg.setText(message)
    infoMsg.setWindowTitle("Information")
    infoMsg.show()