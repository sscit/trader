'''
Created on 25.08.2012

@author: Stefan
'''
from Importer import CImporter
from pData.Stock import CStock
from pDataInterface.FinanzenNet import CFinanzenNet

class CImporterDAX(CImporter):

    def __init__(self):
        self.__FN = CFinanzenNet()
        self.__StockList = list()
        
        self.__templateStock = CStock()
        
        self.__templateStock.strIndexFinanzenNet = "DAX"
        self.__templateStock.strBoerseFinanzenNet = "FSE"
        
    def getListOfStocks(self):
        
        self.__StockList = self.__FN.getEinzelwerteListe(self.__templateStock.strIndexFinanzenNet)
        
        for i in self.__StockList:
            i.strBoerseFinanzenNet =  self.__templateStock.strBoerseFinanzenNet
            i.strIndexFinanzenNet = self.__templateStock.strIndexFinanzenNet
            
        
        
        
        
        return self.__StockList
    

if __name__ == '__main__':
    xx = CImporterDAX()
     
    d = CStock("BASF11", "BASF", 59905, 81490, 1, "FSE", "DAX")
    
    a = xx.getListOfStocks()
    
    b=1
    
    
    ''' TODO
    den importer fuer den dax fertig machen:
    - die ids von onvista sowie finanzen.net ergaenzen
    -- dazu einfach mit den ISINs die einzelnen seiten der aktien aufrufen und die info extrahieren
    -- is large cap am besten aus marktkapitalisierung onvista auslesen
    - excehption handling ergaenzen, bei fatalen fehlern

        