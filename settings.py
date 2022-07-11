import sys
import os
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic
import qdarkstyle
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
os.environ['QT_MAC_WANTS_LAYER'] = '1'
# from configparser import ConfigParser
# config = ConfigParser()
# conf_path = 'config.ini'
# config.read(conf_path)
#
#
# path_k_exp = config.get('main', 'k_exp_path')
# path_db = config.get('main', 'path_db')
# dark_mode = config.get('main', 'dark_mode')

# path = os.path.dirname(__file__) #uic paths from itself, not the active dir, so path needed
# qtCreatorFile = "GUI_Files/settings.ui" #Ui file name, from QtDesigner, assumes in same folder as this .py
#
# Ui_Settings, QtBaseClass = uic.loadUiType(qtCreatorFile) #process through pyuic
from GUI_Files.Settings import Ui_settings
class MyApp1(QMainWindow, Ui_settings): #gui class
    def __init__(self):
        #The following sets up the gui via Qt
        super(MyApp1, self).__init__()

        self.setupUi(self)

        # self.port_in.setText(config.get('main', 'ibkr_port'))

        dark_mode = config.get('main', 'dark_mode')
        if dark_mode == 'True':
            self.setStyleSheet(qdarkstyle.load_stylesheet())
            # self.logo.setPixmap(QPixmap("GUI_Files/logo_dark.png").transformed(QTransform().rotate(-90)))



        self.delegate = QtWidgets.QStyledItemDelegate()
        self.comboBox.addItems(['An', 'Aus'])
        if dark_mode == 'True':
            self.setStyleSheet(qdarkstyle.load_stylesheet())
            self.comboBox.setCurrentIndex(0)
        else:
            self.comboBox.setCurrentIndex(1)

        self.comboBox.setItemDelegate(self.delegate)


        self.lineEdit.setText(path_db)
        self.lineEdit_2.setText(path_k_exp)



        #set up callbacks

        self.b_close.clicked.connect(self.close)
        self.b_save_port.clicked.connect(self.save)




    def save(self):

        if self.comboBox.currentText() == 'An':
            dark_mode = 'True'
        else:
            dark_mode = 'False'


        # port =self.port_in.text()
        config.set('main', 'path_db', self.lineEdit.text())
        config.set('main', 'k_exp_path', self.lineEdit_2.text())
        config.set('main', 'dark_mode', dark_mode)
        with open(conf_path, 'w') as f:
            config.write(f)
        # print(port)






def settingsGUI():
    app = QApplication(sys.argv) #instantiate a QtGui (holder for the app)
    # app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    window = MyApp1()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    settingsGUI()