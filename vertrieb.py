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
from preisgruppen import MyApp1 as preisgruppen
from figuren import MyApp1 as figuren
from lander import MyApp1 as lander
from kunden import MyApp1 as kunden
from kunden_export import MyApp1 as kunden_export

#

# path = os.path.dirname(__file__) #uic paths from itself, not the active dir, so path needed
# qtCreatorFile = "GUI_Files/vertrieb.ui" #Ui file name, from QtDesigner, assumes in same folder as this .py
#
# Ui_Settings, QtBaseClass = uic.loadUiType(qtCreatorFile) #process through pyuic
from GUI_Files.Vertrieb import Ui_Main

class MyApp1(QMainWindow, Ui_Main): #gui class
    def __init__(self,data):
        #The following sets up the gui via Qt
        super(MyApp1, self).__init__()
        self.dialogs = list()
        self.setupUi(self)




        # self.port_in.setText(config.get('main', 'ibkr_port'))

        # self.simple_merge, self.df_gesamt, self.df_purchases = load_data.tabellen_zusamenfuegen()

        self.df_gesamt=data[0]
        self.df_purchases = data[1]
        self.purch_pos = data[2]

        #set up callbacks
        self.logo.setScaledContents(True)
        self.logo.setPixmap(QPixmap("GUI_Files/logo.png"))
        self.b_close.clicked.connect(self.close)
        self.b_pg.clicked.connect(self.preisgruppen_win)
        self.b_Lander.clicked.connect(self.lander_win)
        self.b_kunden.clicked.connect(self.kunden_win)
        self.b_export.clicked.connect(self.kunden_exp_win)
        self.b_fig.clicked.connect(self.fig_win)
        # self.b_settings.clicked.connect(self.settings_win)
        # self.setStyleSheet(qdarkstyle.load_stylesheet())

        dark_mode = False
        if dark_mode == 'True':
            self.setStyleSheet(qdarkstyle.load_stylesheet())
            self.logo.setPixmap(QPixmap("GUI_Files/logo_dark.png"))
    # def save_port(self):




        # port =self.port_in.text()

        # print(port)
    def fig_win(self):
        dialog = figuren(self.purch_pos)
        self.dialogs.append(dialog)
        dialog.show()

    def preisgruppen_win(self):
        dialog = preisgruppen([self.df_gesamt,self.df_purchases])
        self.dialogs.append(dialog)
        dialog.show()

    def lander_win(self):
        dialog = lander([self.df_gesamt,self.df_purchases])
        self.dialogs.append(dialog)
        dialog.show()

    def kunden_win(self):
        dialog = kunden([self.df_gesamt, self.df_purchases])
        self.dialogs.append(dialog)
        dialog.show()
    def kunden_exp_win(self):
        dialog = kunden_export(self.df_gesamt)
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