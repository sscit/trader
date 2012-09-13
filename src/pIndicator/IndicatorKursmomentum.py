from pIndicator.Indicator import CIndicator
from pIndicator.IndicatorKursVor12M import CIndicatorKursVor12M
from pIndicator.IndicatorKursVor6M import CIndicatorKursVor6M

class CIndicatorKursMomentum(CIndicator):

    def __init__(self):
        CIndicator.__init__(self)
        self._Name = str(self.__class__)
        
    def getPoints(self, stock):    
        twelveM = CIndicatorKursVor12M()
        sixM = CIndicatorKursVor6M()
        
        if sixM.getPoints(stock) == 1 and (twelveM.getPoints(stock) == 0 or twelveM.getPoints(stock) == -1):
            result = 1
        elif sixM.getPoints(stock) == -1 and (twelveM.getPoints(stock) == 0 or twelveM.getPoints(stock) == 1):
            result = -1
        else:
            result = 0
            
        return result