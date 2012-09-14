# -*- coding: iso-8859-1 -*-

'''
Created on 01.09.2012

@author: Stefan
'''
import libxml2dom
import string, traceback

from pTool.WebConnect import CWebConnect
from pData.Stock import CStock

class COnvista(object):
    
    __webConnect = CWebConnect()

    def __init__(self):
        self.__OnvistaFundamentaldatenTabelleUrl = "http://www.onvista.de/aktien/kennzahlen/fundamental.html?ID_OSI="
        self.__StockOverviewUrl = "http://www.onvista.de/aktien/suche.html?SEARCH_VALUE="
               
        self.__EKRAktJahrProzent = 0
        self.__EbitMargeAktJahrProzent = 0
        self.__EigenkapitalquoteAktJahrProzent = 0
        self.__KGVMean5Years = 0
        self.__KGVAktJahr = 0
        self.__KBVAktJahr = 0
        self.__DivRenditeAktJahrProzent = 0
        self.__MarktkapitalisierungInEuro = 0
        
    def getOnvistaId(self, stock):
        page = self.__webConnect.runGETRequest( self.__StockOverviewUrl + str(stock.ISIN) )
        
        onvistaId = ""
        
        doc = libxml2dom.parseString(page, html=1)
        a_elements = doc.getElementsByTagName("a")
        
        for i in a_elements:
            if i.textContent == "Kennzahlen" and "kennzahlen/fundamental.html?ID_OSI" in i.attributes["href"].value:
                url = i.attributes["href"].value
                onvistaId = str(url.split("=")[1])
                break
        
        if onvistaId.isdigit() == False:
            raise NameError('Error: getOnvistaId, Id nicht numeric: ' + onvistaId)
        
        return onvistaId 
        
    def getMarktkapitalisierungInEuro(self, stock):
        self.__parseOnvistaSummary(stock)            
        return self.__MarktkapitalisierungInEuro
                
    def getEKRAktJahrProzent(self, stock):
        self.__parseOnvistaSummary(stock)
        return self.__EKRAktJahrProzent
    
    def getEbitMargeAktJahrProzent(self, stock):
        self.__parseOnvistaSummary(stock)
        return self.__EbitMargeAktJahrProzent
    
    def getEigenkapitalquoteAktJahrProzent(self, stock):
        self.__parseOnvistaSummary(stock)
        return self.__EigenkapitalquoteAktJahrProzent
    
    def getKGVMean5Years(self, stock):
        self.__parseOnvistaSummary(stock)
        return self.__KGVMean5Years
    
    def getKGVAktJahr(self, stock):
        self.__parseOnvistaSummary(stock)
        return self.__KGVAktJahr
    
    def getKBVAktJahr(self, stock):
        self.__parseOnvistaSummary(stock)
        return self.__KBVAktJahr
    '''    
    def getDivRenditeAktJahrProzent(self, stock):
        self.__parseOnvistaSummary(stock)        
        return self.__DivRenditeAktJahrProzent
       ''' 
        
    def __parseOnvistaSummary(self, stock):
               
        page = self.__webConnect.runGETRequest( self.__OnvistaFundamentaldatenTabelleUrl + str(stock.OnvistaId) )
        
        doc = libxml2dom.parseString(page, html=1)
        td_elements = doc.getElementsByTagName("td")
        
        c = 0
        for i in td_elements:
            data = i.textContent
            try:
                if (data == "Marktkap.:"):
                    try:
                        tmp = float(td_elements[c+1].textContent.replace(".", "").replace(",",".").replace(" Mio EUR",""))
                        self.__MarktkapitalisierungInEuro = tmp*1000 * 1000
                    except ValueError:
                        self.__MarktkapitalisierungInEuro = "NA"
                        
                if (data == "Dividendenrendite in %"):
                    try:
                        self.__DivRenditeAktJahrProzent = float( td_elements[c+1].textContent.replace(",", ".") )
                    except ValueError:
                        self.__DivRenditeAktJahrProzent = "NA"
                    
                if (data == u"Kurs-Buchwert-Verhältnis"):
                    try:
                        self.__KBVAktJahr = float( td_elements[c+1].textContent.replace(",", ".") )
                    except ValueError:
                        self.__KBVAktJahr = "NA"
                        
                if (data == "KGV"):
                    try:
                        self.__KGVAktJahr = float( td_elements[c+1].textContent.replace(",", ".") )
                        
                        summe = 0
                        for j in {1,2,3,4,5}:
                            summe += float(td_elements[c+j].textContent.replace(",",".")) 
                        self.__KGVMean5Years = summe / 5
                    except ValueError:
                        self.__KGVMean5Years = "NA"
                        self.__KGVAktJahr = "NA"
                        
                if (data == "Eigenkapitalquote in %"):
                    try:
                        self.__EigenkapitalquoteAktJahrProzent = float( td_elements[c+1].textContent.replace(",", ".") )
                    except ValueError:
                        self.__EigenkapitalquoteAktJahrProzent= "NA"
                        
                if (data == "EBIT-Marge in %"):
                    try:
                        self.__EbitMargeAktJahrProzent = float( td_elements[c+1].textContent.replace("%", "").replace(",", ".") )
                    except ValueError:
                        self.__EbitMargeAktJahrProzent = "NA"
                        
                if (data == "Eigenkapitalrendite in %"):
                    try:
                        self.__EKRAktJahrProzent = float( td_elements[c+1].textContent.replace("%", "").replace(",", ".") )
                    except ValueError:
                        self.__EKRAktJahrProzent = "NA"
                        
            except ValueError, e:
                traceback.print_exc()
                raise ValueError("Error parseOnvistaSummary, Stock " + stock.Name + ", ISIN " + stock.ISIN)
                
            c = c + 1
            

if __name__ == '__main__':
    xx = COnvista()
     
    d = CStock("BASF11", "BASF", 59905, 81490)
     
    print "marktkap  " + str(xx.getMarktkapitalisierungInEuro(d))
    print "id " + str(xx.getOnvistaId(d))

        