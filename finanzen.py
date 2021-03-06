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
from configparser import ConfigParser
config = ConfigParser()

config.read('config.ini')
from incomestatement import MyApp1 as incomestatement

from settings import MyApp1 as settings
import load_data
#

# path = os.path.dirname(__file__) #uic paths from itself, not the active dir, so path needed
# qtCreatorFile = "GUI_Files/produktion.ui" #Ui file name, from QtDesigner, assumes in same folder as this .py
#
# Ui_Settings, QtBaseClass = uic.loadUiType(qtCreatorFile) #process through pyuic

from GUI_Files.finanzen import  Ui_Main

class MyApp1(QMainWindow, Ui_Main): #gui class
    def __init__(self,data):
        #The following sets up the gui via Qt
        super(MyApp1, self).__init__()
        self.dialogs = list()
        self.setupUi(self)




        # self.port_in.setText(config.get('main', 'ibkr_port'))

        # self.simple_merge, self.df_gesamt, self.df_purchases = load_data.tabellen_zusamenfuegen()

        self.df_is = data

        #set up callbacks
        self.logo.setScaledContents(True)
        self.logo.setPixmap(QPixmap("GUI_Files/logo.png"))
        self.b_close.clicked.connect(self.close)
        self.b_pg.clicked.connect(self.is_win)
        # self.b_Lander.clicked.connect(self.lander_win)
        # self.b_kunden.clicked.connect(self.kunden_win)
        # self.b_settings.clicked.connect(self.settings_win)
        # self.setStyleSheet(qdarkstyle.load_stylesheet())

        dark_mode = False
        if dark_mode == 'True':
            self.setStyleSheet(qdarkstyle.load_stylesheet())
            self.logo.setPixmap(QPixmap("GUI_Files/logo_dark.png"))
    # def save_port(self):




        # port =self.port_in.text()

        # print(port)


    def is_win(self):
        dialog = incomestatement(self.df_is)
        self.dialogs.append(dialog)
        dialog.show()

    # def lander_win(self):
    #     dialog = lander([self.df_gesamt,self.df_purchases])
    #     self.dialogs.append(dialog)
    #     dialog.show()
    #
    # def kunden_win(self):
    #     dialog = kunden([self.df_gesamt, self.df_purchases])
    #     self.dialogs.append(dialog)
    #     dialog.show()





def mainGUI():
    app = QApplication(sys.argv) #instantiate a QtGui (holder for the app)
    # app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    window = MyApp1()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    mainGUI()