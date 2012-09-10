'''
Created on 02.09.2012

@author: Stefan
'''
from pTool.WebConnect import CWebConnect
from datetime import timedelta, date
import time, libxml2dom, datetime
from pData.Stock import CStock

class CFinanzenNet(object):
    
    __webConnect = CWebConnect()


    def __init__(self):
        
        self.__FinanzenNetHistorischeKurseURL = "http://www.finanzen.net/kurse/kurse_historisch.asp"
        self.__FinanzenNetHistorischeKurseIndizesURL = "http://www.finanzen.net/index/XXX/Historisch"
        self.__POSTDataAktie = {'pkAktieNr' : 0,
                          'strBoerse' : '',
                          'dtTag1': 1,
                          'dtMonat1': 7,
                          'dtJahr1' : 2003,
                          'dtTag2': 2,
                          'dtMonat2': 7,
                          'dtJahr2' : 2003
                          }
        self.__POSTDataIndex = {
                          'dtTag1': 1,
                          'dtMonat1': 7,
                          'dtJahr1' : 2003,
                          'dtTag2': 2,
                          'dtMonat2': 7,
                          'dtJahr2' : 2003
                          }
    
    def __resetState(self):
        self.AktienkursHeute = 0
        self.AktienkursVor6Monaten = 0
        self.AktienkursVor12Monaten = 0
        
        ''' aktuelles datum z.b. 10.9
            letzer monat: dax wert von 29.8 bis 1.9
            vor letzter monat: dax wert von ende juli/anfang august
            vorvorletzter monat: dax wert von ende juni/anfang august
        '''
        self.IndexLetzterMonat = 0
        self.IndexVorLetzterMonat = 0
        self.IndexVorVorLetzterMonat = 0
        
        self.AktieLetzterMonat = 0
        self.AktieVorLetzterMonat = 0
        self.AktieVorVorLetzterMonat = 0
        
    def __getDataForIndex(self, stock):
        t1 = date.today()
        t2 = t1 - timedelta(days=380)
        
        url = self.__FinanzenNetHistorischeKurseIndizesURL.replace("XXX", stock.strIndexFinanzenNet)
        
        self.__POSTDataIndex["dtTag1"] = t2.day
        self.__POSTDataIndex["dtMonat1"] = t2.month
        self.__POSTDataIndex["dtJahr1"] = t2.year
        
        self.__POSTDataIndex["dtTag2"] = t1.day
        self.__POSTDataIndex["dtMonat2"] = t1.month
        self.__POSTDataIndex["dtJahr2"] = t1.year
        
        page = self.__webConnect.runPOSTRequest(url, self.__POSTDataIndex)
        
        doc = libxml2dom.parseString(page, html=1)
        td_elements = doc.getElementsByTagName("td")
        
        c = 0
        for i in td_elements:
            data = i.textContent
            
            if( self.__validateDate(data) == 1 ):
                datum = datetime.datetime.strptime(data, '%d.%m.%Y').date()
 
                '''
                    datum ist gueltig. pruefe nun, wann die notwendigen deltas erreicht wurden,
                    um die werte zu setzen
                '''
     
                LetzterMonat = date.today() - timedelta(date.today().day)
                VorletzterMonat = LetzterMonat - timedelta(LetzterMonat.day)
                VorVorletzterMonat = VorletzterMonat - timedelta(VorletzterMonat.day)    
                
                if( self.IndexLetzterMonat == 0 and datum <= LetzterMonat  ):
                    self.IndexLetzterMonat = float( td_elements[c+2].textContent.replace(".", "").replace(",", ".") )
                                    
                if( self.IndexVorLetzterMonat == 0 and datum <= VorletzterMonat  ):
                    self.IndexVorLetzterMonat = float( td_elements[c+2].textContent.replace(".", "").replace(",", ".") )
                    
                if( self.IndexVorVorLetzterMonat == 0 and datum <= VorVorletzterMonat ):
                    self.IndexVorVorLetzterMonat = float( td_elements[c+2].textContent.replace(".", "").replace(",", ".") )
                
            c = c + 1
    
    def __getDataforStock(self, stock):
        t1 = date.today()
        t2 = t1 - timedelta(days=380)
        
        self.__POSTDataAktie["pkAktieNr"] = stock.FinanztreffId
        self.__POSTDataAktie["strBoerse"] = stock.strBoerseFinanzenNet
        
        self.__POSTDataAktie["dtTag1"] = t2.day
        self.__POSTDataAktie["dtMonat1"] = t2.month
        self.__POSTDataAktie["dtJahr1"] = t2.year
        
        self.__POSTDataAktie["dtTag2"] = t1.day
        self.__POSTDataAktie["dtMonat2"] = t1.month
        self.__POSTDataAktie["dtJahr2"] = t1.year
        
        page = self.__webConnect.runPOSTRequest(self.__FinanzenNetHistorischeKurseURL, self.__POSTDataAktie)
        
        doc = libxml2dom.parseString(page, html=1)
        td_elements = doc.getElementsByTagName("td")
        
        c = 0
        for i in td_elements:
            data = i.textContent
            
            if( self.__validateDate(data) == 1 ):
                datum = datetime.datetime.strptime(data, '%d.%m.%Y').date()
                '''
                    datum ist gueltig. pruefe nun, wann die notwendigen deltas erreicht wurden,
                    um die werte zu setzen
                '''
                if( self.AktienkursHeute == 0 and datum >= date.today() - timedelta(days=3) ):
                    self.AktienkursHeute = float( td_elements[c+2].textContent.replace(",", ".") )
                    
                if( self.AktienkursVor6Monaten == 0 and datum <= date.today() - timedelta(days=180) ):
                    self.AktienkursVor6Monaten = float( td_elements[c+2].textContent.replace(",", ".") )
            
                if( self.AktienkursVor12Monaten == 0 and datum <= date.today() - timedelta(days=360) ):
                    self.AktienkursVor12Monaten = float( td_elements[c+2].textContent.replace(",", ".") )
      
                LetzterMonat = date.today() - timedelta(date.today().day)
                VorletzterMonat = LetzterMonat - timedelta(LetzterMonat.day)
                VorVorletzterMonat = VorletzterMonat - timedelta(VorletzterMonat.day)    
                
                if( self.AktieLetzterMonat == 0 and datum <= LetzterMonat  ):
                    self.AktieLetzterMonat = float( td_elements[c+2].textContent.replace(".", "").replace(",", ".") )
                                    
                if( self.AktieVorLetzterMonat == 0 and datum <= VorletzterMonat  ):
                    self.AktieVorLetzterMonat = float( td_elements[c+2].textContent.replace(".", "").replace(",", ".") )
                    
                if( self.AktieVorVorLetzterMonat == 0 and datum <= VorVorletzterMonat ):
                    self.AktieVorVorLetzterMonat = float( td_elements[c+2].textContent.replace(".", "").replace(",", ".") )    
                
            c = c + 1    
        
    def parseFinanzenNet(self, stock):
        self.__resetState()
        
        self.__getDataforStock(stock)
        
        self.__getDataForIndex(stock)
        
      
    def __validateDate(self, datum):
        result= 1
        
        try:
            d = time.strptime(datum, '%d.%m.%Y')
        except ValueError:
            result = 0
            
        return result
        

if __name__ == '__main__':
    xx = CFinanzenNet()
     
    d = CStock("BASF11", "BASF", 59905, 81490, 1, "FSE", "DAX")
    
    xx.parseFinanzenNet(d)
    
    print "kurs heute " + xx.AktienkursHeute
    print "kurs heute " + xx.AktienkursHeute
    
    '''
    TODO
     mit den gewonnenen daten aus finanzen.net die indikatoren für die historischen kurse ausrechnen, der vergleich
     außerdem testfälle für finanzen.net machen, das die historischen kurse immer richtig abgerufen werden!
    '''
    