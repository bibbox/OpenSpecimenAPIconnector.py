#! /bin/python3


class url_gen:

    #Konstruktor
    def __init__(self):

        pass


    def site_search_url_gen(self, sitename=None, institutename=None, maxresults=100):
    
        url_string = '/?'

        if sitename!=None:
            if isinstance(sitename,list):
                for name in sitename:
                    url_string += 'name=' + str(name).replace(' ', '+') + '&'
            else:
                url_string += 'name=' + str(sitename).replace(' ', '+') + '&'

        if institutename!=None:
            if isinstance(institutename,list):
                for name in institutename:
                    url_string += 'institute=' + str(name).replace(' ','+') + '&'
            else:
                url_string += 'institute=' + str(institutename).replace(' ','+') + '&'
        
        url_string += 'maxResults=' + str(maxresults)

        return url_string
    