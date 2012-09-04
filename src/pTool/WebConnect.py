'''
Created on 01.09.2012

@author: Stefan
'''

import urllib, urllib2, time, json

class CWebConnect(object):
    '''
    classdocs
    '''


    def __init__(self):
        # Maps the unique url to the content of the page to cache data and avoid multiple calls
        self.__mapUrlsToPageContent = dict()
        
    def runGETRequest(self, pageUrl):
        
        if( pageUrl in self.__mapUrlsToPageContent ):
            return self.__mapUrlsToPageContent[pageUrl]
        
        req = urllib2.Request(pageUrl)
        browser = "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)"
        req.add_header('User-Agent', browser)
        response = urllib2.urlopen(req)
        
        page = response.read()
        
        self.__mapUrlsToPageContent[pageUrl] = page
        
        return page
    
    def runPOSTRequest(self, pageUrl, postData):
        try:
            key = pageUrl + json.dumps(postData)
            
            if( key in self.__mapUrlsToPageContent ):
                return self.__mapUrlsToPageContent[pageUrl]
            
            data = urllib.urlencode(postData)          
            req = urllib2.Request(pageUrl, data)
            response = urllib2.urlopen(req)
            the_page = response.read() 
           
            return the_page
        
        except Exception, detail: 
            print "Err ", detail 
        
        
'''
        
xx =  CWebConnect()

url = 'http://www.finanzen.net/kurse/kurse_historisch.asp' # write ur URL here

values = {'pkAktieNr' : 938, #write ur specific key/value pair
          #'strAktieWKN' : 'A1EWWW',
          #'strAktieISIN' : 'DE000A1EWWW0',
          #'strAktieSymbol' : '' , 
          #'strAktieName' : 'adidas AG', 
          'strBoerse' : 'FSE',
          'dtTag1': 1,
          'dtMonat1': 7,
          'dtJahr1' : 2003,
          'dtTag2': 2,
          'dtMonat2': 7,
          'dtJahr2' : 2003
          }

print xx.runPOSTRequest(url, values)
        


'''