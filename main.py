print('Programm Startet...')
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
from vertrieb import MyApp1 as vertrieb
from produktion import MyApp1 as produktion
from finanzen import MyApp1 as finanzen
from settings import MyApp1 as settings
import load_data
#
from GUI_Files.Main import Ui_Main
# path = os.path.dirname(__file__) #uic paths from itself, not the active dir, so path needed
# qtCreatorFile = "GUI_Files/main.ui" #Ui file name, from QtDesigner, assumes in same folder as this .py
#
# Ui_Settings, QtBaseClass = uic.loadUiType(qtCreatorFile) #process through pyuic

class MyApp1(QMainWindow,Ui_Main): #gui class
    def __init__(self):
        #The following sets up the gui via Qt
        super(MyApp1, self).__init__()
        self.dialogs = list()

        self.setupUi(self)




        # self.port_in.setText(config.get('main', 'ibkr_port'))
        data = load_data.vertrieb()
        if data !=False:
            self.simple_merge, self.df_gesamt, self.df_purchases,self.purch_pos = data
            self.b_vertrieb.clicked.connect(self.vertrieb_win)
        else:
            self.b_vertrieb.deleteLater()

        data = load_data.produktion()
        if data != False:
            self.df_werk = data
            self.b_prod.clicked.connect(self.produktion_win)
        else:
            self.b_prod.deleteLater()

        data = load_data.finanzen()
        if data != False:
            self.df_is = data
            self.b_fin.clicked.connect(self.fin_win)
        else:
            self.b_fin.deleteLater()

        #set up callbacks
        # self.logo.setScaledContents(True)
        # self.logo.setPixmap(QPixmap("GUI_Files/logo.png"))

        self.b_close.clicked.connect(self.close)


        # self.b_kunden.clicked.connect(self.kunden_win)
        self.b_settings.clicked.connect(self.settings_win)
        # self.setStyleSheet(qdarkstyle.load_stylesheet())
        self.logo.setScaledContents(True)
        self.logo.setPixmap(QPixmap("GUI_Files/logo.png"))
        dark_mode = False
        if dark_mode == 'True':
            self.setStyleSheet(qdarkstyle.load_stylesheet())
            self.logo.setPixmap(QPixmap("GUI_Files/logo_dark.png"))
    # def save_port(self):




        # port =self.port_in.text()

        # print(port)


    def vertrieb_win(self):
        dialog = vertrieb([self.df_gesamt,self.df_purchases,self.purch_pos])
        self.dialogs.append(dialog)
        dialog.show()

    def produktion_win(self):
        dialog = produktion(self.df_werk)
        self.dialogs.append(dialog)
        dialog.show()
    def fin_win(self):
        dialog = finanzen(self.df_is)
        self.dialogs.append(dialog)
        dialog.show()


    def settings_win(self):
        dialog = settings()
        self.dialogs.append(dialog)
        dialog.show()



def mainGUI():
    app = QApplication(sys.argv) #instantiate a QtGui (holder for the app)
    # app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    window = MyApp1()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    mainGUI()