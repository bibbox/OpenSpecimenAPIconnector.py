#! /bin/python3

from os_core.visit import visit
from os_core.req_util import OS_request_gen
from os_core.jsons import Json_factory
from os_core.url import url_gen
import json
import io
import pandas
import time

class visit_util:

    """Handles the API calls for Visits
    
    This class handles the API calls for OpenSpecimen Visits. It can create, update, 
    search visits with different parameters, add visits and specimens in one call.
    The outputs are JSON dicts or the Error messages as dict. 
    
    Notes
    -----
    In order to use this and also the other classes, the user has to know OpenSpecimen.
    The API calls are documented in https://openspecimen.atlassian.net/wiki/spaces/CAT/pages/1116035/REST+APIs and 
    the calls refer to this site. More details can be seen in the documentation.
    
    Example
    -------
    A code example, where the Visits are handled is in the Jupyter-Notebook::
        $ jupyter notebook main.ipynb
    """

    def __init__(self, base_url, auth):

        """Constructor of the Class visit
        
        Constructor of the class visit, can handle the basic API-calls
        of the Visits in OpenSpecimen. It also connects this class to the os_core classes
        visit, Json_factory, url_gen.
        
        Parameters
        ----------
        base_url : string
            URL to openspecimen, has the format: http(s)://<host>:<port>/openspecimen/rest/ng
        auth : tuple
            Consits of two strings ( loginname , password)
        """ 

        self.visit = visit(base_url=base_url, auth=auth)
        self.jsons = Json_factory()
        self.url = url_gen()


    def add_visit(self, name, site, eventid=None, eventlabel=None, cprid= None, ppid=None, cptitle=None, cpshorttitle=None,
                        cpid=None, diagnosis=None, clinicalstatus=None, activity=None, visitstatus="COMPLETE", missedreason=None,
                        missedby=None, comments=None,pathologynumber=None,cohort=None, visitdate=None):
        
        """Add a visit to a Participant.
        
        Add a visit to a participant in OpenSpecimen via API call. To use this function, one has to know the
        Parameters of the Participant, event and site.

        Note
        ----
        Mandatory fields are -cprId or (ppid and cpTitle) or (ppid and cpShortTitle) or (ppid and cpid)
        - name, site     

        Parameters
        ----------
        name : string
            Name of the Visit.
        
        site : string
            Site to which the Visit belongs.
        
        eventid : int
            ID of the event to which the visit belongs.[optional]
        
        eventlabel : string
            Label of the event to which the visit belongs.[optional]
        
        cprid : int
            Identifier of the Collection Protocoll Registration to which the Visit belongs.
            cprid or (cptitle and ppid) or (cpid and ppid) or (cpshorttitle and ppid) are mandatory.

        ppid : string
            Identifier of the Participant to whom the Visit belongs.
            cprid or (cptitle and ppid) or (cpid and ppid) or (cpshorttitle and ppid) are mandatory.
        
        cptitle : string
            Name of the Collection Protocol.
            cprid or (cptitle and ppid) or (cpid and ppid) or (cpshorttitle and ppid) are mandatory.
        
        cpshorttitle : title
            Acronym of the Collection Protocol.
            cprid or (cptitle and ppid) or (cpid and ppid) or (cpshorttitle and ppid) are mandatory.
        
        cpid : int
            Identifier of the Collection Protocol.
            cprid or (cptitle and ppid) or (cpid and ppid) or (cpshorttitle and ppid) are mandatory.

        diagnosis : string
            Name of the diagnoses of the visit.
        
        clinicalstatus : string
            Clinical Status of the visit.[optional]
        
        activity : string
            Activity Status of the Visit.[optional]

        visitstatus : string
            Status of the visit.[optional]

        missedreason : string
            Reason why the visit was missed.[optional]

        missedby : string
            Details of the person who missed the visit.[optional]

        comments : string
            Commets regarding the visit.[optional]
        
        pathologynumber : string
            Surgical Pathology number. [optional]
        
        cohort : string
            Cohorts to which the Visit belongs. [optional]

        visitdate : string
            Date when the visit will occur, if empty takes the current date.[optional]

        Returns
        -------
        dict
            Details of the visit as JSON dict or the Openspecimen's error message.
        """

        vis = self.jsons.add_visit_json(cprid=cprid, name=name, site=site, eventid=eventid, eventlabel=eventlabel, ppid=ppid, cptitle=cptitle, 
                                        cpshorttitle=cpshorttitle, diagnosis=diagnosis,clinicalstatus=clinicalstatus, activity=acitivity,
                                        visitstatus=visitstatus, missedreason=missedreason, missedby=missedby, comments=comments,
                                        pathologynumber=pathologynumber, cohort=cohort, visitdate=visitdate, cpid=cpid)
        r = self.visit.add_visit(params = vis)

        return r


    def add_visit_speci(self, cprid, name, lineage, visit_id, av_qty, user, init_qty, spec_class, spec_type, anat_site,
                        site, speclabel, eventid=None,eventlabel=None,ppid=None, cptitle=None, cpshorttitle=None,
                        diagnosis=None, clinicalstatus=None, acitivity=None, visitstatus=None, missedreason=None,
                        missedby=None, comments=None,pathologynumber=None,cohort=None, visitdate=None, cpid=None,                         
                        stor_loc=None, status="Collected", cont=None, proced=None, qual="Acceptable", concent=None,  
                        path=None, laterality=None, visitDate=None):

        vis = self.jsons.add_visit_json(cprid=cprid, name=name, site=site, eventid=eventid, eventlabel=eventlabel, ppid=ppid, cptitle=cptitle, 
                                        cpshorttitle=cpshorttitle, diagnosis=diagnosis,clinicalstatus=clinicalstatus, activity=acitivity,
                                        visitstatus=visitstatus, missedreason=missedreason, missedby=missedby, comments=comments,
                                        pathologynumber=pathologynumber, cohort=cohort, visitdate=visitdate, cpid=cpid)
        
        speci = self.jsons.create_spec_json(lineage=lineage,  av_qty=av_qty, user=user, visitDate=visitdate, init_qty=init_qty, visit_id=None,
                                        spec_class=spec_class, spec_type=spec_type, anat_site=anat_site, stor_loc=stor_loc, label=speclabel,
                                        status=status, cont=cont, proced=proced, qual=qual, concent=concent, path=path, laterality=laterality)
        
        vis = json.loads(vis)
        speci= json.loads(speci)
        
        params={}
        params={"visit":vis,
            "specimens":[speci]}
        
        params=json.dumps(params)

        r = self.visit.add_visit_specimen(params)

        return r
    

    def update_visit(self, visitid, name, site, eventid=None, eventlabel=None, cprid= None, ppid=None, cptitle=None, cpshorttitle=None,
                        diagnosis=None, clinicalstatus=None, activity=None, visitstatus=None, missedreason=None,
                        missedby=None, comments=None,pathologynumber=None,cohort=None, visitdate=None, cpid=None):
        
        vis = self.jsons.add_visit_json(cprid=cprid, name=name, site=site, eventid=eventid, eventlabel=eventlabel, ppid=ppid, cptitle=cptitle, 
                                        cpshorttitle=cpshorttitle, diagnosis=diagnosis,clinicalstatus=clinicalstatus, activity=acitivity,
                                        visitstatus=visitstatus, missedreason=missedreason, missedby=missedby, comments=comments,
                                        pathologynumber=pathologynumber, cohort=cohort, visitdate=visitdate, cpid=cpid)
        r = self.visit.update_visit(visitid = visitid, params = vis)

        return r

    def search_visit_namespr(self, visitname=None, sprnumber=None):

        searchstring = self.url.search_visit_name_spr(visitname = visitname, sprnumber = sprnumber)

        r = self.visit.get_visit_namespr(search_string =searchstring)

        return r
    
    def search_visit_cprid(self, cprid, includestats = "false"):

        searchstring = self.url.search_visit_cprid(cprid = cprid, includestats = includestats)
        r = self.visit.get_visits_cpr(search_string = searchstring)

        return r
        

