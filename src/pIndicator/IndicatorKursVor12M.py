from pIndicator.Indicator import CIndicator
from pDataInterface.FinanzenNet import CFinanzenNet

class CIndicatorKursVor12M(CIndicator):

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
        
        ratio =  self.__FinanzenNet.AktienkursHeute / self.__FinanzenNet.AktienkursVor12Monaten
        
        if ratio > 1.05:
            result = 1
        elif ratio < 0.95:
            result = -1
        else:
            result = 0 
        
        self.__StockDict[stock] = result      
        
        return result   