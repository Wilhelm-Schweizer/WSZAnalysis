
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
qtCreatorFile = "GUI_Files/kunden.ui" #Ui file name, from QtDesigner, assumes in same folder as this .py

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
        self.dark_mode = config.get('main', 'dark_mode')
        self.main_col = 'k'
        if self.dark_mode == 'True':
            self.setStyleSheet(qdarkstyle.load_stylesheet())
            self.logo.setPixmap(QPixmap("GUI_Files/logo_dark.png").transformed(QTransform().rotate(-90)))
            self.main_col = 'w'
        # self.checkBox_2.setChecked(True)

        delegate = QStyledItemDelegate()
        self.comboBox.setItemDelegate(delegate)
        self.comboBox.addItems(['1 Jahr - ' +str(dt.today().year -1),'2 Jahre - ' +str(dt.today().year -2),'3 Jahre - ' +str(dt.today().year -3),'4 Jahre - ' +str(dt.today().year -4),'5 Jahre - ' +str(dt.today().year -5),'10 Jahre - ' +str(dt.today().year -10),'20 Jahre - ' +str(dt.today().year -20)])
        self.comboBox.setCurrentIndex(5)

        self.comboBox_3.setItemDelegate(delegate)
        self.comboBox_3.addItems(['Normal','Jahresübersicht','Kumulativ','Durchschnitt Bestellung'])
        self.comboBox_3.setCurrentIndex(0)
        self.comboBox_4.setItemDelegate(delegate)
        self.comboBox_4.addItems(['Alle','Privat','Partner'])
        self.comboBox_4.setCurrentIndex(0)
        # print(data[0]['Land'].unique().tolist())
        self.comboBox_2.setItemDelegate(delegate)
        l = data[0]['KundenNr'].sort_values().dropna().unique().tolist()
        print(l)
        l = ['Top 4','Top 4 Vergleich','Top'] + l
        self.comboBox_2.addItems(l)
        self.comboBox_2.setCurrentIndex(0)


        # print(data[0].loc[data[0]['Land']=='MEXIC'])
        # print(self.bm)
        # print(self.df)

        # print(self.df['date'],self.df['total_value'])
        # print(pd.to_datetime(self.df['date']))



        # print(df)
        # self.df = self.df.iloc[80:].reset_index(drop=True)

        # self.plt_df = self.df
        self.refresh()
        # self.create_plot()



    def create_plot(self):





        for i in reversed(range(self.verticalLayout.count())):
            self.verticalLayout.itemAt(i).widget().setParent(None)
        for i in reversed(range(self.verticalLayout_2.count())):
            self.verticalLayout_2.itemAt(i).widget().setParent(None)
        #
        df = self.df
        df1 = self.df1
        #
        #
        datum = self.comboBox.currentText().split('-')[1]






        if self.comboBox_3.currentText() == 'Jahresübersicht':
            datum = ' 2000'
        #
        df1['Periode'] = pd.to_datetime(df1['Periode'], format='%Y%m', errors='coerce')
        df1 = df1[df1['Periode'] >= dt.strptime(datum, ' %Y')].reset_index(drop=True)
        df1 = df1[df1['Periode'] <= dt.today().replace(day=1) - timedelta(days=1)].reset_index(drop=True)
        # # df1 = df1.tail(100).reset_index(drop=True)
        #
        df = df[['KundenNr', 'Preisgruppe','Land']]
        #
        join = pd.merge(df1, df, on='KundenNr', how='inner')
        #
        df1 = join[['KundenNr', 'EUR_sum', 'Periode', 'Preisgruppe','Land']]

        if self.comboBox_4.currentText()=='Privat':
            df1 = df1.loc[df1['Preisgruppe']==1]
        if self.comboBox_4.currentText()=='Partner':
            df1 = df1.loc[df1['Preisgruppe']==2]

        print(df1.tail())
        df1 = df1.loc[df1['EUR_sum']>0].reset_index(drop=True)

        # print(df1.tail())
        df1['year'] = df1['Periode'].dt.year
        df1['month'] = 0

        if self.comboBox_2.currentText() == 'Top 4 Vergleich':
            top = df1.groupby('KundenNr').sum().reset_index().sort_values(['EUR_sum'], ascending=False).head(4).reset_index(
                drop=True)
            plt_df= pd.DataFrame()
            plt_df['Periode'] = df1['Periode'].drop_duplicates()
            plt_df =plt_df.sort_values('Periode').reset_index(drop=True)
            print(plt_df.tail())


            for i, r in top.iterrows():
                print(i)
                df_m = df1.loc[df1['KundenNr']==r['KundenNr']].groupby('Periode')['EUR_sum'].sum().reset_index().rename(columns={'EUR_sum':r['KundenNr']})
                plt_df = plt_df.merge(df_m,on='Periode')

            plt_df['sum'] = 0
            for c in list(plt_df)[1:-1]:
                print(c)
                plt_df['sum'] = plt_df['sum'] + plt_df[c]


            plt_df_pct = pd.DataFrame()
            plt_df_pct['Periode'] = plt_df['Periode']
            for c in list(plt_df)[1:-1]:

                plt_df_pct[c] = plt_df[c]/ plt_df['sum']
                # plt_df_pct = plt_df_pct.loc[plt_df_pct[c]>0].reset_index(drop=True)


                plt_df_pct[c] = plt_df_pct[c].rolling(window=12).mean()

            plt_df_pct = plt_df_pct.loc[plt_df_pct[list(plt_df)[1]] > 0].reset_index(drop=True)
            print(plt_df_pct.head(500))
            # print(plt_df_pct.tail())
            self.plots(plt_df_pct, self.comboBox_2.currentText(), 1)
            # return
        elif self.comboBox_2.currentText() == 'Top 4':

            top = df1.groupby('KundenNr').sum().reset_index().sort_values(['EUR_sum'], ascending=False).head(4).reset_index(drop=True)

            for i,r in top.iterrows():
                self.plots(df1,r['KundenNr'],i)
        elif self.comboBox_2.currentText() == 'Top':
            top = df1.groupby('KundenNr').sum().reset_index().sort_values(['EUR_sum'], ascending=False).head(1).reset_index(
                drop=True)

            for i, r in top.iterrows():
                self.plots(df1, r['KundenNr'], i)
        else:
            self.plots(df1, self.comboBox_2.currentText(), 1)



    def plots(self,df1,KundenNr,i):
        if i <2 :
            layout = self.verticalLayout
        else:
            layout = self.verticalLayout_2

        lbl = QLabel()
        lbl.setText(KundenNr)
        lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl)
        MA_win = 24

        if self.comboBox_2.currentText() == 'Top 4 Vergleich':
            dates = df1['Periode']
            date_axis = pg.graphicsItems.DateAxisItem.DateAxisItem(orientation='bottom')
            self.graphWidget = pg.PlotWidget(axisItems = {'bottom': date_axis})
            layout.addWidget(self.graphWidget)
            self.graphWidget.addLegend()
            df1.reindex(df1.mean().sort_values().index, axis=1)
            print(df1.tail())
            df1['sum'] = 1
            col = ['g','y','b','w']
            x = 0

            for c in list(df1)[1:-1]: #list(reversed(list(df1)))[1:-1]:
                if x != 0:
                    df1['sum'] = df1['sum'] - df1[list(df1)[x]]
                print(c)

                self.graphWidget.plot(dates.values.astype(np.int64) // 10 ** 9, df1['sum'],fillLevel = 0,name = c, fillBrush=col[x],pen = col[x])

                x+=1

            self.graphWidget.showGrid(x=True, y=True)
            self.graphWidget.addLine(x=None, y=0, pen=pg.mkPen('r', width=3))
            self.graphWidget.sizeHint = lambda: pg.QtCore.QSize(100, 100)
            if self.dark_mode != 'True':
                self.graphWidget.setBackground('w')
            return


        elif self.comboBox_3.currentText() == 'Normal':



            plt_df = df1.loc[df1['KundenNr']== KundenNr]
            plt_df = plt_df.groupby('Periode')['EUR_sum'].sum().reset_index()

            dates = plt_df['Periode']
            date_axis = pg.graphicsItems.DateAxisItem.DateAxisItem(orientation='bottom')
            self.graphWidget = pg.PlotWidget(axisItems = {'bottom': date_axis})
            layout.addWidget(self.graphWidget)
            self.graphWidget.addLegend()
            self.graphWidget.plot(dates.values.astype(np.int64) // 10 ** 9, plt_df['EUR_sum'],pen = pg.mkPen(self.main_col, width=5))
            self.graphWidget.showGrid(x=True,y=True)
            self.graphWidget.addLine(x=None, y=0, pen=pg.mkPen('r', width=3))
            self.graphWidget.sizeHint = lambda: pg.QtCore.QSize(100, 100)
            plt_df['MA'] = plt_df['EUR_sum'].rolling(window=MA_win).mean()
            self.graphWidget.plot(dates.values.astype(np.int64) // 10 ** 9, plt_df['MA'],
                                  pen=pg.mkPen('g', width=5), name=str(MA_win) + "MO MA")
        elif self.comboBox_3.currentText() == 'Kumulativ':
            plt_df = df1.loc[df1['KundenNr'] == KundenNr]
            plt_df = plt_df.groupby('Periode')['EUR_sum'].sum().reset_index()
            plt_df['r_sum'] = plt_df['EUR_sum'].expanding(2).sum()
            dates = plt_df['Periode']
            date_axis = pg.graphicsItems.DateAxisItem.DateAxisItem(orientation='bottom')
            self.graphWidget = pg.PlotWidget(axisItems={'bottom': date_axis})
            layout.addWidget(self.graphWidget)
            self.graphWidget.addLegend()
            self.graphWidget.plot(dates.values.astype(np.int64) // 10 ** 9, plt_df['r_sum'], stepmode=True, fillLevel=0, fillOutline=True,pen = pg.mkPen(self.main_col, width=5))
            self.graphWidget.showGrid(x=True, y=True)
            self.graphWidget.addLine(x=None, y=0, pen=pg.mkPen('r', width=3))
            self.graphWidget.sizeHint = lambda: pg.QtCore.QSize(100, 100)
        elif self.comboBox_3.currentText() == 'Durchschnitt Bestellung':
            plt_df = df1.loc[df1['KundenNr'] == KundenNr]
            print(plt_df.tail())
            plt_df = plt_df.groupby('Periode')['EUR_sum'].mean().reset_index()
            print(plt_df.tail())
            dates = plt_df['Periode']
            date_axis = pg.graphicsItems.DateAxisItem.DateAxisItem(orientation='bottom')
            self.graphWidget = pg.PlotWidget(axisItems={'bottom': date_axis})
            layout.addWidget(self.graphWidget)
            self.graphWidget.addLegend()
            self.graphWidget.plot(dates.values.astype(np.int64) // 10 ** 9, plt_df['EUR_sum'], stepmode=True, fillLevel=0, fillOutline=True,pen = pg.mkPen(self.main_col, width=5))
            self.graphWidget.showGrid(x=True, y=True)
            self.graphWidget.addLine(x=None, y=0, pen=pg.mkPen('r', width=3))
            self.graphWidget.sizeHint = lambda: pg.QtCore.QSize(100, 100)
            plt_df['MA'] = plt_df['EUR_sum'].rolling(window=MA_win).mean()
            self.graphWidget.plot(dates.values.astype(np.int64) // 10 ** 9, plt_df['MA'],
                                  pen=pg.mkPen('g', width=5), name=str(MA_win) + "MO MA")
        elif self.comboBox_3.currentText() == 'Jahresübersicht':

            df1 = df1.loc[df1['KundenNr'] == KundenNr]
            annual = [df1[df1['year'] == y] for y in df1['year'].unique()]


            # print(annaul_pr)
            x = 0
            for i in annual:
                annual[x] = i.groupby('Periode')['EUR_sum'].sum().reset_index()
                annual[x]['month'] = annual[x]['Periode'].dt.month
                # print(annaul_ges[x].tail(20))

                x += 1

            x = 0
            self.graphWidget = pg.PlotWidget()
            layout.addWidget(self.graphWidget, 0)
            self.graphWidget.addLegend()
            for i in annual[0:-2]:
                self.graphWidget.plot(i['month'], i['EUR_sum'],)

            self.graphWidget.plot(annual[-2]['month'], annual[-2]['EUR_sum'], pen=pg.mkPen('b', width=5),name = annual[-2]['Periode'][0].year)
            self.graphWidget.plot(annual[-1]['month'], annual[-1]['EUR_sum'], pen=pg.mkPen('g', width=7),name = annual[-1]['Periode'][0].year)
            self.graphWidget.showGrid(x=True,y=True)
            self.graphWidget.addLine(x=None, y=0, pen=pg.mkPen('r', width=3))
            self.graphWidget.sizeHint = lambda: pg.QtCore.QSize(100, 100)
        if self.dark_mode != 'True':
            self.graphWidget.setBackground('w')
                    #
                    # bargraph = pg.BarGraphItem(x=plt_df['Periode'], y=plt_df['EUR_sum'], width=0.6, brush='g')
                    # self.gridLayout.addItem(bargraph)
        #
        # df_pr = df1.loc[df1['Preisgruppe'] == 1]
        # df_pa = df1.loc[df1['Preisgruppe'] == 2]
        # df_ges = df1
        # self.df_pr = df_pr
        # self.df_pa = df_pa
        # self.df_ges = df_ges
        #
        # if self.checkBox.isChecked()==True:
        #
        #     annual_ges = [df1[df1['year'] == y] for y in df1['year'].unique()]
        #
        #     annual_pr = [df_pr[df_pr['year'] == y] for y in df_pr['year'].unique()]
        #     annual_pa = [df_pa[df_pa['year'] == y] for y in df_pa['year'].unique()]
        #     # print(annaul_pr)
        #     x = 0
        #     for i in annual_ges:
        #         annual_ges[x] = i.groupby('Periode')['EUR_sum'].sum().reset_index()
        #         annual_ges[x]['month'] = annual_ges[x]['Periode'].dt.month
        #         # print(annaul_ges[x].tail(20))
        #
        #         x += 1
        #
        #     x = 0
        #     for i in annual_pr:
        #         annual_pr[x] = i.groupby('Periode')['EUR_sum'].sum().reset_index()
        #         annual_pr[x]['month'] = annual_pr[x]['Periode'].dt.month
        #         print(annual_pr[x].tail(20))
        #
        #         x += 1
        #
        #     # print(annaul_pr)
        #     x = 0
        #     for i in annual_pa:
        #         annual_pa[x] = i.groupby('Periode')['EUR_sum'].sum().reset_index()
        #         annual_pa[x]['month'] = annual_pa[x]['Periode'].dt.month
        #         print(annual_pa[x].tail(20))
        #
        #         x += 1
        #
        #
        #     dic = {self.checkBox_2:[annual_ges,'Gesamt'],self.checkBox_3:[annual_pr,'Privat'],self.checkBox_4:[annual_pa,'Partner']}
        # else:
        #     df_pr = df_pr.groupby('Periode')['EUR_sum'].sum().reset_index()
        #     df_pa = df_pa.groupby('Periode')['EUR_sum'].sum().reset_index()
        #     df_ges = df1.groupby('Periode')['EUR_sum'].sum().reset_index()
        #     dic = {self.checkBox_2: [df_ges, 'Gesamt'], self.checkBox_3: [df_pr, 'Privat'],
        #            self.checkBox_4: [df_pa, 'Partner']}
        #
        # for k in dic.keys():
        #
        #
        #     if k.isChecked()==True:
        #         lbl = QLabel()
        #         lbl.setText(dic[k][1])
        #         lbl.setAlignment(Qt.AlignCenter)
        #         self.verticalLayout.addWidget(lbl)
        #         if self.checkBox.isChecked() == False:
        #
        #
        #
        #             self.plt_df = dic[k][0]
        #
        #
        #
        #             dates = self.plt_df['Periode']
        #             date_axis = pg.graphicsItems.DateAxisItem.DateAxisItem(orientation='bottom')
        #             self.graphWidget = pg.PlotWidget(axisItems = {'bottom': date_axis})
        #             self.verticalLayout.addWidget(self.graphWidget,0)
        #             self.graphWidget.addLegend()
        #             self.graphWidget.plot(dates.values.astype(np.int64) // 10 ** 9, self.plt_df['EUR_sum'])
        #             self.graphWidget.showGrid(x=True,y=True)
        #             self.graphWidget.addLine(x=None, y=0, pen=pg.mkPen('r', width=3))
        #             self.graphWidget.sizeHint = lambda: pg.QtCore.QSize(100, 100)
        #
        #         else:
        #             self.graphWidget = pg.PlotWidget()
        #             self.verticalLayout.addWidget(self.graphWidget, 0)
        #             self.graphWidget.addLegend()
        #             for i in dic[k][0][0:-2]:
        #                 self.graphWidget.plot(i['month'], i['EUR_sum'],)
        #
        #             self.graphWidget.plot(dic[k][0][-2]['month'], dic[k][0][-2]['EUR_sum'], pen=pg.mkPen('b', width=5),name = dt.today().year - 1)
        #             self.graphWidget.plot(dic[k][0][-1]['month'], dic[k][0][-1]['EUR_sum'], pen=pg.mkPen('g', width=7),name = dt.today().year)
        #             self.graphWidget.showGrid(x=True,y=True)
        #             self.graphWidget.addLine(x=None, y=0, pen=pg.mkPen('r', width=3))
        #             self.graphWidget.sizeHint = lambda: pg.QtCore.QSize(100, 100)
        #
        #
        #         # bm_date = self.bm['Date'].reset_index(drop=True)
        #         # print(dates,bm_date)
        #         # if self.bm_ex != False:
        #         #     self.graphWidget.plot(dates.values.astype(np.int64) // 10 ** 9,self.plt_df['cum_pct_change_bm']*100, pen=pg.mkPen('b', width=2),name = 'SPY')
        #
        #         # self.graphWidget.addLine(x=None, y=self.df['cum_pct_change'].iloc[-1]*100, pen=pg.mkPen('b', width=1))
        #         # print(self.plt_df.tail())



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











def kundenGUI():
    app = QApplication(sys.argv) #instantiate a QtGui (holder for the app)
    # app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    window = MyApp1()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    kundenGUI()
