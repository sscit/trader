'''
Created on 02.09.2012

@author: Stefan
'''
from pTool.WebConnect import CWebConnect
from datetime import timedelta, date
import time, libxml2dom, datetime
from pData.Stock import CStock
import string, traceback, re


class CFinanzenNet(object):
    
    __webConnect = CWebConnect()


    def __init__(self):
        
        self.__FinanzenNetHistorischeKurseURL = "http://www.finanzen.net/kurse/kurse_historisch.asp"
        self.__FinanzenNetHistorischeKurseIndizesURL = "http://www.finanzen.net/index/XXX/Historisch"
        self.__UrlKBV = "http://www.finanzen.net/suchergebnis.asp?frmAktiensucheTextfeld="
        self.__UrlEinzelwerteListePerIndex = "http://www.finanzen.net/index/XXX"
        
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
        
    def getFinanzenNetId(self, stock):
        url= self.__UrlKBV + stock.ISIN
        page = self.__webConnect.runGETRequest( url )
        finanzenNetId = ""
        
        doc = libxml2dom.parseString(page, html=1)
        a_elements = doc.getElementsByTagName("a")
        
        for i in a_elements:
            if i.textContent == "Historisch" and "kurse_historisch.asp" in i.attributes["href"].value:
                url = i.attributes["href"].value
                finanzenNetId = str(url.split("=")[1].split("&")[0])
                break
        
        if finanzenNetId.isdigit() == False:
            raise NameError('Error: getFinanzenNetId, Id nicht numeric: ' + finanzenNetId)
        
        return finanzenNetId     
        
    def getEinzelwerteListe(self, strIndex):
        url = self.__UrlEinzelwerteListePerIndex.replace("XXX", strIndex)
        
        page = self.__webConnect.runGETRequest( url )
        page = page.replace("<br>", " ").replace("<br/>", " ").replace("<br />", " ")
                        
        doc = libxml2dom.parseString(page, html=1)
        td_elements = doc.getElementsByTagName("td")
        
        '''
            durch alle td elemente laufen und schauen,ob irgendwo eine isin gefunden wurde. falls ja, ist das ein gueltiger eintrag
        '''
        
        StockList = list()
        
        for i in td_elements:
            data = i.textContent
            
            arr = data.rsplit()
            
            if len(arr) > 1 and self.__checkForISIN(arr[-1]) == 1:
                s = CStock()
                
                s.ISIN = arr[-1]
                s.Name = string.join(arr[0:-1])
                StockList.append(s)
            
        if len(StockList) == 0:
            raise NameError('Achtung: Aktienliste fuer ' + strIndex + ' hat keine Werte!')    
            
        return StockList
        
    def __checkForISIN(self, ISIN):
                
        if len(ISIN) != 12:
            return 0
        
        if not (re.match("^[A-Za-z0-9]*$", ISIN)):
            return 0
        
        ISINNew = str(ISIN)
        letters = string.uppercase
        index = range(0, len(letters))
        
        c= 10
        for i in index:
            ISINNew = ISINNew.replace( letters[i], str(c))
            c = c + 1
        
        
        if self.__checkLuhn(ISINNew) == 1:
            return 1
        else:
            return 0    
        
        
    def __checkLuhn(self, purportedCC=''):
        summe = 0
        parity = len(purportedCC) % 2
        for i, digit in enumerate([int(x) for x in purportedCC]):
            if i % 2 == parity:
                digit *= 2
            if digit > 9:
                digit -= 9
            summe += digit
        return summe % 10 == 0 
    
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
        
        self.KBV = "NA"
        
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
        
        self.__POSTDataAktie["pkAktieNr"] = stock.FinanzenNetId
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
                
        page = self.__webConnect.runGETRequest( self.__UrlKBV + str(stock.ISIN) )
        
        doc = libxml2dom.parseString(page, html=1)
        td_elements = doc.getElementsByTagName("td")
        
        c = 0
        for i in td_elements:
            data = i.textContent
            
            if self.KBV == "NA" and data.find("KBV") > -1 and data.find("title=\"Kurs/Buchungs"):
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
    
    a = xx.getFinanzenNetId(d)
    
    b=1
    
    
    