'''
Created on 02.09.2012

@author: Stefan
'''
from pTool.WebConnect import CWebConnect
from datetime import timedelta, date
import time, libxml2dom

class CFinanzenNet(object):
    
    __webConnect = CWebConnect()


    def __init__(self):
        
        self.__FinanzenNetHistorischeKurseURL = "http://www.finanzen.net/kurse/kurse_historisch.asp"
        self.__POSTData = {'pkAktieNr' : 0,
                          'strBoerse' : '',
                          'dtTag1': 1,
                          'dtMonat1': 7,
                          'dtJahr1' : 2003,
                          'dtTag2': 2,
                          'dtMonat2': 7,
                          'dtJahr2' : 2003
                          }
    
    def __resetState(self):
        self.__AktienkursHeute = 0
        self.__AktienkursVor6Monaten = 0
        self.__AktienkursVor12Monaten = 0
        
        ''' aktuelles datum z.b. 10.9
            letzer monat: dax wert von 29.8 bis 1.9
            vor letzter monat: dax wert von ende juli/anfang august
            vorvorletzter monat: dax wert von ende juni/anfang august
        '''
        self.__DAXLetzterMonat = 0
        self.__DAXVorLetzterMonat = 0
        self.__DAXVorVorLetzterMonat = 0
        
        self.__AktieLetzterMonat = 0
        self.__AktieVorLetzterMonat = 0
        self.__AktieVorVorLetzterMonat = 0
        
    def __getDataforStock(self, stock):
        t1 = date.today()
        t2 = t1 - timedelta(months=13)
        
        self.__POSTData["pkAktieNr"] = stock.FinanztreffId
        self.__POSTData["strBoerse"] = stock.strBoerseFinanzenNet
        
        self.__POSTData["dtTag1"] = t2.day
        self.__POSTData["dtMonat1"] = t2.month
        self.__POSTData["dtJahr1"] = t2.year
        
        self.__POSTData["dtTag2"] = t1.day
        self.__POSTData["dtMonat2"] = t1.month
        self.__POSTData["dtJahr2"] = t1.year
        
        page = self.__webConnect.runPOSTRequest(self.__FinanzenNetHistorischeKurseURL, self.__POSTData)
        
        doc = libxml2dom.parseString(page, html=1)
        td_elements = doc.getElementsByTagName("td")
        
        c = 0
        for i in td_elements:
            data = i.textContent
            
            if( self.__validateDate(data) == 1 ):
                datum = time.strptime(data, '%d.%m.%Y')
                '''
                    datum ist gültig. prüfe nun, wann die notwendigen deltas erreicht wurden,
                    um die werte zu setzen
                '''
                if( self.__AktienkursHeute == 0 and datum >= date.today() - timedelta(days=3) ):
                    self.__AktienkursHeute = float( td_elements[c+2].textContent.replace(",", ".") )
                    
                if( self.__AktienkursVor6Monaten == 0 and datum < date.today() - timedelta(months=6) ):
                    self.__AktienkursVor6Monaten = float( td_elements[c+2].textContent.replace(",", ".") )
            
                if( self.__AktienkursVor12Monaten == 0 and datum < date.today() - timedelta(months=12) ):
                    self.__AktienkursVor12Monaten = float( td_elements[c+2].textContent.replace(",", ".") )
      
                LetzterMonat = date.today() - timedelta(date.today().day)
                VorletzterMonat = LetzterMonat - timedelta(LetzterMonat.day)
                VorVorletzterMonat = VorletzterMonat - timedelta(VorletzterMonat.day)    
                
                if( self.__AktieLetzterMonat == 0 and datum < LetzterMonat  ):
                    self.__AktieLetzterMonat = float( td_elements[c+2].textContent.replace(",", ".") )
                                    
                if( self.__AktieVorLetzterMonat == 0 and datum < VorletzterMonat  ):
                    self.__AktieVorLetzterMonat = float( td_elements[c+2].textContent.replace(",", ".") )
                    
                if( self.__AktieVorVorLetzterMonat == 0 and datum < VorVorletzterMonat ):
                    self.__AktieVorVorLetzterMonat = float( td_elements[c+2].textContent.replace(",", ".") )    
                
            c = c + 1    
        
    def __parseFinanzenNet(self, stock):
        self.__resetState()
        
        self.__getDataForStock(stock)
        
        ''' TODO
            den index (dax, CAC) ebenfalls irgendwo in eine klasse aufnehmen, zusammen mit
            finanztreff id etc. damit der hier abgefragt werden kann, passend zum stock
            '''
        
      
    def __validateDate(self, datum):
        result= 1
        
        try:
            d = time.strptime(datum, '%d.%m.%Y')
        except ValueError:
            result = 0
            
        return result
    
     
 
        
        