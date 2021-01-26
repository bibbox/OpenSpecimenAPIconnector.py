#! /bin/python3


def _write_instance(entity, value):
    
    instance= ''
    if isinstance(value,list):
        for val in value:
            instance += str(entity) + '=' + str(val).replace(' ', '+') + '&'
    else:
        instance += str(entity) + '=' + str(val).replace(' ', '+') + '&'

        return instance

class url_gen:

    #Konstruktor
    def __init__(self):

        pass

    def site_search_url_gen(self, sitename=None, institutename=None, maxresults=100):
    
        url_string = '/?'

        if sitename!=None:
            url_string += _write_instance(entity = 'name', value = sitename)

        if institutename!=None:
            url_string += _write_instance(entity = 'institute', value = institutename
        
        url_string += 'maxResults=' + str(maxresults)

        return url_string

    def cp_search_url_gen(self, searchstring = None, title = None, piid = None, reponame = None, startat = none, maxresults = None, detailedlist = None):

        url_string='?'

        if searchstring != None:
            url_string += _write_instance(entity = 'query', value = searchstring)
        
        if title != None:
            url_string += _write_instance(entity = 'title', value = title)

        if piid != None:
            url_string += _write_instance(entity = 'piId', value = piid)

        if reponame != None:
            url_string += _write_instance(entity = 'repositoryName', value = reponame)

        if startat != None:
            url_string += _write_instance(entity = 'startAt', value = startat)

        if maxresults != None:
            url_string += _write_instance(entity = 'maxResults', value = maxresults)
        
        if str(detailedlist).lower() == 'true':
            url_string += _write_instance(entity = 'detailedList', value = str(detailedlist).lower())
        
        url_string = url_string[0:-1]

        return url_string

    def query_url_gen(self, cpid = None, searchstring = None, start = None, max_ = None, countreq = None):

        url_string = '?'

        if cpid != None:
            url_string += _write_instance(entity = 'cpId', value = cpid)
        
        if searchString != None:
            url_string += _write_instance(entity = 'searchString', value = searchstring)

        if start != None:
            url_string += _write_instance(entity = 'start', value = start)

        if max_ != None:
            url_string += _write_instance(entity = 'max', value = max_)

        if countreq != None:
            url_string += _write_instance(entity = 'countReq', value = countreq)

        url_string = url_string[0:-1]
        
        return url_string

    