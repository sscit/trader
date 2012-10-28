'''
Created on 24.09.2012

@author: Stefan
'''

from Presenter import CPresenter
from pDataInterface.FinanzenNet import CFinanzenNet
from pData.Stock import CStock
from datetime import timedelta, date
from pImport.ImporterDummy import CImporterDummy
import xlwt

class CPresenterExcel(CPresenter):
    '''
    classdocs
    '''


    def __init__(self):
        self.__heading_xf = xlwt.easyxf('font: bold on; align: wrap on, vert centre, horiz center')
        self.__stockData = xlwt.easyxf('font: bold off; align: wrap on')
        
    def printData(self, StockList, PointList, IndicatorList, Importer):
        
        excelName = date.today().strftime("%Y%m%d") + "_Importer_" + Importer.getName() + ".xls"
        
        book = xlwt.Workbook()
        sheet = book.add_sheet(Importer.getName())
        heading = ['ISIN', 'Aktie', 'Gesamtpunkte']
        
        for i in IndicatorList:
            heading.append( i.getName().rsplit(".")[-1].replace("CIndicator", "").replace("'>", "") )
        
        rowx = 0
        colx = 0
        for i in heading:
            sheet.write(rowx, colx, i, self.__heading_xf)
            colx +=1
            
        rowx += 1
        colx = 0
        c = 0
        for curStock in StockList:
            colx=0
            sheet.write(rowx, colx, curStock.ISIN, self.__stockData)
            sheet.write(rowx, colx+1, curStock.Name, self.__stockData)
            sheet.write(rowx, colx+2, PointList[c], self.__stockData)
            
            colx = 3
            for ind in IndicatorList:
                sheet.write(rowx, colx, ind.getPoints(curStock), self.__stockData)
                
                colx +=1
            
            c+=1
            rowx +=1
            
        
            
            
        book.save(excelName)
        
if __name__ == '__main__':
    xx = CPresenterExcel()
    
    Importer = CImporterDummy()
    StockList = Importer.getListOfStocks()
    PointList = [3, -1]
    IndicatorList = []
    
    xx.printData(StockList, PointList, IndicatorList, Importer)
    
    
        