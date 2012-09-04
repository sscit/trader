# -*- coding: iso-8859-1 -*-

'''
Created on 01.09.2012

@author: Stefan
'''
import libxml2dom


from pTool.WebConnect import CWebConnect
from pData.Stock import CStock

class COnvista(object):
    
    __webConnect = CWebConnect()

    def __init__(self):
        self.__OnvistaFundamentaldatenTabelleUrl = "http://www.onvista.de/aktien/kennzahlen/fundamental.html?ID_OSI="
               
        self.__EKRAktJahrProzent = 0
        self.__EbitMargeAktJahrProzent = 0
        self.__EigenkapitalquoteAktJahrProzent = 0
        self.__KGVMean5Years = 0
        self.__KGVAktJahr = 0
        self.__KBVAktJahr = 0
        self.__DivRenditeAktJahrProzent = 0
        
                
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
            if (data == "Dividendenrendite in %"):
                self.__DivRenditeAktJahrProzent = float( td_elements[c+1].textContent.replace(",", ".") )
            if (data == u"Kurs-Buchwert-Verhältnis"):
                self.__KBVAktJahr = float( td_elements[c+1].textContent.replace(",", ".") )
            if (data == "KGV"):
                self.__KGVAktJahr = float( td_elements[c+1].textContent.replace(",", ".") )
                
                summe = 0
                for j in {1,2,3,4,5}:
                    summe += float(td_elements[c+j].textContent.replace(",",".")) 
                self.__KGVMean5Years = summe / 5
            if (data == "Eigenkapitalquote in %"):
                self.__EigenkapitalquoteAktJahrProzent = float( td_elements[c+1].textContent.replace(",", ".") )
            if (data == "EBIT-Marge in %"):
                self.__EbitMargeAktJahrProzent = float( td_elements[c+1].textContent.replace("%", "").replace(",", ".") )
            if (data == "Eigenkapitalrendite in %"):
                self.__EKRAktJahrProzent = float( td_elements[c+1].textContent.replace("%", "").replace(",", ".") )
                
            c = c + 1
            

if __name__ == '__main__':
    xx = COnvista()
     
    d = CStock("BASF11", "BASF", 59905, 81490)
     
    print "ekr " + xx.getEKRAktJahrProzent(d)
    print "ebit marge " + xx.getEbitMargeAktJahrProzent(d)
    print "eigenkapital " + xx.getEigenkapitalquoteAktJahrProzent(d)
    print "kgv mean " + str(xx.getKGVMean5Years(d))
    print "kgv akt jahr " + xx.getKGVAktJahr(d)
    print "kbv " + xx.getKBVAktJahr(d)

        