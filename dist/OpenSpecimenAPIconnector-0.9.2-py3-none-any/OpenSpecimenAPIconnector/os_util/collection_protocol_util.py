#! /bin/python3

from ..os_core.collection_protocol import collection_protocol
from ..os_core.jsons import Json_factory
from ..os_core.url import url_gen

import pandas as pd
import json

class collection_protocol_util:

    """Utility class for Site API calls

    This class handles the API calls for OpenSpecimen Collection Protocol. It can create, update, 
    search  and merge  Protocols.
    The output is a JSON dict or the Error message as JSON dict, except the Pandas dataframe.

    Note
    -----
    In order to use this and also the other classes, the user has to know OpenSpecimen. In the core classes one can
    just pass the parameters via JSON-formatted string. This means the user has to know the keywords.
    The API calls are documented in https://openspecimen.atlassian.net/wiki/spaces/CAT/pages/1116035/REST+APIs and 
    the calls refer to this site. More details can be seen in the documentation.

    Examples
    --------

    A code Examples, where the Collection protocols are handled is in the Jupyter-Notebook

        $ jupyter notebook main.ipynb
    """

    def __init__(self):

        """Constructor of the Class collection_protocol_util

        Constructor of the class colelction_protocol, can handle the basic API-calls
        of the collection protocol in OpenSpecimen. Connects this class to OpenSpecimen
        specific request handle (os_core.request_util.py) and the os_core classes
        Json_fatory, url_gen and collection_protocol

        Parameters
        ----------
        base_url : string
            URL to openspecimen, has the format: http(s)://<host>:<port>/openspecimen/rest/ng
        auth : tuple
            Consits of two strings ( loginname , password)
        """

        self.jsons = Json_factory()
        self.urls = url_gen()
        self.cps = collection_protocol()

  
    def search_cps(self, searchstring = None, title = None, piid = None, reponame = None, startat = None, maxresults = None, detailedlist = None):

        """Search for Colelction Protocols with specific values.

        Search for one or more Collection Protocols with the search_string defined. The search string looks like:
        http(s)://<host>:<port>/openspecimen/rest/np/collection-protocols?{param_1}={value_1}&...&{param_x}={value_x}
        With the class collection_protocol_util from os_util and function <search_cps> the search string is generated
        and this function is called. Not all keys from OpenSpecimen can be easily searched after.

        Parameters
        ----------
        search_string : string
            openSpecimen's Advanced Query Language[optional]. Substring of the title or shorttitle

        title : string
            Name of the desired Collection Protocol
        
        ppid : string or int
            Id of the Pricincipal Investigator, gets converted to a string[optional].
        
        reponame : string
            Name of the Repository in which the Collection Protocol is[optional].
        
        startat : int
            Value which one of the outcomes is the first to show, if not specified OpenSpecimen takes 0.
        
        maxresults : int
            Value how many Collection Protocols are shown, if not specified OpenSpecimen takes 100.
        
        detailedList: string
            String in OpenSpecimen's boolean format, permissable values are true/false. If not specified, OpenSpecimen takes false.

        Returns
        -------
        JSON-dict
            [Details of the matching Collection Protocols, if no one matches it is an empty list.
        """

        search_string = self.urls.cp_search_url_gen(searchstring = searchstring, title = title, piid = piid, reponame = reponame,
                                                    startat = startat, maxresults = maxresults, detailedlist = detailedlist)

        r = self.cps.search_collection_protocols(search_string = search_string)

        return r

    def merge_cps(self, src_cp, trg_cp):

        """Merge two Collection protocols

        Merge two Colelction Protocols which are defined in src_cp and trg_cp together. To call this function the short titles of
        the source and target collection protocol has to be known. The merged Protocol is the one with short title tgtCpShortTitle,
        with merge logic outer. 

        Note
        ----
        Merging is restricted to Super Admins. The CPs must have the same format for PPI, visits and specimens. Or the target CP 
        has no specific formats. 

        Parameters
        ----------
        src_cp : string
            String with the shortTitle of the source collection Protocol.
        
        trgcp : string
            String with the shortTitle of the target collection Protocol.

        Returns
        -------
        JSON-dict
            JSON dict with the short titles of the source and target Colelction Protocols.
        """

        data = self.jsons.merge_cps(src_cp = src_cp, trg_cp = trg_cp)
        r = self.cps.merge_colelction_protocols(params = data)

        return r


    def create_cp(self, short_title , title, pi_mail, sites, time_start=None, time_end=None,  man_id=None, coords=None,
                           consentsWaived=None,eth_cons_id=None, part_no=None, desc_url=None, visitNameFmt=None, specimenLabelFmt=None, 
                           derivativeLabelFmt =None, man_visit_name=None, man_spec_label=None, aliquots_in_same=None, activity=None,
                           aliquotLabelFmt = None, ppidFmt= None, specimenCentric = None):
        
        """Create a Collection protocol with the given Parameters
        
        Create a collection protocol with the Parameters passed to the function.

        Parameters
        ----------
        short_title : string
            Short title of the Collection Protocol.

        title : string
            Title of the Collection Protocol.

        pi_mail : string
            Email Address of the Principal Investigator.
        
        time_start: string
            String with the start_time of the collection Protocol in the timeformat specified in the System configuration.
        
        time_end: string
            String with the end_time of the collection Protocol in the timeformat specified in the System configuration.

        sites: list
            Sites which are assigned to the collection Protocl.
        
        man_id : string
            OpenSpecimen's boolean true/false if the manual PPID creation is enabled.

        coords: dict
            dict with Coordinators and coordinator ids in it.

        consentsWaived : string
            OpenSpecimen's boolean true/false if consent should be waived.

        eth_cons_id : string
            Ethical aproavel id.

        part_no : string
            String with number of anticipated Participant count.

        desc_url = string
            URL with the decription of the Collection Protocol.
        
        visitNameFMT : string
            String which contains the OpenSpecimen's token for creating Visit Names automatically.

        man_visit_name : string
            String with OpenSpecimen's boolean format if the Visits should be created manually.
        
        man_spec_label : string
            String with OpenSpecimen's boolean format if the Specimen Labels should be created manually.
        
        man_spec_label : string
            String with OpenSpecimen's boolean format if the Aliquotes are stored in the same Container.
        
        activity : string
            String with the acitivity status of the Specimen.
        
        Returns
        -------
        dict
            Details of the created Collection Protocol, or the OpenSpecimen's error message.
        """

        data = self.jsons.create_CP_json(short_title=short_title, title=title, pi_mail=pi_mail, time_start=time_start, time_end=time_end,
                    sites=sites, man_id=man_id, coords=coords, consentsWaived=consentsWaived, eth_cons_id=eth_cons_id, part_no=part_no,
                    desc_url=desc_url, visitNameFmt=visitNameFmt, specimenLabelFmt=specimenLabelFmt, derivativeLabelFmt=derivativeLabelFmt,
                    man_visit_name=man_visit_name, man_spec_label=man_spec_label, aliquots_in_same=aliquots_in_same, activity=activity,
                    aliquotLabelFmt=aliquotLabelFmt, ppidFmt=ppidFmt, specimenCentric=specimenCentric)

        r = self.cps.create_collection_protocol(data = data)

        return r
    
    def update_cp(self, cpid, short_title = None, title=None, pi_mail=None, time_start=None, time_end=None, sites=None, man_id=False, coords=None,
                           consentsWaived=None,eth_cons_id=None, part_no=None, desc_url=None, visitNameFmt=None, specimenLabelFmt=None, 
                           derivativeLabelFmt =None, man_visit_name=False, man_spec_label=True, aliquots_in_same=None, activity=None,
                           aliquotLabelFmt = None, ppidFmt= None, specimenCentric = None):

        """Update a Collection protocol with the given Parameters.
        
        Update a collection protocol with the Parameters passed to the function. The Collection protocol ID 
        cpid is mandatory.

        Note
        -----
        The parameters except cpid are mandatory. All values not passed will not get changed.
        
        Parameters
        ----------
        cpid : int
            ID of the Colelction Protocol which should get updated.

        short_title : string
            Short title of the Collection Protocol.

        title : string
            Title of the Collection Protocol.

        pi_mail : string
            Email Address of the Principal Investigator.
        
        time_start: string
            String with the start_time of the collection Protocol in the timeformat specified in the System configuration.
        
        time_end: string
            String with the end_time of the collection Protocol in the timeformat specified in the System configuration.

        sites: list
            Sites which are assigned to the Collection Protocl.
        
        man_id : string
            OpenSpecimen's boolean true/false if the manual PPID creation is enabled.

        coords: dict
            dict with Coordinators and coordinator ids in it.

        consentsWaived : string
            OpenSpecimen's boolean true/false if consent should be waived.

        eth_cons_id : string
            Ethical aproavel id.

        part_no : string
            String with number of anticipated Participant count.

        desc_url = string
            URL with the decription of the Collection Protocol.
        
        visitNameFMT : string
            String which contains the OpenSpecimen's token for creating Visit Names automatically.

        man_visit_name : string
            String with OpenSpecimen's boolean format if the Visits should be created manually.
        
        man_spec_label : string
            String with OpenSpecimen's boolean format if the Specimen Labels should be created manually.
        
        man_spec_label : string
            String with OpenSpecimen's boolean format if the Aliquotes are stored in the same Container.
        
        activity : string
            String with the acitivity status of the Specimen.
        
        Returns
        -------
        dict
            Details of the created Collection Protocol, or the OpenSpecimen's error message.
        """
    
        params = self.jsons.create_CP_json(cpid =cpid, short_title=short_title, title=title, pi_mail=pi_mail, time_start=time_start, time_end=time_end,
                    sites=sites, man_id=man_id, coords=coords, consentsWaived=consentsWaived, eth_cons_id=eth_cons_id, part_no=part_no,
                    desc_url=desc_url, visitNameFmt=visitNameFmt, specimenLabelFmt=specimenLabelFmt, derivativeLabelFmt=derivativeLabelFmt,
                    man_visit_name=man_visit_name, man_spec_label=man_spec_label, aliquots_in_same=aliquots_in_same, activity=activity,
                    aliquotLabelFmt=aliquotLabelFmt, ppidFmt=ppidFmt, specimenCentric=specimenCentric)
        
        r = self.cps.update_collection_protocol(cpid =cpid, params = params)

        return r


