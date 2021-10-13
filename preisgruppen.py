
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic
import qdarkstyle
import pandas as pd
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg
import numpy as np

from datetime import datetime as dt
from datetime import timedelta
from configparser import ConfigParser

import sys,os
os.environ['QT_MAC_WANTS_LAYER'] = '1'


from pg_stats import MyApp1 as pg_stats


config = ConfigParser()
config.read('config.ini')








# dark_mode = config.get('main', 'dark_mode')



# import pyqtgraph.examples
# pyqtgraph.examples.run()
# path = os.path.dirname(__file__) #uic paths from itself, not the active dir, so path needed
qtCreatorFile = "GUI_Files/preisgruppen.ui" #Ui file name, from QtDesigner, assumes in same folder as this .py

Ui_Error, QtBaseClass = uic.loadUiType(qtCreatorFile) #process through pyuic

class MyApp1(QMainWindow, Ui_Error): #gui class
    def __init__(self,data):
        #The following sets up the gui via Qt
        super(MyApp1, self).__init__()
        self.df = data[0]
        self.df1 = data[1]
        import random

        # print(data)
        self.dialogs = list()
        self.setupUi(self)
        # if dark_mode == 'True':
        #     self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())


        #set up callbacks
        # self.label.setText(label_txt)
        # self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.label.setAlignment(Qt.AlignCenter)
        # self.ui.label.setStyleSheet("QLabel {background-color: red;}")
        self.b_close.clicked.connect(self.close)
        self.refresh_b.clicked.connect(self.refresh)
        self.b_stats.clicked.connect(self.pg_stats_win)
        self.logo.setScaledContents(True)
        self.logo.setPixmap(QPixmap("GUI_Files/logo.png").transformed(QTransform().rotate(-90)))
        dark_mode = config.get('main', 'dark_mode')
        if dark_mode == 'True':
            self.setStyleSheet(qdarkstyle.load_stylesheet())
            self.logo.setPixmap(QPixmap("GUI_Files/logo_dark.png").transformed(QTransform().rotate(-90)))
        self.checkBox_2.setChecked(True)

        delegate = QStyledItemDelegate()
        self.comboBox.setItemDelegate(delegate)
        self.comboBox.addItems(['1 Jahr - ' +str(dt.today().year -1),'2 Jahre - ' +str(dt.today().year -2),'3 Jahre - ' +str(dt.today().year -3),'4 Jahre - ' +str(dt.today().year -4),'5 Jahre - ' +str(dt.today().year -5),'10 Jahre - ' +str(dt.today().year -10),'20 Jahre - ' +str(dt.today().year -20)])
        self.comboBox.setCurrentIndex(4)



        # print(self.bm)
        # print(self.df)

        # print(self.df['date'],self.df['total_value'])
        # print(pd.to_datetime(self.df['date']))



        # print(df)
        # self.df = self.df.iloc[80:].reset_index(drop=True)

        # self.plt_df = self.df
        self.refresh()
        self.create_plot()



    def create_plot(self):





        for i in reversed(range(self.verticalLayout.count())):
            self.verticalLayout.itemAt(i).widget().setParent(None)

        df = self.df
        df1 = self.df1


        datum = self.comboBox.currentText().split('-')[1]
        if self.checkBox.isChecked() == True:
            datum = ' 2000'

        df1['Periode'] = pd.to_datetime(df1['Periode'], format='%Y%m', errors='coerce')
        df1 = df1[df1['Periode'] >= dt.strptime(datum, ' %Y')].reset_index(drop=True)
        df1 = df1[df1['Periode'] <= dt.today().replace(day=1) - timedelta(days=1)].reset_index(drop=True)
        # df1 = df1.tail(100).reset_index(drop=True)

        df = df[['KundenNr', 'Preisgruppe']]

        join = pd.merge(df1, df, on='KundenNr', how='inner')

        df1 = join[['KundenNr', 'EUR_sum', 'Periode', 'Preisgruppe']]
        # print(join.tail())
        # df1['Preisgruppe']=0
        # for i,r in df1.iterrows():
        #     try:
        #         print(i,'/',len(df1),df.loc[df['KundenNr']==r['KundenNr']]['Preisgruppe'].reset_index(drop=True)[0])
        #         df1['Preisgruppe'][i]= df.loc[df['KundenNr']==r['KundenNr']]['Preisgruppe'].reset_index(drop=True)[0]
        #     except:
        #         df1['Preisgruppe'][i] =0
        print(df1.tail())
        df1['year'] = df1['Periode'].dt.year
        df1['month'] = 0

        df_pr = df1.loc[df1['Preisgruppe'] == 1]
        df_pa = df1.loc[df1['Preisgruppe'] == 2]
        df_ges = df1
        self.df_pr = df_pr
        self.df_pa = df_pa
        self.df_ges = df_ges

        if self.checkBox.isChecked()==True:

            annual_ges = [df1[df1['year'] == y] for y in df1['year'].unique()]

            annual_pr = [df_pr[df_pr['year'] == y] for y in df_pr['year'].unique()]
            annual_pa = [df_pa[df_pa['year'] == y] for y in df_pa['year'].unique()]
            # print(annaul_pr)
            x = 0
            for i in annual_ges:
                annual_ges[x] = i.groupby('Periode')['EUR_sum'].sum().reset_index()
                annual_ges[x]['month'] = annual_ges[x]['Periode'].dt.month
                # print(annaul_ges[x].tail(20))

                x += 1

            x = 0
            for i in annual_pr:
                annual_pr[x] = i.groupby('Periode')['EUR_sum'].sum().reset_index()
                annual_pr[x]['month'] = annual_pr[x]['Periode'].dt.month
                print(annual_pr[x].tail(20))

                x += 1

            # print(annaul_pr)
            x = 0
            for i in annual_pa:
                annual_pa[x] = i.groupby('Periode')['EUR_sum'].sum().reset_index()
                annual_pa[x]['month'] = annual_pa[x]['Periode'].dt.month
                print(annual_pa[x].tail(20))

                x += 1


            dic = {self.checkBox_2:[annual_ges,'Gesamt'],self.checkBox_3:[annual_pr,'Privat'],self.checkBox_4:[annual_pa,'Partner']}
        else:
            df_pr = df_pr.groupby('Periode')['EUR_sum'].sum().reset_index()
            df_pa = df_pa.groupby('Periode')['EUR_sum'].sum().reset_index()
            df_ges = df1.groupby('Periode')['EUR_sum'].sum().reset_index()
            dic = {self.checkBox_2: [df_ges, 'Gesamt'], self.checkBox_3: [df_pr, 'Privat'],
                   self.checkBox_4: [df_pa, 'Partner']}

        for k in dic.keys():


            if k.isChecked()==True:
                lbl = QLabel()
                lbl.setText(dic[k][1])
                lbl.setAlignment(Qt.AlignCenter)
                self.verticalLayout.addWidget(lbl)
                if self.checkBox.isChecked() == False:



                    self.plt_df = dic[k][0]



                    dates = self.plt_df['Periode']
                    date_axis = pg.graphicsItems.DateAxisItem.DateAxisItem(orientation='bottom')
                    self.graphWidget = pg.PlotWidget(axisItems = {'bottom': date_axis})
                    self.verticalLayout.addWidget(self.graphWidget,0)
                    self.graphWidget.addLegend()
                    self.graphWidget.plot(dates.values.astype(np.int64) // 10 ** 9, self.plt_df['EUR_sum'])
                    self.graphWidget.showGrid(x=True,y=True)
                    self.graphWidget.addLine(x=None, y=0, pen=pg.mkPen('r', width=3))
                    self.graphWidget.sizeHint = lambda: pg.QtCore.QSize(100, 100)

                else:
                    self.graphWidget = pg.PlotWidget()
                    self.verticalLayout.addWidget(self.graphWidget, 0)
                    self.graphWidget.addLegend()
                    for i in dic[k][0][0:-2]:
                        self.graphWidget.plot(i['month'], i['EUR_sum'],)

                    self.graphWidget.plot(dic[k][0][-2]['month'], dic[k][0][-2]['EUR_sum'], pen=pg.mkPen('b', width=5),name = dt.today().year - 1)
                    self.graphWidget.plot(dic[k][0][-1]['month'], dic[k][0][-1]['EUR_sum'], pen=pg.mkPen('g', width=7),name = dt.today().year)
                    self.graphWidget.showGrid(x=True,y=True)
                    self.graphWidget.addLine(x=None, y=0, pen=pg.mkPen('r', width=3))
                    self.graphWidget.sizeHint = lambda: pg.QtCore.QSize(100, 100)


                # bm_date = self.bm['Date'].reset_index(drop=True)
                # print(dates,bm_date)
                # if self.bm_ex != False:
                #     self.graphWidget.plot(dates.values.astype(np.int64) // 10 ** 9,self.plt_df['cum_pct_change_bm']*100, pen=pg.mkPen('b', width=2),name = 'SPY')

                # self.graphWidget.addLine(x=None, y=self.df['cum_pct_change'].iloc[-1]*100, pen=pg.mkPen('b', width=1))
                # print(self.plt_df.tail())



    def refresh(self):


        # if self.comboBox.currentText() == 'All extended':
        #     start_date = '01.01.2015'
        #     self.plt_df = self.recalculate_df(start_date)
        #
        # if self.comboBox.currentText() == 'Since 2020':
        #     start_date = '01.01.2020'
        #     self.plt_df = self.recalculate_df(start_date)
        # if self.comboBox.currentText() == 'YTD':
        #     start_date = dt(dt.today().year, 1, 1)
        #     self.plt_df = self.recalculate_df(start_date)
        #
        #
        # if self.comboBox.currentText() == 'Trailing Month':
        #     start_date = dt.today() - timedelta(days=31)
        #     self.plt_df = self.recalculate_df(start_date)
        #
        # if self.comboBox.currentText() == 'Trailing Week':
        #     start_date =  dt.today() - timedelta(days=7)
        #     self.plt_df = self.recalculate_df(start_date)

        self.create_plot()
    def pg_stats_win(self):
        dialog = pg_stats([self.df_pr,self.df_pa,self.df_ges])
        self.dialogs.append(dialog)
        dialog.show()



    #
    # def recalculate_df(self, start_date):
    #
    #     df = self.df.loc[self.df['date'] > start_date].reset_index(drop=True)
    #     # print(df.head())
    #     df['cum_pct_change'] = (df['pct_change'][1:] + 1).cumprod() - 1
    #     df['cum_pct_change'].iloc[0] = 0
    #
    #     if self.bm_ex != False:
    #         df['cum_pct_change_bm'] = (df['pct_change_bm'][1:] + 1).cumprod() - 1
    #         df['cum_pct_change_bm'].iloc[0] = 0
    #
    #     print(df.head())
    #     return df











def preisgruppenGUI():
    app = QApplication(sys.argv) #instantiate a QtGui (holder for the app)
    # app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    window = MyApp1()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    preisgruppenGUI()
