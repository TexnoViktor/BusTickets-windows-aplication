from PyQt6.QtSql import *
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QDialog
from PyQt6 import QtWidgets

db_name = 'db/data.db'

db = QSqlDatabase.addDatabase("QSQLITE")
db.setDatabaseName(db_name)
ok = db.open()
buses = QSqlTableModel()
buses.setTable('routes')
buses.select()


class FirstWindow(QDialog):
    def __init__(self):
        super(FirstWindow, self).__init__()
        uic.loadUi('ui/start.ui', self)
        self.


    def go_to_delete(self):
        deleteWindow = DeleteWindow()
        widget.addWidget(deleteWindow)
        widget.setCurrentWidget(widget.currentIndex()+1)


class DeleteWindow(QDialog):
    def __init__(self):
        super(DeleteWindow, self).__init__()
        uic.loadUi('ui/delete.ui', self)
    #     self.backButton.clicked.connect(self.go_to_back())
    #
    # def go_to_back(self):
    #     firstWindow = FirstWindow()
    #     widget.addWidget(firstWindow)
    #     widget.setCurrentWidget(widget.currentIndex() + 1)


app = QApplication([])
widget = QtWidgets.QStackedWidget()
firstWindow = FirstWindow()
deleteWindow = DeleteWindow()
widget.addWidget(firstWindow)
widget.addWidget(deleteWindow)
widget.show()
app.exec()
