
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
from ipywidgets import interact, interactive, fixed, interact_manual
from datetime import datetime as dt
from datetime import timedelta
from configparser import ConfigParser

import sys,os
os.environ['QT_MAC_WANTS_LAYER'] = '1'


from pg_stats import MyApp1 as pg_stats


config = ConfigParser()
config.read('config.ini')


import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from mpl_toolkits.mplot3d import Axes3D




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
        self.dark_mode = config.get('main', 'dark_mode')
        self.main_col = 'k'
        if self.dark_mode == 'True':
            self.setStyleSheet(qdarkstyle.load_stylesheet())
            self.logo.setPixmap(QPixmap("GUI_Files/logo_dark.png").transformed(QTransform().rotate(-90)))
            self.main_col = 'w'


        self.checkBox_2.setChecked(True)

        delegate = QStyledItemDelegate()
        self.comboBox.setItemDelegate(delegate)
        self.comboBox.addItems(['1 Jahr - ' +str(dt.today().year -1),'2 Jahre - ' +str(dt.today().year -2),'3 Jahre - ' +str(dt.today().year -3),'4 Jahre - ' +str(dt.today().year -4),'5 Jahre - ' +str(dt.today().year -5),'10 Jahre - ' +str(dt.today().year -10),'20 Jahre - ' +str(dt.today().year -20)])
        self.comboBox.setCurrentIndex(5)
        self.comboBox_2.setItemDelegate(delegate)
        self.comboBox_2.addItems(['Normal','Jahresübersicht','Kumulativ','Durchschnitt Bestellung','Vergleich'])
        self.comboBox_2.setCurrentIndex(0)


        # print(self.bm)
        # print(self.df)

        # print(self.df['date'],self.df['total_value'])
        # print(pd.to_datetime(self.df['date']))



        # print(df)
        # self.df = self.df.iloc[80:].reset_index(drop=True)

        # self.plt_df = self.df
        self.refresh()
        self.create_plot()


    def d_plot(self):
        x = 1
        print(self.threed_plts)
        fig = plt.figure()
        for key in list(self.threed_plts.keys()):
            print(key)
            df = self.threed_plts[key]
            df = df.sort_values('year',ascending=True).reset_index(drop=True)

            ax = fig.add_subplot(1, len(list(self.threed_plts.keys())), x, projection='3d')
            ax.plot_trisurf(df.month, df.year, df.EUR_sum, cmap=cm.jet, linewidth=0.2)
            ax.set_ylim(df.tail(1).reset_index(drop=True)['year'][0],df.year.loc[0])
            print(reversed(pd.unique(df['year'])))
            lst =list(reversed(pd.unique(df['year'])))[::2]
            ax.set_yticks(lst)
            ax.set_title(key)


            x+=1

        fig.tight_layout()
        plt.show()



    def create_plot(self):





        for i in reversed(range(self.verticalLayout.count())):
            self.verticalLayout.itemAt(i).widget().setParent(None)

        df = self.df
        df1 = self.df1


        datum = self.comboBox.currentText().split('-')[1]
        if self.comboBox_2.currentText() == 'Jahresübersicht':
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
        # print(df1.tail())
        df1['year'] = df1['Periode'].dt.year
        df1['month'] = 0

        df_pr = df1.loc[df1['Preisgruppe'] == 1]
        df_pa = df1.loc[df1['Preisgruppe'] == 2]
        df_ges = df1
        self.df_pr = df_pr
        self.df_pa = df_pa
        self.df_ges = df_ges


        if self.comboBox_2.currentText() == 'Vergleich':

            df_pr = df_pr.groupby('Periode')['EUR_sum'].sum().reset_index().rename(columns={'EUR_sum':'Privat'})
            df_pa = df_pa.groupby('Periode')['EUR_sum'].sum().reset_index().rename(columns={'EUR_sum':'Partner'})
            df_merge = df_pa.merge(df_pr,on='Periode').reset_index(drop=True)
            df_merge['sum'] = df_merge['Privat'] + df_merge['Partner']
            df_merge['Pr%'] = df_merge['Privat']/df_merge['sum']
            df_merge['Pa%'] = df_merge['Partner'] / df_merge['sum']

            df_merge['Pr%'] = df_merge['Pr%'].rolling(window=12).mean()
            df_merge['Pa%'] = df_merge['Pa%'].rolling(window=12).mean()
            df_merge = df_merge.loc[df_merge['Pr%'] > 0].reset_index(drop=True)


            dates = df_merge['Periode']
            date_axis = pg.graphicsItems.DateAxisItem.DateAxisItem(orientation='bottom')
            self.graphWidget = pg.PlotWidget(axisItems={'bottom': date_axis})
            self.verticalLayout.addWidget(self.graphWidget)
            self.graphWidget.addLegend()
            df_merge = df_merge[['Periode','Pr%','Pa%']].rename(columns={'Pr%':'Privat','Pa%':'Partner'})
            df_merge.reindex(df_merge.mean().sort_values().index, axis=1)

            df_merge['sum'] = 1
            col = ['g', 'y', 'b', 'w']
            x = 0

            for c in list(df_merge)[1:-1]:  # list(reversed(list(df1)))[1:-1]:
                if x != 0:
                    df_merge['sum'] = df_merge['sum'] - df_merge[list(df_merge)[x]]
                print(c)

                self.graphWidget.plot(dates.values.astype(np.int64) // 10 ** 9, df_merge['sum'], fillLevel=0, name=c,
                                      fillBrush=col[x], pen=col[x])

                x += 1

            self.graphWidget.showGrid(x=True, y=True)
            self.graphWidget.addLine(x=None, y=0, pen=pg.mkPen('r', width=3))
            self.graphWidget.sizeHint = lambda: pg.QtCore.QSize(100, 100)
            if self.dark_mode != 'True':
                self.graphWidget.setBackground('w')
            return






        elif self.comboBox_2.currentText() == 'Jahresübersicht':

            annual_ges = [df1[df1['year'] == y] for y in df1['year'].unique()]

            annual_pr = [df_pr[df_pr['year'] == y] for y in df_pr['year'].unique()]
            annual_pa = [df_pa[df_pa['year'] == y] for y in df_pa['year'].unique()]
            # print(annaul_pr)
            x = 0
            for i in annual_ges:
                annual_ges[x] = i.groupby('Periode')['EUR_sum'].sum().reset_index()
                annual_ges[x]['month'] = annual_ges[x]['Periode'].dt.month
                annual_ges[x]['year'] = annual_ges[x]['Periode'].dt.year
                # print(annaul_ges[x].tail(20))

                x += 1

            x = 0
            for i in annual_pr:
                annual_pr[x] = i.groupby('Periode')['EUR_sum'].sum().reset_index()
                annual_pr[x]['month'] = annual_pr[x]['Periode'].dt.month
                annual_pr[x]['year'] = annual_pr[x]['Periode'].dt.year
                # print(annual_pr[x].tail(20))

                x += 1

            # print(annaul_pr)
            x = 0

            for i in annual_pa:
                annual_pa[x] = i.groupby('Periode')['EUR_sum'].sum().reset_index()
                annual_pa[x]['month'] = annual_pa[x]['Periode'].dt.month
                annual_pa[x]['year'] = annual_pa[x]['Periode'].dt.year
                print(annual_pa[x].tail(20))




                x += 1







            dic = {self.checkBox_2:[annual_ges,'Gesamt'],self.checkBox_3:[annual_pr,'Privat'],self.checkBox_4:[annual_pa,'Partner']}
        else:
            df_pr = df_pr
            df_pa = df_pa
            df_ges = df1
            dic = {self.checkBox_2: [df_ges, 'Gesamt'], self.checkBox_3: [df_pr, 'Privat'],
                   self.checkBox_4: [df_pa, 'Partner']}

        self.threed_plts = {}
        for k in dic.keys():


            if k.isChecked()==True:
                MA_win = 24
                lbl = QLabel()
                lbl.setText(dic[k][1])
                lbl.setAlignment(Qt.AlignCenter)
                self.verticalLayout.addWidget(lbl)
                if self.comboBox_2.currentText() == 'Normal':



                    self.plt_df = dic[k][0].groupby('Periode')['EUR_sum'].sum().reset_index()



                    dates = self.plt_df['Periode']
                    date_axis = pg.graphicsItems.DateAxisItem.DateAxisItem(orientation='bottom')
                    self.graphWidget = pg.PlotWidget(axisItems = {'bottom': date_axis})
                    self.verticalLayout.addWidget(self.graphWidget,0)
                    self.graphWidget.addLegend()
                    self.graphWidget.plot(dates.values.astype(np.int64) // 10 ** 9, self.plt_df['EUR_sum'],pen = pg.mkPen(self.main_col, width=5))
                    self.graphWidget.showGrid(x=True,y=True)
                    self.graphWidget.addLine(x=None, y=0, pen=pg.mkPen('r', width=3))
                    self.graphWidget.sizeHint = lambda: pg.QtCore.QSize(100, 100)

                    self.plt_df['MA'] = self.plt_df['EUR_sum'].rolling(window=MA_win).mean()
                    self.graphWidget.plot(dates.values.astype(np.int64) // 10 ** 9, self.plt_df['MA'],
                                          pen=pg.mkPen('g', width=5),name = str(MA_win)+"MO MA")

                elif self.comboBox_2.currentText() == 'Jahresübersicht':
                    self.graphWidget = pg.PlotWidget()
                    self.verticalLayout.addWidget(self.graphWidget, 0)
                    self.graphWidget.addLegend()
                    ges_df = pd.DataFrame()
                    for i in dic[k][0]:
                        ges_df = ges_df.append(i)
                    self.threed_plts[dic[k][1]]=ges_df

                    for i in dic[k][0][0:-2]:
                        self.graphWidget.plot(i['month'], i['EUR_sum'],)

                    self.graphWidget.plot(dic[k][0][-2]['month'], dic[k][0][-2]['EUR_sum'], pen=pg.mkPen('b', width=5),name = dt.today().year - 1)
                    self.graphWidget.plot(dic[k][0][-1]['month'], dic[k][0][-1]['EUR_sum'], pen=pg.mkPen('g', width=7),name = dt.today().year)
                    self.graphWidget.showGrid(x=True,y=True)
                    self.graphWidget.addLine(x=None, y=0, pen=pg.mkPen('r', width=3))
                    self.graphWidget.sizeHint = lambda: pg.QtCore.QSize(100, 100)
                elif self.comboBox_2.currentText() == 'Kumulativ':



                    self.plt_df = dic[k][0].groupby('Periode')['EUR_sum'].sum().reset_index()
                    self.plt_df['r_sum'] = self.plt_df['EUR_sum'].expanding(2).sum()


                    dates = self.plt_df['Periode']
                    date_axis = pg.graphicsItems.DateAxisItem.DateAxisItem(orientation='bottom')
                    self.graphWidget = pg.PlotWidget(axisItems = {'bottom': date_axis})
                    self.verticalLayout.addWidget(self.graphWidget,0)
                    self.graphWidget.addLegend()
                    self.graphWidget.plot(dates.values.astype(np.int64) // 10 ** 9, self.plt_df['r_sum'],pen = pg.mkPen(self.main_col, width=5))
                    self.graphWidget.showGrid(x=True,y=True)
                    self.graphWidget.addLine(x=None, y=0, pen=pg.mkPen('r', width=3))
                    self.graphWidget.sizeHint = lambda: pg.QtCore.QSize(100, 100)
                elif self.comboBox_2.currentText() == 'Durchschnitt Bestellung':



                    self.plt_df = dic[k][0]
                    print(self.plt_df.tail())
                    self.plt_df = self.plt_df.groupby('Periode')['EUR_sum'].mean().reset_index()
                    print(self.plt_df.tail())


                    dates = self.plt_df['Periode']
                    date_axis = pg.graphicsItems.DateAxisItem.DateAxisItem(orientation='bottom')
                    self.graphWidget = pg.PlotWidget(axisItems = {'bottom': date_axis})
                    self.verticalLayout.addWidget(self.graphWidget,0)
                    self.graphWidget.addLegend()
                    self.graphWidget.plot(dates.values.astype(np.int64) // 10 ** 9, self.plt_df['EUR_sum'],pen = pg.mkPen(self.main_col, width=5))
                    self.graphWidget.showGrid(x=True,y=True)
                    self.graphWidget.addLine(x=None, y=0, pen=pg.mkPen('r', width=3))
                    self.graphWidget.sizeHint = lambda: pg.QtCore.QSize(100, 100)

                    self.plt_df['MA'] = self.plt_df['EUR_sum'].rolling(window=MA_win).mean()
                    self.graphWidget.plot(dates.values.astype(np.int64) // 10 ** 9, self.plt_df['MA'], pen=pg.mkPen('g', width=5),name = str(MA_win)+"MO MA")
                if self.dark_mode != 'True':
                    self.graphWidget.setBackground('w')



                # bm_date = self.bm['Date'].reset_index(drop=True)
                # print(dates,bm_date)
                # if self.bm_ex != False:
                #     self.graphWidget.plot(dates.values.astype(np.int64) // 10 ** 9,self.plt_df['cum_pct_change_bm']*100, pen=pg.mkPen('b', width=2),name = 'SPY')

                # self.graphWidget.addLine(x=None, y=self.df['cum_pct_change'].iloc[-1]*100, pen=pg.mkPen('b', width=1))
                # print(self.plt_df.tail())



    def refresh(self):
        for i in reversed(range(self.verticalLayout_2.count())):
            self.verticalLayout_2.itemAt(i).widget().setParent(None)


        if self.comboBox_2.currentText() == 'Jahresübersicht':
            self.Button_1 = QPushButton("3D")
            self.verticalLayout_2.addWidget(self.Button_1)
            self.Button_1.clicked.connect(self.d_plot)


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











def preisgruppenGUI(data):
    app = QApplication(sys.argv) #instantiate a QtGui (holder for the app)
    # app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    window = MyApp1(data)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    import load_data
    data = load_data.tabellen_zusamenfuegen()[1:3]
    preisgruppenGUI(data)
