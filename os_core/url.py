#! /bin/python3


def _write_instance(entity, value, sep = '&'):
    
    instance= ''
    if isinstance(value,list):
        for val in value:
            instance += str(entity) + '=' + str(val).replace(' ', '+') + str(sep)
    else:
        instance += str(entity) + '=' + str(val).replace(' ', '+') + str(sep)

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
            url_string += _write_instance(entity = 'institute', value = institutename)
        
        url_string += 'maxResults=' + str(maxresults)

        return url_string

    def cp_search_url_gen(self, searchstring = None, title = None, piid = None, reponame = None, startat = None, maxresults = None, detailedlist = None):

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


    def search_specimen(self, label=None, cprid=None, eventid=None, visitid=None, maxres="100", exact="false", extension="true"):

        url_string = '?'

        if label != None:
            url_string += _write_instance(entity = 'label', value = label)

        if cprid != None:
            url_string += _write_instance(entity = 'cprId', value = cprid)

        if eventid != None:
            url_string += _write_instance(entity = 'eventId', value = eventid)
        
        if visitid != None:
            url_string += _write_instance(entity = 'visitId', value = visitid)

        if maxres !="100":
            url_string += _write_instance(entity = 'maxResults', value = maxres)

        if exact == 'true':
            url_string += _write_instance(entity = 'exactMatch', value = exact)
        
        if extension == 'true':
            url_string += _write_instance(entity = 'includeExtensions', value = extension)
        
        url_string= url_string[0:-1]

        return url_string

    def delete_specimens(self, specimenids):

        url_string = '?id='

        if isinstance(specimenids,list):
            for id_ in specimenids:
                url_string += str(id_) + ','
            url_string = url_string[0:-1]
        else:
            url_string += str(specimenids)

        return url_string

    