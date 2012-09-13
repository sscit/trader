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
        self.__UrlKBV = "http://www.finanzen.net/suchergebnis.asp?frmAktiensucheTextfeld="
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
        
        self.__resetState()
    
    def __resetState(self):
        self.AktienkursHeute = 0
        self.AktienkursVor6Monaten = 0
        self.AktienkursVor12Monaten = 0
        
        ''' aktuelles datum z.b. 10.9
            letzer monat: dax wert von 29.8 bis 1.9
            vor letzter monat: dax wert von ende juli/anfang august
            vorvorletzter monat: dax wert von ende juni/anfang august
        '''
        '''
        Enthaelt den Indexwert vom Ende letzten Monat, Ende vorletzten Monat, vorvorletzten Monat etc. 
        '''
        self.IndexList = [0,0,0,0]
                
        self.AktieList = [0,0,0,0]
        
        self.KBV = 0
        
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
     
                DatumList= []    
                DatumList.append( date.today() - timedelta(date.today().day) )
                DatumList.append( DatumList[0] - timedelta(DatumList[0].day) )
                DatumList.append( DatumList[1] - timedelta(DatumList[1].day) )   
                DatumList.append( DatumList[2] - timedelta(DatumList[2].day) )
                
                for i in [0,1,2,3]:
                    if( self.IndexList[i] == 0 and datum <= DatumList[i]  ):
                        self.IndexList[i] = float( td_elements[c+2].textContent.replace(".", "").replace(",", ".") )
                
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
      
                DatumList= []    
                DatumList.append( date.today() - timedelta(date.today().day) )
                DatumList.append( DatumList[0] - timedelta(DatumList[0].day) )
                DatumList.append( DatumList[1] - timedelta(DatumList[1].day) )   
                DatumList.append( DatumList[2] - timedelta(DatumList[2].day) )
                
                for i in [0,1,2,3]:
                    if( self.AktieList[i] == 0 and datum <= DatumList[i]  ):
                        self.AktieList[i] = float( td_elements[c+2].textContent.replace(".", "").replace(",", ".") )
                
            c = c + 1    
        
    def parseFinanzenNet(self, stock):
        self.__resetState()
        
        self.__getDataforStock(stock)
        
        self.__getDataForIndex(stock)
        
        self.__getKBV(stock)
        
    def getKBV(self, stock):
        self.__resetState()
        
        self.__getKBV(stock)
        
        return self.KBV
        
    def __getKBV(self, stock):
                
        page = self.__webConnect.runGETRequest( self.__UrlKBV + str(stock.WKN) )
        
        doc = libxml2dom.parseString(page, html=1)
        td_elements = doc.getElementsByTagName("td")
        
        c = 0
        for i in td_elements:
            data = i.textContent
            
            if self.KBV == 0 and data.find("KBV") > -1 and data.find("title=\"Kurs/Buchungs"):
                self.KBV = float( td_elements[c+1].textContent.replace(",", ".") )
                
            c = c + 1
      
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
    
    print "index aug " + str(xx.IndexList[0])
    print "index sept " + str(xx.IndexList[1])
    
    '''
    TODO
     mit den gewonnenen daten aus finanzen.net die indikatoren fuer die historischen kurse ausrechnen, der vergleich
     ausserdem testfaelle fuer finanzen.net machen, das die historischen kurse immer richtig abgerufen werden!
    '''
    