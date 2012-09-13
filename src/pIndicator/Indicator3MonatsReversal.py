from pIndicator.Indicator import CIndicator
from pDataInterface.FinanzenNet import CFinanzenNet


class CIndicator3MonatsReversal(CIndicator):

    def __init__(self):
        CIndicator.__init__(self)
        
        self.__FinanzenNet = CFinanzenNet()
        self.__StockDict = dict()
        self._Name = str(self.__class__)
        
    def getPoints(self, stock):    
        
        '''
        check if this stock has already been processed
        '''
        
        if stock in self.__StockDict:
            return self.__StockDict[stock]
            
        self.__FinanzenNet.parseFinanzenNet(stock)
        
        aktieAenderung = [0, 0, 0]
        indexAenderung = [0,0,0]
        
        kleiner = 0
        groesser = 0
        
        for i in [0,1,2]:
            aktieAenderung[i] = self.__FinanzenNet.AktieList[i] / self.__FinanzenNet.AktieList[i+1]
            indexAenderung[i] = self.__FinanzenNet.IndexList[i] / self.__FinanzenNet.IndexList[i+1]
            
            if aktieAenderung[i] < indexAenderung[i]:
                kleiner = kleiner + 1
            elif aktieAenderung[i] > indexAenderung[i]:
                groesser = groesser + 1
            
        if kleiner == len(aktieAenderung):
            result = 1
        elif groesser == len(aktieAenderung):
            result = -1
        else:
            result = 0  
        
        self.__StockDict[stock] = result      
        
        return result   