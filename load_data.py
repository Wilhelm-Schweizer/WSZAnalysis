import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime as dt
from datetime import timedelta
import csv
import codecs
import json
pd.options.display.width = 0
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.3f' % x)

from os import path

path_db = 'W:'

# path_kunden = path_db+'/Kunden.txt'
#
# path_adressen = path_db+'/Adressen.txt'
#
# path_umsatz = path_db+'/Umsatz_Kunden.txt'
# path_werk = path_db+'/WerksauftrPos.txt'
# path_belegepos = path_db + '/Belege_Pos.txt'
# # path_belegepos ='/Volumes/LaCie/HDD SynDrive/Geschaeftsfuerung/IT/4D/4D Export/TEST/Belege_Pos.txt'
# path_belege = path_db + '/Belege.txt'
# path_kunden = '/Volumes/LaCie/HDD SynDrive/Geschaeftsfuerung/IT/4D/4D Export/27.09.21/kunden01.txt'
# path_adressen = '/Volumes/LaCie/HDD SynDrive/Geschaeftsfuerung/IT/4D/4D Export/27.09.21/adressen01.txt'
# path_kunden = '/Volumes/LaCie/HDD SynDrive/Geschaeftsfuerung/IT/4D/4D Export/Datenbank-Export/4D-Datenbankexport/Kunden.txt'
# path_adressen = '/Volumes/LaCie/HDD SynDrive/Geschaeftsfuerung/IT/4D/4D Export/Datenbank-Export/4D-Datenbankexport/Adressen.txt'








def vertrieb(path_db=path_db):

    # print(p1)
    p = path.join(path_db ,'Vertrieb')

    p1 = path.join(p , 'Kunden.txt')
    p2 = path.join(p , 'Adressen.txt')
    p3 = path.join(p , 'Umsatz_Kunden.txt')
    p4 = path.join(p , 'Belege.txt')
    p5 = path.join(p, 'Belege_Pos_short.csv')
    print(p1)
    path_mwst = path.join(p, 'EU_MWST.csv')
    try:
        data = json.load(codecs.open(p1, 'r', 'utf-8-sig'))
        df1 = pd.DataFrame(data)
    except:

        return False




    data = json.load(codecs.open(p2, 'r', 'utf-8-sig'))
    df2 = pd.DataFrame(data)
    data = json.load(codecs.open(p3, 'r', 'utf-8-sig'))
    df3 = pd.DataFrame(data)
    data = json.load(codecs.open(p4, 'r', 'utf-8-sig'))
    df4 = pd.DataFrame(data)
    # data = json.load(codecs.open(p5, 'r', 'utf-8-sig'))
    df5 = pd.read_csv(p5)
    mwst = pd.read_csv(path_mwst)[['Land', 'mwst']]
    # print(df1.head())
    # print(df4.head())
    # print(df5.head())



    # df5 = df5.tail(500000)
    # df5.to_json('/Volumes/LaCie/HDD SynDrive/Geschaeftsfuerung/IT/4D/4D Export/TEST/Belege_Pos.txt')



    df4 = df4[['Papierart','PapierNr','KundenNr','Datum','ID','Endbetrag','Anzahl_Teile','Zahlungsart_A','Preisgruppe']]
    df4['PapierNr'] = df4['PapierNr'].astype(int)
    df5 =df5[['AbsNr','ArtNr','Bezeichnung','Menge','Preis','Pos Betrag']]

    df4 = df4.rename(columns={'ID':'ID_MATCH'})
    df5 = df5.rename(columns={'AbsNr': 'ID_MATCH'})

    df_purch_pos = df5.merge(df4,on = 'ID_MATCH',how = 'left')

    df_purch_pos['%_endbetrag'] = df_purch_pos['Pos Betrag']/df_purch_pos['Endbetrag']
    df_purch_pos['%_teile'] = df_purch_pos['Menge']/df_purch_pos['Anzahl_Teile']
    df_purch_pos = df_purch_pos.loc[df_purch_pos['Menge']>0]
    #df_purch_pos['Datum'] = pd.to_datetime(df_purch_pos['Datum'],errors='coerce')
    df4 = df4.tail(15000).reset_index(drop=True)





    # print(df_purch_pos.tail(10))



    # df1 = pd.read_csv(p1,delimiter="\t", quoting=csv.QUOTE_NONE, error_bad_lines=False)
    # df2 = pd.read_csv(p2,delimiter="\t", quoting=csv.QUOTE_NONE, error_bad_lines=False)
    # df3 = pd.read_csv(p3,delimiter="\t")

    # print(df1)

    # print(len(df1),len(df2))

    df_purchases = df3
    df4 = df3
    df5 = df3
    # print(df3.head())
    df3['EUR_sum'] = df3['EUR']
    # df3['EUR_sum'] = df3['EUR'].str.replace(',', '.')
    df3 =df3.astype({'EUR_sum': 'float'})
    # print(df3)
    df3 =df3.groupby('KundenNr')['EUR_sum'].sum()

    # print(df3)
    df4['EUR_mean'] = df4['EUR']
    # df4['EUR_mean'] = df4['EUR'].str.replace(',', '.')
    df4 =df4.astype({'EUR_mean': 'float'})
    # print(df3)
    df4 =df4.groupby('KundenNr')['EUR_mean'].mean()


    # print(df3)
    df6 =df5.groupby('KundenNr').size().reset_index(name='Orders')


    # print(df6.head(50))



    # print(df1,df2,df3)

    # print(df3)
    merge_1 = pd.merge(df1,df2,on='AdrNr',how = 'left')
    merge_1['Land'] = merge_1.Land.replace('', 'DE')
    # print(len(df1),len(df2),len(merge_1))
    simple_merge = merge_1




    df = pd.merge(merge_1,df3,on= 'KundenNr')

    df_ = pd.merge(df, df4, on='KundenNr')
    df_main = pd.merge(df_,df6,on='KundenNr')
    # print(df_main.head())
    df = df_main[['KundenNr','Anrede','Vorname','Name1','Name2','Strasse','Land','PLZ','Ort','Ansprechp','Briefanrede','Telefon','Fax','AufnahmeDatum','Preisgruppe_x','Kundengr','e_Mail','WWW_Adr','Werbung','E_Werbung','WWW_Adr','AdrNr','letzteLieferung','EUR_sum','EUR_mean','Orders','Hausnummer']]
    # print(df.head())
    # print(df.loc[df['KundenNr']== '17957610'])
    df = pd.merge(df,mwst,on='Land',how = 'left')
    df = df.rename(columns={'Preisgruppe_x':'Preisgruppe'})
    # print(df.loc[df['KundenNr']== '17957610'])
    # df['letzteLieferung'] = pd.to_datetime(df['letzteLieferung'],errors='coerce')
    # print(df.head(50))

    df['Preisgruppe'] = df['Preisgruppe'].astype(int)



    # df = df.applymap(lambda x: x.encode('unicode_escape').
    #              decode('utf-8') if isinstance(x, str) else x)

    # print(df.loc[df['KundenNr']== '17957610'])
    df.loc[df['Preisgruppe']==2,['mwst']] = ""
    df['AufnahmeDatum'] = pd.to_datetime(df['AufnahmeDatum'], format='%Y-%m-%d', errors='coerce')
    df['letzteLieferung'] = pd.to_datetime(df['letzteLieferung'], format='%Y-%m-%d', errors='coerce')
    return [simple_merge, df, df_purchases,df_purch_pos]

def produktion(path_db=path_db):

    p = path.join(path_db, 'Produktion')

    p1 = path.join(p, 'WerksauftrPos.txt')
    p2 = path.join(p, 'Stueckzeiten.txt')
    p3 = path.join(p, 'Personal.txt')

    try:
        data = json.load(codecs.open(p1, 'r', 'utf-8-sig'))
        df_werk = pd.DataFrame(data)

    except:

        return False

    data = json.load(codecs.open(p2, 'r', 'utf-8-sig'))
    df_zeit = pd.DataFrame(data)
    data = json.load(codecs.open(p3, 'r', 'utf-8-sig'))
    df_pers = pd.DataFrame(data)[['Pers_Nr','Vorname','Name','Std_Satz','ausgeschieden']] #['Pers_Nr','Vorname','Name','Std_Satz','ausgeschieden']
    df_pers['Name'] = df_pers['Vorname'] + ' ' + df_pers['Name']
    print(df_pers.head())
    df_werk['Datum_begin'] = pd.to_datetime(df_werk['Datum_begin'], format='%Y-%m-%d', errors='coerce').dropna()
    merge = df_werk.merge(df_zeit,on='WAP_Nr',how='left')
    merge=merge.rename(columns={'Pers__Nr':'Pers_Nr'})
    merge=merge.merge(df_pers,on='Pers_Nr',how='left')
    merge['Name'] = merge['Name'] +' ('+ merge['Pers_Nr'].dropna().astype(int).astype(str) +')'
    print(merge.head())
    return [merge]
produktion()


def finanzen(path_db=path_db):

    p = path.join(path_db, 'Finanzen')

    p1 = path.join(p, 'IncomeStatement\Monthly.csv')

    try:
        df_is = pd.read_csv(p1)
    except:

        return False
    #print(df_is.head(10))
    return [df_is]





if __name__ == '__main__':
    t1 = dt.now()
    simple_merge,df_gesamt,df_purchases,df_purch = vertrieb()
    # analyse_privat_handel(df_gesamt,df_purchases)
    # df= df_gesamt.loc[df_gesamt['Preisgruppe']==2].sort_values('letzteLieferung',ascending = True).reset_index(drop=True)
    # df = df.loc[df['letzteLieferung']>dt.strptime('2018','%Y')]
    # df.to_csv('/Volumes/LaCie/HDD SynDrive/Vertrieb/Kunden Exports/Karte/kunden_partner.csv', index=False, encoding='utf-8-sig')
    # print(df.head(),len(df))
    print(dt.now()-t1)
    # print(df_gesamt.head(20))
    # print(len(df_gesamt))
    # export_kunden(df_gesamt)
    # print(df_gesamt.head())
    # purchase_plts(df_purchases,df_gesamt)
    # country_plts(df_purchases,df_gesamt)
    # draw_plts(df_gesamt)

    # art = '115115-BE'
    #
    # df_purch = df_purch.loc[df_purch['Papierart'] == 'R']
    # df_purch = df_purch.loc[df_purch['ArtNr']==art].reset_index(drop=True)
    #
    #
    # print(df_purch.head(10))
    # df_purch['month_year'] = df_purch['Datum'].dt.to_period('M')
    # df_purch = df_purch.groupby('month_year')['Menge'].sum().reset_index()
    #
    # print(df_purch)
    # # plt.plot(df_purch['Menge'])
    # # plt.xticklabels(df_purch['Datum'])
    # # plt.show()
    #
    # fig, ax = plt.subplots(1, 1)
    # ax.plot(df_purch.index,df_purch['Menge'])
    # ax.set_xticks(df_purch.index)
    # ax.set_xticklabels(df_purch['month_year'])
    # plt.xticks(rotation=70)
    # plt.title(art)
    # plt.tight_layout()
    #
    # plt.show()



    df_purch = df_purch.loc[df_purch['Papierart'] == 'R']
    df_purch = df_purch.loc[df_purch['Preisgruppe'] == 1]
    df_purch = df_purch.merge(df_gesamt,on='KundenNr',).reset_index(drop=True)
    df_purch = df_purch.drop_duplicates(['PapierNr'])
    # df_purch = df_purch.groupby(['PapierNr'])['Pos Betrag'].sum()
    #
    # # l = df_purch['Land'].unique()
    df_purch = df_purch.loc[df_purch['Datum']>dt.strptime('2020-01','%Y-%m')]
    df_purch = df_purch.loc[df_purch['Datum'] < dt.strptime('2021-01', '%Y-%m')]
    l = [ 'FR', 'IT', 'AT', 'ES', 'DK', 'NL','LI', 'IE', 'LU','PL', 'BE','SE', 'CZ','FI','PT', 'MT','ME','LV']
    # df_purch=df_purch.loc[df_purch['Land'].isin(l)].reset_index(drop=True)
    rolling = df_purch.groupby(['Datum'])['Endbetrag'].sum().reset_index()
    rolling['rolling'] = rolling['Endbetrag'].expanding(2).sum()
    df_purch = df_purch[['Datum','Papierart','PapierNr','KundenNr','Endbetrag','Kundengr','Land']]
    print(df_purch.tail(5))
    # df_purch.to_csv('/Volumes/LaCie/HDD SynDrive/Buchhaltung/Auswertungen/Bestellungen EU Ausland/2021.csv',index=False)
    # print(rolling)

    plt.plot(rolling['Datum'],rolling['rolling'])
    plt.axhline(10000,color='r')
    plt.title('2021')
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.show()


    # lander = df_purch.groupby(['Land'])['Pos Betrag'].sum().sort_values().reset_index()
    # print(lander,df_purch['Pos Betrag'].sum())
    #
    # plt.bar(lander['Land'],lander['Pos Betrag'])
    # plt.title('2020-Jetzt Gesamt: '+str(round(df_purch['Pos Betrag'].sum(),2)))
    # plt.show()
    #
    #
    #
    #
    # print(df_purch.tail())
    # print(l)
    #
    # df = df_gesamt.loc[df_gesamt['letzteLieferung']>dt.strptime('2018-01','%Y-%m')].sort_values('letzteLieferung')
    # df = df.loc[df['Preisgruppe'] == 1]
    # df = df.loc[df['Werbung'] != 1]
    # df=df.loc[~df['Land'].isin(l)].reset_index(drop=True)
    # lander = df.groupby(['Land']).size().sort_values()
    # print(df.tail())
    # print(lander,lander.sum())