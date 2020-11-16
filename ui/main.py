# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt\main.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(510, 374)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 10, 471, 261))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lblCode = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.lblCode.setObjectName("lblCode")
        self.verticalLayout.addWidget(self.lblCode)
        self.txtCode = QtWidgets.QPlainTextEdit(self.verticalLayoutWidget)
        self.txtCode.setObjectName("txtCode")
        self.verticalLayout.addWidget(self.txtCode)
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(20, 280, 371, 31))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lblPlan = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.lblPlan.setMaximumSize(QtCore.QSize(90, 16777215))
        self.lblPlan.setObjectName("lblPlan")
        self.horizontalLayout.addWidget(self.lblPlan)
        self.cbPlan = QtWidgets.QComboBox(self.horizontalLayoutWidget)
        self.cbPlan.setObjectName("cbPlan")
        self.cbPlan.addItem("")
        self.cbPlan.addItem("")
        self.cbPlan.addItem("")
        self.cbPlan.addItem("")
        self.horizontalLayout.addWidget(self.cbPlan)
        self.btnShowPlan = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.btnShowPlan.setMaximumSize(QtCore.QSize(100, 16777215))
        self.btnShowPlan.setObjectName("btnShowPlan")
        self.horizontalLayout.addWidget(self.btnShowPlan)
        self.btnShowPrivileges = QtWidgets.QPushButton(self.centralwidget)
        self.btnShowPrivileges.setGeometry(QtCore.QRect(180, 330, 75, 23))
        self.btnShowPrivileges.setObjectName("btnShowPrivileges")
        self.btnSignoff = QtWidgets.QPushButton(self.centralwidget)
        self.btnSignoff.setGeometry(QtCore.QRect(260, 330, 75, 23))
        self.btnSignoff.setObjectName("btnSignoff")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Proyecto"))
        self.lblCode.setText(_translate("MainWindow", "Código a analizar"))
        self.txtCode.setPlainText(_translate("MainWindow", "--Inserte aquí su código SQL para mostrar el plan de ejecución\n"
"    --código de ejemplo:\n"
"    select * from \n"
"        optimizacion.catastro_municipal as c\n"
"        inner join\n"
"        optimizacion.patentes as p \n"
"        on st_contains(c.geom,p.geom5367)"))
        self.lblPlan.setText(_translate("MainWindow", "Plan de ejecución:"))
        self.cbPlan.setItemText(0, _translate("MainWindow", "Estimado detallado"))
        self.cbPlan.setItemText(1, _translate("MainWindow", "Estimado simple"))
        self.cbPlan.setItemText(2, _translate("MainWindow", "Real detallado"))
        self.cbPlan.setItemText(3, _translate("MainWindow", "Real simple"))
        self.btnShowPlan.setText(_translate("MainWindow", "Ver plan"))
        self.btnShowPrivileges.setText(_translate("MainWindow", "Ver privilegios"))
        self.btnSignoff.setText(_translate("MainWindow", "Cerrar sesión"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
