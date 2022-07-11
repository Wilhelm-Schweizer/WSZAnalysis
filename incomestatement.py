
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic
import qdarkstyle
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.3f' % x)
from datetime import date
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg
import numpy as np

from datetime import datetime as dt
from datetime import timedelta
from configparser import ConfigParser
from statistics import mean
import sys,os
os.environ['QT_MAC_WANTS_LAYER'] = '1'


from pg_stats import MyApp1 as pg_stats
import random

# config = ConfigParser()
# config.read('config.ini')
#




class CustomAxisItem(pg.AxisItem):

    def tickStrings(self, values, scale, spacing):
        if self.logMode:
            return self.logTickStrings(values, scale, spacing)

        places = max(0, np.ceil(-np.log10(spacing*scale)))
        strings = []
        for v in values:
            vs = v * scale
            vstr = ("%%0.%df" % places) % vs
            strings.append(vstr)
        return strings




# dark_mode = config.get('main', 'dark_mode')



# import pyqtgraph.examples
# pyqtgraph.examples.run()
# path = os.path.dirname(__file__) #uic paths from itself, not the active dir, so path needed
# qtCreatorFile = "GUI_Files/lander.ui" #Ui file name, from QtDesigner, assumes in same folder as this .py
#
# Ui_Error, QtBaseClass = uic.loadUiType(qtCreatorFile) #process through pyuic
from GUI_Files.incomestatement import Ui_Incomestatement
class MyApp1(QMainWindow, Ui_Incomestatement): #gui class
    def __init__(self,data):
        #The following sets up the gui via Qt
        super(MyApp1, self).__init__()
        self.df = data[0]

        import random

        print(self.df)
        self.df = self.df.loc[self.df['Gesamtkosten'] > 20000 ]
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
        self.dark_mode = False
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
        self.comboBox_3.addItems(['Normal','Jahresübersicht','Pro Jahr','Pro Quartal','Vergleich Quartale'])
        self.comboBox_3.setCurrentIndex(0)

        # print(data[0]['Land'].unique().tolist())
        self.comboBox_2.setItemDelegate(delegate)
        l = list(self.df)
        print(l)
        l = ['Uebersicht'] + l
        self.comboBox_2.addItems(l)
        self.comboBox_2.setCurrentIndex(0)


        self.create_plot()



    def create_plot(self):





        for i in reversed(range(self.verticalLayout.count())):
            self.verticalLayout.itemAt(i).widget().setParent(None)

        #
        df = self.df

        #
        #
        datum = self.comboBox.currentText().split('-')[1]
        if self.comboBox_3.currentText() == 'Jahresübersicht':
            datum = ' 2000'



        #
        df['Periode'] = pd.to_datetime(df['Date'], format='%Y-%m-%d', errors='coerce')

        df = df[df['Periode'] >= dt.strptime(datum, ' %Y')].reset_index(drop=True)
        df = df[df['Periode'] <= dt.today().replace(day=1) - timedelta(days=1)].reset_index(drop=True)

        # # df1 = df1.tail(100).reset_index(drop=True)
        #

        #




        print(df.tail())


        # print(df1.tail())
        df['year'] = df['Periode'].dt.year
        df['month'] = 0
        plt_df = df
        if self.comboBox_2.currentText() == 'Uebersicht':

            for i in ['Gesamtleistung','Gesamtkosten','Vorl Ergebnis']:

                self.plots(plt_df, i, 1)
        else:
            self.plots(plt_df, self.comboBox_2.currentText(), 1)







    def plots(self,plt_df,fig,i):
        layout = self.verticalLayout


        lbl = QLabel()
        lbl.setText(fig)
        lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl)
        MA_win = 24



        if self.comboBox_3.currentText() == 'Normal':





            dates = plt_df['Periode']
            date_axis = pg.graphicsItems.DateAxisItem.DateAxisItem(orientation='bottom')
            self.graphWidget = pg.PlotWidget(axisItems = {'bottom': date_axis})
            layout.addWidget(self.graphWidget)
            self.graphWidget.addLegend()
            self.graphWidget.plot(dates.values.astype(np.int64) // 10 ** 9, plt_df[fig],pen = pg.mkPen(self.main_col, width=5))
            self.graphWidget.showGrid(x=True,y=True)
            self.graphWidget.addLine(x=None, y=0, pen=pg.mkPen('r', width=3))
            self.graphWidget.sizeHint = lambda: pg.QtCore.QSize(100, 100)

            plt_df['MA'] = plt_df[fig].rolling(window=MA_win).mean()
            self.graphWidget.plot(dates.values.astype(np.int64) // 10 ** 9, plt_df['MA'],
                                  pen=pg.mkPen('g', width=5), name=str(MA_win) + "MO MA")

        # elif self.comboBox_3.currentText() == 'Kumulativ':
        #     plt_df = df.loc[df['ArtNr'] == fig]
        #     plt_df = plt_df.groupby('Periode')[mode].sum().reset_index()
        #     plt_df['r_sum'] = plt_df[mode].expanding(2).sum()
        #     dates = plt_df['Periode']
        #     date_axis = pg.graphicsItems.DateAxisItem.DateAxisItem(orientation='bottom')
        #     self.graphWidget = pg.PlotWidget(axisItems={'bottom': date_axis})
        #     layout.addWidget(self.graphWidget)
        #     self.graphWidget.addLegend()
        #     self.graphWidget.plot(dates.values.astype(np.int64) // 10 ** 9, plt_df['r_sum'],
        #                           name=fig, stepmode=True, fillLevel=0, fillOutline=True,pen = pg.mkPen(self.main_col, width=5))
        #     self.graphWidget.showGrid(x=True, y=True)
        #     self.graphWidget.addLine(x=None, y=0, pen=pg.mkPen('r', width=3))
        #     self.graphWidget.sizeHint = lambda: pg.QtCore.QSize(100, 100)
        # elif self.comboBox_3.currentText() == 'Durchschnitt Bestellung':
        #     plt_df = df.loc[df['ArtNr'] == fig]
        #
        #     plt_df = plt_df.groupby('Periode')[mode].mean().reset_index()
        #
        #     dates = plt_df['Periode']
        #     date_axis = pg.graphicsItems.DateAxisItem.DateAxisItem(orientation='bottom')
        #     self.graphWidget = pg.PlotWidget(axisItems={'bottom': date_axis})
        #     layout.addWidget(self.graphWidget)
        #     self.graphWidget.addLegend()
        #     self.graphWidget.plot(dates.values.astype(np.int64) // 10 ** 9, plt_df[mode], stepmode=True, fillLevel=0, fillOutline=True,pen = pg.mkPen(self.main_col, width=5) )
        #     self.graphWidget.showGrid(x=True, y=True)
        #     self.graphWidget.addLine(x=None, y=0, pen=pg.mkPen('r', width=3))
        #     self.graphWidget.sizeHint = lambda: pg.QtCore.QSize(100, 100)
        #
        #     plt_df['MA'] = plt_df[mode].rolling(window=MA_win).mean()
        #     self.graphWidget.plot(dates.values.astype(np.int64) // 10 ** 9, plt_df['MA'],
        #                           pen=pg.mkPen('g', width=5), name=str(MA_win) + "MO MA")
        elif self.comboBox_3.currentText() == 'Jahresübersicht':

            df1 = plt_df[['year','month','Periode',fig]]
            annual = [df1[df1['year'] == y] for y in df1['year'].unique()]


            # print(annaul_pr)
            x = 0
            for i in annual:
                annual[x] = i.groupby('Periode')[fig].sum().reset_index()
                annual[x]['month'] = annual[x]['Periode'].dt.month
                # print(annaul_ges[x].tail(20))

                x += 1

            l = []

            for i in range(1,13):
                dic = {}
                ll = []

                for ii in annual:

                    try:
                        ll.append(ii.loc[ii['month']==i][fig].reset_index(drop=True)[0])
                    except:
                        pass

                ll=mean(ll)
                dic['AVG'] = ll
                dic['month'] = i
                l.append(dic)



            avg = pd.DataFrame(l)
            print(avg)
            self.graphWidget = pg.PlotWidget()
            layout.addWidget(self.graphWidget, 0)
            self.graphWidget.addLegend()
            for i in annual[0:-2]:
                self.graphWidget.plot(i['month'], i[fig],)

            print(annual[-2])
            self.graphWidget.plot(avg.month, avg.AVG, pen=pg.mkPen(self.main_col,width=3),name = 'AVG')
            self.graphWidget.plot(annual[-2]['month'], annual[-2][fig], pen=pg.mkPen('b', width=5),name = annual[-2]['Periode'][0].year)
            self.graphWidget.plot(annual[-1]['month'], annual[-1][fig], pen=pg.mkPen('g', width=7),name = annual[-1]['Periode'][0].year)

            self.graphWidget.showGrid(x=True,y=True)
            self.graphWidget.addLine(x=None, y=0, pen=pg.mkPen('r', width=3))
            self.graphWidget.sizeHint = lambda: pg.QtCore.QSize(100, 100)
        elif self.comboBox_3.currentText() == 'Pro Jahr':

            plt_df = plt_df[plt_df['Periode'] <= dt.today().replace(day=1).replace(month = 1) - timedelta(days=1)].reset_index(drop=True)
            plt_df = plt_df[['year',fig]]
            plt_df= plt_df.groupby('year').sum().reset_index()
            print(plt_df)


           # date_axis = pg.graphicsItems.DateAxisItem.DateAxisItem(orientation='bottom')
            self.graphWidget = pg.PlotWidget()
            self.graphWidget.plotItem.setAxisItems({'left': CustomAxisItem('left')})
            layout.addWidget(self.graphWidget)
            self.graphWidget.addLegend()
            bargraph = pg.BarGraphItem(x = plt_df['year'],height =  plt_df[fig],width = 0.6)
            self.graphWidget.addItem(bargraph)
            self.graphWidget.showGrid(x=True,y=True)
            self.graphWidget.addLine(x=None, y=0, pen=pg.mkPen('r', width=3))
            self.graphWidget.sizeHint = lambda: pg.QtCore.QSize(100, 100)
        elif self.comboBox_3.currentText() == 'Pro Quartal':
            q_start = (date(dt.today().year, 3 * ((dt.today().month - 1) // 3) + 1, 1) - timedelta(days=1)).strftime(format = '%Y-%m-%d')
            q_start=dt.strptime(q_start,'%Y-%m-%d')

            print(q_start)
            plt_df['Date']=pd.to_datetime(plt_df['Date'])
            plt_df = plt_df[plt_df['Date'] <= q_start].reset_index(drop=True)
            plt_df = plt_df[['Date',fig]]

            plt_df=plt_df.groupby(plt_df['Date'].dt.to_period('Q')).sum().reset_index()
            plt_df['Date'] = plt_df['Date'].astype(str)
            print(plt_df)
            xdict = dict(enumerate(plt_df['Date']))
            stringaxis = pg.AxisItem(orientation='bottom')
            stringaxis.setTicks([xdict.items()])

           # date_axis = pg.graphicsItems.DateAxisItem.DateAxisItem(orientation='bottom')
            self.graphWidget = pg.PlotWidget()
            self.graphWidget.plotItem.setAxisItems({'left': CustomAxisItem('left'),'bottom': stringaxis})
            layout.addWidget(self.graphWidget)
            self.graphWidget.addLegend()
            bargraph = pg.BarGraphItem(x = list(xdict.keys()),height =  plt_df[fig],width = 0.6)
            self.graphWidget.addItem(bargraph)
            self.graphWidget.showGrid(x=True,y=True)
            self.graphWidget.addLine(x=None, y=0, pen=pg.mkPen('r', width=3))
            self.graphWidget.getPlotItem().axes['bottom']['item'].setTicks(
                [list(xdict.items())[::4], list(xdict.items())[1::4]])
            self.graphWidget.sizeHint = lambda: pg.QtCore.QSize(100, 100)

        if self.dark_mode != 'True':
            self.graphWidget.setBackground('w')




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











def landerGUI(data):
    app = QApplication(sys.argv) #instantiate a QtGui (holder for the app)
    # app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    window = MyApp1(data)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    import load_data
    data = load_data.finanzen()
    landerGUI(data)
