#! /bin/python3

from ..os_core.site import sites
from ..os_core.jsons import Json_factory
from ..os_core.url import url_gen

import pandas as pd
import json

class site_util:

    """Handles the calls for sites
    
    This class handles the API calls for OpenSpecimen Sites. It can create, update and search 
    sites with different parameters. The other calls are in the os_core class sites.
    
    Note
    -----
    In order to use this and also the other classes, the user has to know OpenSpecimen. 
    The API calls are documented in https://openspecimen.atlassian.net/wiki/spaces/CAT/pages/1116035/REST+APIs and 
    the calls refer to this site. More details can be seen in the documentation.
    
    Examples
    --------
    A code Examples, where the collection protocols are handled is in the Jupyter-Notebook
        $ jupyter notebook main.ipynb
    """

    def __init__(self):

        """Constructor of the Class sites

        Constructor of the class sites, can handle the basic API-calls
        of the sites in OpenSpecimen. It connects this class to OpenSpecimen
        specific request handle (os_core.request_util.py). Also it connects this class
        to the os_core classes, url_gen, Json_factory and sites.

        
        Parameters
        ----------
        base_url : string
            URL to openspecimen, has the format: http(s)://<host>:<port>/openspecimen/rest/ng
        auth : tuple
            Consists of two strings ( loginname , password)
        """
        
        self.jsons = Json_factory()
        self.urls = url_gen()
        self.sites = sites()

    def search_sites(self, sitename = None, institutename = None, maxresults = 100, siteExtension=True):

        """Search for Sites with specific values.

        Search for one or more sites with the values in search_string defined. The search string looks like:
        http(s)://<host>:<port>/openspecimen/rest/np/sites?{param_1}={value_1}&...&{param_x}={value_x}
        This string gets generated here. If siteExtension is true, the detailed site parameters will get returned.
        
        Parameters
        ----------
        sitename : string
            Substring of the sitenames.

        institutename : string
            Substring of the Institutenames
        
        maxresults : int
            Defines how many results will get returned maximally.

        siteExtension : boolean
            If true, returns also the extension details.
            
        Returns
        -------
        JSON-dict
            Details of the matching sites, if no one matches it is an empty list.
        """

        search_string = self.urls.site_search_url_gen(sitename = sitename, institutename = institutename, maxresults = maxresults)     
        r = self.sites.search_sites(search_string = search_string)

        if siteExtension:
            si =[]
            for obj in r:
                siteid=obj['id']
                si.append(self.sites.get_site(siteid = siteid))
            r = si

        return r

    
    def create_sites(self, name, institutename, type_, coordinators = None, address = None):
        
        """Create a site in OpenSpecimen
        
        Create a site in OpenSpecimen with an API call. 
        
        Parameters
        ----------
        name : string
            Name of the site.

        institutename : string
            Name of the institute where the site belongs to.
        
        type_ : string
            Type of the site, permissable values are: collection site, repository, laboratory, not specified.
        
        coordiantors : dict
            Dict with identifier of coordinators.[optional]

        address : string
            String with the Address of the site[optional].
        
        Returns
        -------
        dict
            Details of the created site as dictionary or the OpenSpecimen's error message.
        """ 
        params = self.jsons.create_site(name = name, institutename = institutename, type_ = type_,
                coordinators = coordinators, address = address)
        r = self.sites.create_sites(params = params)

        return r


    def update_sites(self, siteid, name = None, institutename = None, type_ = None, coordinators = None, address = None):
        
        """Update a site in OpenSpecimen
        
        Update a site in OpenSpecimen with an API call. In order to update a site one has to know
        the ID of the site which can be seen in the GUI, by clicking on the site, the URL looks like:
        http(s)://<host>:<port>/openspecimen/sites/{siteid}/overview. Or it can be first searched for,
        for Examples, by name with the function search_sites and then the ID can be extracted from there.
                
        Parameters
        ----------
        siteid : int
            Unique Identifier of the Site

        name : string
            Name of the Site.

        institutename : string
            Name of the institute where the site belongs to.
        
        type_ : string
            Type of the site, permissable values are: collection site, repository, laboratory, not specified.
        
        coordiantors : dict
            Dict with identifier of coordinators.[optional]

        address : string
            String with the Address of the site[optional].
        
        Returns
        -------
        dict
            Details of the created site as dictionary or the OpenSpecimen's error message.
        """ 
        params = self.jsons.create_site(name = name, institutename = institutename, type_ = type_,
                coordinators = coordinators, address = address)
        r = self.sites.update_site(siid = siteid, params = params)

        return r

