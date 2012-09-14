'''
Created on 25.08.2012

@author: Stefan

This indicator evaluates KGV for the current year and the mean of the last 5 years
'''
from pIndicator.Indicator import CIndicator
from pDataInterface.Onvista import COnvista

class CIndicatorKGVMean(CIndicator):

    def __init__(self):
        CIndicator.__init__(self)
        self.__Onvista = COnvista()
        self.__StockDict = dict()
        self._Name = str(self.__class__)
        
    def getPoints(self, stock):    
        
        '''
        check if this stock has already been processed
        '''
        
        if stock in self.__StockDict:
            ekr = self.__StockDict[stock]
        else:
            ekr = self.__Onvista.getKGVMean5Years(stock)
            self.__StockDict[stock] = ekr
        
        result = 0
        
        if ekr == "NA":
            result = 0
            print "Warnung: " + self._Name + ": " + stock.Name + ": Wert nicht verfügbar"
        elif ekr < 12:
            result = 1
        elif (ekr >= 12 and ekr <= 16):
            result = 0
        else: 
            result = -1
        
        
        return result

class CIndicatorKGV(CIndicator):

    def __init__(self):
        CIndicator.__init__(self)
        self.__Onvista = COnvista()
        self.__StockDict = dict()
        self._Name = str(self.__class__)
        
    def getPoints(self, stock):    
        
        '''
        check if this stock has already been processed
        '''
        
        if stock in self.__StockDict:
            return self.__StockDict[stock]
            
        ekr = self.__Onvista.getKGVAktJahr(stock)
        self.__StockDict[stock] = ekr
        
        result = 0
        
        if ekr == "NA":
            result = 0
            print "Warnung: " + self._Name + ": " + stock.Name + ": Wert nicht verfügbar"
        elif ekr < 12:
            result = 1
        elif (ekr >= 12 and ekr <= 16):
            result = 0
        else:
            result = -1
        
        
        return result
    