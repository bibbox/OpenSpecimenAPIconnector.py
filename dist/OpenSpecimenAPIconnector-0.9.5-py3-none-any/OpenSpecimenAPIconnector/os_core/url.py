#! /bin/python3


def _write_instance(entity, value, sep = '&'):

    """Helper function to write the search string.

    Helps to write the search string, can handle lists and values.
    The different entities have to be known and can be found out with the documentation.

    Parameters
    ----------
    entity : string
        The name of the search Parameters.

    value : string or list
        The values corresponding to the entity.

    sep :  string
        The separator between the search parameters and values, most times OS takes '&'.

    Returns
    -------
    string
        String with the 'entities=values&....', such that Openspecimen can dissolve it.
    """
    
    instance= ''
    if isinstance(value,list):
        for val in value:
            instance += str(entity) + '=' + str(val).replace(' ', '+') + str(sep)
    else:
        instance += str(entity) + '=' + str(value).replace(' ', '+') + str(sep)

        return instance

class url_gen:

    """Generates the endpoint URL for search- and list operations

    This class generates the Parameters string used  in search operations. It can also be used on arrays and lists.
    For Examples deleting a list of specimens can be handled with this class. 
    Parameters strings look like '?entity1=value1&...&entityx=valuex'. To specify a list/array operation Parameters string
    format follows the following rule '?entity=value1,...,valuex&'

    Note
    -----
    In order to use this and also the other classes, the user has to know OpenSpecimen. In the core classes, one can
    just pass the parameters via a JSON-formatted string. This means the user has to know the keywords.
    The API calls are documented in https://openspecimen.atlassian.net/wiki/spaces/CAT/pages/1116035/REST+APIs and 
    the calls refer to this site. More details can be seen in the documentation.

    """

    def __init__(self):

        """Constructor of the class url_gen

        The constructor of the class url_gen. The base_url is set in the util_classes.
        """

        pass

    def site_search_url_gen(self, sitename=None, institutename=None, maxresults=100):

        """Generates the string for Site

        This function generates the Parameters string to search for sites, with names or the sites to an institute.
        Sitename and Institutename can be lists, they are handled as a logical AND. 

        Parameters
        ----------
        sitename : string or list
            Substring of the Site which wants to be searched for as string or list.

        instituename : string or list
            Substring of the Institute which want to be searched for as string or list.
        
        maxresults : string or int
            The maximum results what should be shown. OpenSpecimen's and here the default-value is 100.
            Gets converted to a string.

        Returns
        -------
        string
            endpoint of the searchoperation, looks like '?name='sitename1&name=sitename2&...&institute=institutenamex'.
        """
   
        url_string = '/?'

        if sitename!=None:
            url_string += _write_instance(entity = 'name', value = sitename)

        if institutename!=None:
            url_string += _write_instance(entity = 'institute', value = institutename)
        
        url_string += 'maxResults=' + str(maxresults)

        return url_string

    def cp_search_url_gen(self, searchstring = None, title = None, piid = None, reponame = None, startat = None, maxresults = None, detailedlist = None):

        """Generates the Parameters string for Collection Protocol search

        This function generates the Parameters string to search for collection protocols.
        Permissable values are specified within OpenSpecimen.
        Values can be passed as lists single parameters will be added as logical AND. 

        Note
        ----
        All parameters can be passed to the function as lists and will be reformated to be accepted by Openspecimen.
        Parameters permissible to be lists are marked as such within the parameters section.

        Parameters
        ----------
        searchstring : string or list
            Substring of the title and short title which want to be searched for as string or list.

        title : string or list
            Substring of the title which wants to be searched for as string or list.
        
        ppid : string or int
            The ID of the principal investigator as string or int. Gets converted to a string.

        reponame : string or list
            Name of the repositories as string or list.
        
        startat : string or int
            Defines which row of the search outcome will be the first to show in the return(default n=0)

        maxresults : string or int
            Defines how many rows of the search outcome will be shown, default value is 100.

        detailedlist : string
            String with true or false, if true extension details will be shown.
        

        Returns
        -------
        string
            Parameters string specific for the given  searchoperation to be added to the URL endpoint the e.g.: '?query='searchstring&title=title&...&detailedList=true'.
        """

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

        """Generates the URL endpoint for searching a query.

        Generates the string of the URL endpoint to searching for queries. 

        Note
        ----
        All parameters can be passed to the function as lists and will be reformated to be accepted by Openspecimen.
        Parameters permissible to be lists are marked as such within the parameters section.

        Parameters
        ----------
        cpid : string or int
            ID of the Collection Protocol, where the query is assigned to. Gets converted to a string.

        searchstring : string
            Substring of the query-title.

        start : string or int
            Defines the startrow, of the search outcome. Default is 0, gets converted to a string.

        max_ : string or int
            Max results to displayed, default value is 100. Gets converted to a string.

        countreq : true/false
            String with true or false. If true shows the total number of saved queries.

        Returns
        -------
        string
            The URL endpoint to search for queries.
        """

        url_string = '?'

        if cpid != None:
            url_string += _write_instance(entity = 'cpId', value = cpid)
        
        if searchstring != None:
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

        """Generates the searchstring for Specimens

        This function generates the string to search for collection protocols, with the permissable values from OpenSpecimen. 
        The values can be lists, they are handled as a logical OR. The values not passed to the function will be ignored.

        Note
        ----
        All parameters can be passed to the function as lists and will be reformated to be accepted by Openspecimen.
        Parameters permissibke to be lists are marked as such within the paramters section.

        Parameters
        ----------
        label : string or list
            The label of the specimen. If a list is passed it searches for multiple labels (logical OR)

        cprid : string or int
            The Collection Protocol Registration ID of the specimen. Gets converted to a string.

        enventid : string or int
            The Event ID of the anticipated Specimen. If searching with cprid the eventid or visitid is mandatory.

        visitid : string or int
            The Visit ID of the anticipated Specimen. If searching with cprid the eventid or visitid is mandatory.
        
        maxres : string or int
            The maximum results to display as int or string, gets converted to a string. The default value is 100.
        
        exact : string
            Openspecimen's boolean true/false. If true, the search parameters have to match exactly.
        
        extensions : string
            Openspecimen's boolean value true/false. If true, the extensionDetails will be shown in the results.

        Returns
        -------
        string
            String of the URL endpoint for searching after specimens.
        """

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

        """Generates the URL endpoint for deleting Specimens

        Generates the string of the URL endpoint for deleting one or more specimens.
        Looks like '?id=specimenid1,...,specimenidx'

        Parameters
        ----------
        specimenids : string/int or list of string/int
            The specimen IDs which one wants to delete, gets converted to a string.

        Returns
        -------
        string
            The url endpoint as string.
        """

        url_string = '?id='

        if isinstance(specimenids,list):
            for id_ in specimenids:
                url_string += str(id_) + ','
            url_string = url_string[0:-1]
        else:
            url_string += str(specimenids)

        return url_string


    def search_visit_name_spr(self, visitname=None, sprnumber=None):

        """Generates the URL endpoint for searching a Visit

        Generates the string of the URL endpoint for searching one or more visits by
        the name or surgical pathology number.It looks like '?name=visitname&sprNumber=sprnumber'

        Parameters
        ----------
        visitname : string
            The visit name which one wants to get.

        sprnumber : string or int
            The surgical pathology number as int or string, gets converted to a string

        Returns
        -------
        string
            The url endpoint as string.
        """

        url_string = '?'

        if visitname!=None:
            url_string += 'visitName=' + str(visitname)

        elif sprnumber!=None:
            url_string += 'sprNumber=' + str(sprnumber)
        
        return url_string

    def search_visit_cprid(self, cprid , includestats="false"):

        """Generates the URL endpoint for searching a visit

        Generates the string of the URL endpoint for searching visits by the
        Collection Protocol Registration ID.It looks like '?cprId=cprid&includeStats=true/false'

        Parameters
        ----------
        cprid : string or int
            The Visit ID which one wants to get. Gets converted to a string.

        includestats : string
            OpenSpecimens boolean type true/false. Default is false and thus optional. 

        Returns
        -------
        string
            The url endpoint as string.
        """

        url_string = '?'
        url_string += _write_instance(entity = 'cprId', value = cprid)

        if includestats== 'true':
            url_string += _write_instance(entity = 'includeStats', value = includestats)
        
        return url_string
