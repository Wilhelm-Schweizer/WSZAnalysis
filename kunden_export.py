import sys
import os
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic
import qdarkstyle
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import pandas as pd
import os
os.environ['QT_MAC_WANTS_LAYER'] = '1'
from configparser import ConfigParser
config = ConfigParser()
conf_path = 'config.ini'
config.read(conf_path)
from datetime import datetime as dt
path = config.get('main', 'path_db')
dark_mode = config.get('main', 'dark_mode')
path_k_exp = config.get('main', 'k_exp_path')
import shelve
# path = os.path.dirname(__file__) #uic paths from itself, not the active dir, so path needed
qtCreatorFile = "GUI_Files/kunden_export.ui" #Ui file name, from QtDesigner, assumes in same folder as this .py

Ui_Settings, QtBaseClass = uic.loadUiType(qtCreatorFile) #process through pyuic

class MyApp1(QMainWindow, Ui_Settings): #gui class
    def __init__(self,data):
        #The following sets up the gui via Qt
        super(MyApp1, self).__init__()

        self.setupUi(self)

        # self.port_in.setText(config.get('main', 'ibkr_port'))

        dark_mode = config.get('main', 'dark_mode')
        if dark_mode == 'True':
            self.setStyleSheet(qdarkstyle.load_stylesheet())
            # self.logo.setPixmap(QPixmap("GUI_Files/logo_dark.png").transformed(QTransform().rotate(-90)))
        # self.comboBox.addItems(['An','Aus'])



        self.data=data




        #set up callbacks

        self.b_close.clicked.connect(self.close)
        self.b_save.clicked.connect(self.save)


        today = dt.today().year
        print(today)

        l = ['Alle']

        for x in range(0,15):
            l.append(str(today-x))


        print(l)
        self.dic = shelve.open('helper/export_settings')

        self.lineEdit.setText(self.dic.get('file'))
        self.delegate = QtWidgets.QStyledItemDelegate()
        self.comboBox.setItemDelegate(self.delegate)
        self.comboBox.addItems(l)
        self.comboBox.setCurrentIndex(self.dic.get('best_ab')[1])
        self.comboBox_2.setItemDelegate(self.delegate)
        self.comboBox_2.addItems(l)
        self.comboBox_2.setCurrentIndex(self.dic.get('aufg_ab')[1])
        self.comboBox_3.setItemDelegate(self.delegate)
        self.comboBox_3.addItems(['Alle','Privat','Partner'])
        self.comboBox_3.setCurrentIndex(self.dic.get('preisg')[1])

        l = data['Land'].sort_values().dropna().unique().tolist()
        print(l)
        l = ['Alle','Inland','Ausland'] + l

        self.comboBox_4.setItemDelegate(self.delegate)
        self.comboBox_4.addItems(l)
        self.comboBox_4.setCurrentIndex(self.dic.get('land')[1])
        print(data.tail())
        self.comboBox_5.setItemDelegate(self.delegate)
        self.comboBox_5.addItems(['Keine','Land','Land & PLZ'])
        self.comboBox_5.setCurrentIndex(self.dic.get('sort')[1])

        self.checkBox.setChecked(self.dic.get('werb'))
        self.checkBox_2.setChecked(self.dic.get('ewerb'))

        # print(self.dic.get('preisg'))
        self.dic.close()



    def save(self):

        parms = {'file':self.lineEdit.text(),
                 'best_ab':[self.comboBox.currentText(),self.comboBox.currentIndex()],
                 'aufg_ab':[self.comboBox_2.currentText(),self.comboBox_2.currentIndex()],
                 'preisg':[self.comboBox_3.currentText(),self.comboBox_3.currentIndex()],
                 'land':[self.comboBox_4.currentText(),self.comboBox_4.currentIndex()],
                 'sort':[self.comboBox_5.currentText(),self.comboBox_5.currentIndex()],
                 'werb':self.checkBox.isChecked(),
                 'ewerb': self.checkBox_2.isChecked(),
                 }



        df = self.data



        if parms['best_ab'][0] != 'Alle':
            y = dt.strptime(parms['best_ab'][0],'%Y')
            df = df.loc[df['letzteLieferung']>y]



        if parms['aufg_ab'][0] != 'Alle':
            y = dt.strptime(parms['aufg_ab'][0],'%Y')
            df = df.loc[df['AufnahmeDatum']>y]


        if parms['preisg'][0] != 'Alle':
            if parms['preisg'][0] == 'Privat':
                df = df.loc[df['Preisgruppe']==1]
            elif parms['preisg'][0] == 'Partner':
                df = df.loc[df['Preisgruppe']==2]

        if parms['land'][0] != 'Alle' and parms['land'][0] != 'Inland' and parms['land'][0] != 'Ausland':
            df = df[df['Land'] == parms['land'][0]]
        elif parms['land'][0] == 'Inland':
            df = df[df['Land'] == 'DE']
        elif parms['land'][0] == 'Ausland':
            df = df[df['Land'] != 'DE']

        if parms['sort'][0] == 'Land & PLZ':
            df = df.sort_values(['Land', 'PLZ'])
        elif parms['sort'][0] != 'Keine':
            df=df.sort_values(parms['sort'][0])

        if parms['werb'] == True:

            df = df.loc[df['Werbung']!= 1]
        if parms['ewerb'] == True:
            df = df.loc[df['E_Werbung'] != 1]

        df = df.reset_index(drop = True)
        print(df.tail())



        print(path_k_exp+'/'+parms['file']+'.csv')
        try:
            df.to_csv(path_k_exp+'/'+parms['file']+'.csv',index=False,encoding = 'utf-8-sig')
        except:
            try:
                os.mkdir(path_k_exp+'/'+parms['file'].split('/')[0])
                print(path_k_exp+'/'+parms['file'].split('/')[0])
                df.to_csv(path_k_exp + '/' + parms['file'] + '.csv', index=False, encoding='utf-8-sig')
            except:
                pass

        self.dic = shelve.open('helper/export_settings')
        self.dic.update(parms)
        self.dic.close()







def settingsGUI(data):
    app = QApplication(sys.argv) #instantiate a QtGui (holder for the app)
    # app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    window = MyApp1(data)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    import load_data
    data = load_data.tabellen_zusamenfuegen()[1]
    settingsGUI(data)