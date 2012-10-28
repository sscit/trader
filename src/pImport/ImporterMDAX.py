'''
Created on 25.08.2012

@author: Stefan
'''
from Importer import CImporter
from pData.Stock import CStock
from pDataInterface.FinanzenNet import CFinanzenNet
from pDataInterface.Onvista import COnvista
from pImport.Importer import CImporter

class CImporterMDAX(CImporter):

    def __init__(self):
        self.__FN = CFinanzenNet()
        self.__Onvista= COnvista()
        self.__StockList = list()
        
        self.__AnzahlAktienInIndex = 50
        self._strIndexFinanzenNet = "MDAX"
        self.__strBoerseFinanzenNet = "FSE"
        
    def getListOfStocks(self):
        
        self.__StockList = self.__FN.getEinzelwerteListe(self._strIndexFinanzenNet)
        
        self.validateListeLaenge(self.__StockList, self.__AnzahlAktienInIndex, self._strIndexFinanzenNet)
        
        for i in self.__StockList:
            i.strBoerseFinanzenNet =  self.__strBoerseFinanzenNet
            i.strIndexFinanzenNet = self._strIndexFinanzenNet
            i.FinanzenNetId = self.__FN.getFinanzenNetId(i)
            i.OnvistaId = self.__Onvista.getOnvistaId(i)
            mkap = self.__Onvista.getMarktkapitalisierungInEuro(i)
            if mkap > 5*pow(10,9):
                i.isLargeCap = True
            else:
                i.isLargeCap= False
        
                
        return self.__StockList
    

if __name__ == '__main__':
    xx = CImporterMDAX()
     
    
    
    a = xx.getListOfStocks()
    
    b=1
    
    
    
