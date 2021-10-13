import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime as dt
from datetime import timedelta
import csv
import codecs
import json
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.3f' % x)
from configparser import ConfigParser
config = ConfigParser()
config.read('config.ini')
path_db = config.get('main', 'path_db')




path_kunden = path_db+'/Kunden.txt'

path_adressen = path_db+'/Adressen.txt'

path_umsatz = path_db+'/Umsatz_Kunden.txt'

# path_kunden = '/Volumes/LaCie/HDD SynDrive/Geschaeftsfuerung/IT/4D/4D Export/27.09.21/kunden01.txt'
# path_adressen = '/Volumes/LaCie/HDD SynDrive/Geschaeftsfuerung/IT/4D/4D Export/27.09.21/adressen01.txt'
# path_kunden = '/Volumes/LaCie/HDD SynDrive/Geschaeftsfuerung/IT/4D/4D Export/Datenbank-Export/4D-Datenbankexport/Kunden.txt'
# path_adressen = '/Volumes/LaCie/HDD SynDrive/Geschaeftsfuerung/IT/4D/4D Export/Datenbank-Export/4D-Datenbankexport/Adressen.txt'



def tabellen_zusamenfuegen(p1 = path_kunden,p2 = path_adressen,p3= path_umsatz):

    # print(p1)


    data = json.load(codecs.open(p1, 'r', 'utf-8-sig'))
    df1 = pd.DataFrame(data)
    data = json.load(codecs.open(p2, 'r', 'utf-8-sig'))
    df2 = pd.DataFrame(data)
    data = json.load(codecs.open(p3, 'r', 'utf-8-sig'))
    df3 = pd.DataFrame(data)
    # print(df1.head())



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




    # print(merge_1.head(1))
    # print(merge_1)
    df = pd.merge(merge_1,df3,on= 'KundenNr')
    df_ = pd.merge(df, df4, on='KundenNr')
    df_main = pd.merge(df_,df6,on='KundenNr')
    # print(df_main.head())
    df = df_main[['KundenNr','Anrede','Vorname','Name1','Name2','Strasse','Land','PLZ','Ort','Ansprechp','Briefanrede','Telefon','Fax','AufnahmeDatum','Preisgruppe_x','Kundengr','e_Mail','WWW_Adr','Werbung','E_Werbung','WWW_Adr','AdrNr','letzteLieferung','EUR_sum','EUR_mean','Orders','Hausnummer']]
    # print(df.head())
    df = df.rename(columns={'Preisgruppe_x':'Preisgruppe'})
    # df['letzteLieferung'] = pd.to_datetime(df['letzteLieferung'],errors='coerce')
    # print(df.head(50))

    df['Preisgruppe'] = df['Preisgruppe'].astype(int)
    # df = df.applymap(lambda x: x.encode('unicode_escape').
    #              decode('utf-8') if isinstance(x, str) else x)
    # print(df.head())
    return [simple_merge,df,df_purchases]




def export_kunden(df):


    # print(df.head())

    file_name = 'kunden_p_Ausland' #.csv


#     Filter



    keine_werbung = True # False : Keine Filter, True: Werbung erlaubt oder NA

    keine_email =False # False : Keine Filter, True: Werbung erlaubt oder NA

    datum_aufgenommen_ab = False #deaktivieren durch False

    datum_letzte_bestellung_ab = '01.01.2018' # deaktivieren durch False

    preisgruppe = 1  #0 = beide, 1 = privat,2= handel

    land = 'Ausland'

    welche_columns = ['KundenNr','Vorname','Name1','Name2','Strasse','Land','PLZ','Ort']   # deaktivieren durch False

    # sortierung


    sort = 'Land' #['Land','AufnahmeDatum','letzteLieferung']  deaktivieren durch False

    #If sort == Land:
    nach_plz = True

    # print(df.head())

    df['AufnahmeDatum'] = pd.to_datetime(df['AufnahmeDatum'], format='%Y-%m-%d', errors='coerce')
    df['letzteLieferung'] =pd.to_datetime(df['letzteLieferung'], format='%Y-%m-%d', errors='coerce')

    # df['AufnahmeDatum'] = pd.to_datetime(df['AufnahmeDatum'], format='%d.%m.%y', errors='coerce')
    # df['letzteLieferung'] =pd.to_datetime(df['letzteLieferung'], format='%d.%m.%y', errors='coerce')



    # print(len(df),df.head())
    # df['AufnahmeDatum'] = pd.to_datetime(df['AufnahmeDatum'], format='%d.%m.%Y', errors='coerce')
    # df['letzteLieferung'] =pd.to_datetime(df['letzteLieferung'], format='%d.%m.%Y', errors='coerce')

    # print(df.sort_values(['AufnahmeDatum']))
    print(len(df))
    print(df.head())
    if keine_werbung == True:
        df = df[df['Werbung']!=1]
    print(len(df))
    if keine_email == True:
        df = df[df['E_Werbung']!=1]
    print(len(df))
    if datum_aufgenommen_ab != False:
        df = df[df['AufnahmeDatum']>=dt.strptime(datum_aufgenommen_ab,'%d.%m.%Y')]
    print(len(df))
    if datum_letzte_bestellung_ab != False:
        df = df[df['letzteLieferung']>=dt.strptime(datum_letzte_bestellung_ab,'%d.%m.%Y')]
    print(len(df))
    if preisgruppe != 0 :
        df = df[df['Preisgruppe']==preisgruppe]
    print(len(df))
    if land != False and land != 'Inland'and land != 'Ausland':
        df = df[df['Land']==land]
    elif land == 'Inland':
        df = df[df['Land'] == 'DE']
    elif land == 'Ausland':
        df = df[df['Land'] != 'DE']
    #Sorting
    if sort == 'Land' and nach_plz == True:

        df = df.sort_values(['Land', 'PLZ'])

    elif sort != False:
        df = df.sort_values([sort],ascending=False)


    df = df.reset_index(drop=True)


    if welche_columns != False:
        df = df[welche_columns]





    df['Land'] = df.Land.replace( 'DE','')

    df['plz_ort'] = df['PLZ']+' '+df['Ort']
    df['Name'] = df['Vorname'] + ' ' + df['Name1']
    print(df.head(), len(df))

    df.to_csv('/Users/joan/Desktop/WSZ/'+ file_name + '.csv',index=False,encoding = 'utf-8-sig')



if __name__ == '__main__':
    t1 = dt.now()
    simple_merge,df_gesamt,df_purchases = tabellen_zusamenfuegen()
    # analyse_privat_handel(df_gesamt,df_purchases)
    print(df_gesamt.tail())
    print(dt.now()-t1)
    # print(df_gesamt.head(20))
    # print(len(df_gesamt))
    # export_kunden(df_gesamt)
    # print(df_gesamt.head())
    # purchase_plts(df_purchases,df_gesamt)
    # country_plts(df_purchases,df_gesamt)
    # draw_plts(df_gesamt)

