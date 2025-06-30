#! /bin/python3

from ..os_core.visit import visit
from ..os_core.jsons import Json_factory
from ..os_core.url import url_gen
import json
import io
import pandas
import time

class visit_util:

    """Handles the API calls for Visits

    This class handles the API calls for OpenSpecimen Visits. It can create, update, 
    search visits with different parameters, add visits and specimens in one call.
    The outputs are JSON dicts or the Error messages as dict. 

    Note
    -----
    In order to use this and also the other classes, the user has to know OpenSpecimen.
    The API calls are documented in https://openspecimen.atlassian.net/wiki/spaces/CAT/pages/1116035/REST+APIs and 
    the calls refer to this site. More details can be seen in the documentation.

    Examples
    --------
    A code Examples, where the visits are handled is in the Jupyter-Notebook
        $ jupyter notebook main.ipynb
    """

    def __init__(self):

        """Constructor of the Class visit
        
        Constructor of the class visit, can handle the basic API-calls
        of the visits in OpenSpecimen. It also connects this class to the os_core classes
        visit, Json_factory, url_gen.
        
        Parameters
        ----------
        base_url : string
            URL to openspecimen, has the format: http(s)://<host>:<port>/openspecimen/rest/ng
        auth : tuple
            Consists of two strings ( loginname , password)
        """ 

        self.visit = visit()
        self.jsons = Json_factory()
        self.url = url_gen()


    def add_visit(self, name, site, eventid=None, eventlabel=None, cprid= None, ppid=None, cptitle=None, cpshorttitle=None,
                        cpid=None, diagnosis=None, clinicalstatus=None, activity=None, visitstatus="Complete", missedreason=None,
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
            Site to which the Visit belongs to.

        eventid : int
            ID of the event to which the visit belongs to.[optional]

        eventlabel : string
            Label of the event to which the visit belongs to.[optional]

        cprid : int
            Identifier of the Collection Protocoll Registration to which the visit belongs to.
            cprid or (cptitle and ppid) or (cpid and ppid) or (cpshorttitle and ppid) are mandatory.

        ppid : string
            Identifier of the Participant to whom the visit belongs to.
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
            Comments regarding the visit.[optional]

        pathologynumber : string
            Surgical Pathology number. [optional]

        cohort : string
            Cohorts to which the visit belongs to. [optional]

        visitdate : string
            Date when the visit will occur, if empty takes the current date.[optional]

        Returns
        -------
        dict
            Details of the visit as JSON dict or the Openspecimen's error message.
        """

        vis = self.jsons.add_visit_json(cprid=cprid, name=name, site=site, eventid=eventid, eventlabel=eventlabel, ppid=ppid, cptitle=cptitle, 
                                        cpshorttitle=cpshorttitle, diagnosis=diagnosis,clinicalstatus=clinicalstatus, activity=activity,
                                        visitstatus=visitstatus, missedreason=missedreason, missedby=missedby, comments=comments,
                                        pathologynumber=pathologynumber, cohort=cohort, visitdate=visitdate, cpid=cpid)
        
        r = self.visit.add_visit(params = vis)

        return r


    def add_visit_speci(self,  name, lineage, av_qty, user, init_qty, spec_class, spec_type, anat_site, site, path,
                        speclabel = None, eventid=None, eventlabel=None, cprid = None, ppid=None, cptitle=None, cpshorttitle=None,
                        cpid = None, diagnosis=None, clinicalstatus=None, activity=None, visitstatus=None, missedreason=None,
                        missedby=None, comments=None, pathologynumber=None, cohort=None, visitdate=None, laterality=None, rec_qlt = None,                        
                        colltime = None, rectime = None, status="Collected", stor_name=None, storlocx =None, storlocy =None, concentration=None, 
                        biohazrad = None, collproc=None, conttype = None, extensionudn = None, extensionmap = None,
                        extensiondict = None):

        """Add a visit and a specimen in one call.
        
        Add a visit and a specimen in OpenSpecimen via one API call. To use this function, one has to know the
        Parameters of the participant, event and site.

        Note
        ----
        Mandatory fields are -cprId or (ppid and cpTitle) or (ppid and cpShortTitle) or (ppid and cpid)
        - name, site
        The label is mandatory if the Protocolsettings are such that the Label is created manually, otherwise
        it has to be left empty.  

        Parameters
        ----------
        cprid : int
            Identifier of the Collection Protocoll Registration to which the visit belongs to.
            cprid or (cptitle and ppid) or (cpid and ppid) or (cpshorttitle and ppid) are mandatory.

        name : string
            Name of the Visit.
        
        lineage : string
            Lineage of the specimen, if created it is New.
        
        av_qty : int
            The available quantity of a specimen.
        
        user : int
            ID of the user who creates the specimen. If not specified the API user is taken.
        
        init_qty : int
            The initial quantity of a specimen.

        spec_class : string
            Class of the specimen.
        
        spec_type : string
            Type of the specimen, belongs to the class.
        
        anat_site : string
            The anatomic site of the specimen.

        site : string
            Site to which the visit belongs to.
        site,
        eventid : int
            ID of the event to which the visit belongs to.[optional]
        
        eventlabel : string
            Label of the event to which the visit belongs to.[optional]
        
        ppid : string
            Identifier of the Participant to whom the visit belongs to.
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
        
        activity : stringsite,
            Activity Status of the visit.[optional]

        visitstatus : string
            Status of the visit.[optional]

        missedreason : string
            Reason why the visit was missed.[optional]

        missedby : string
            Details of the person who missed the visit.[optional]

        comments : string
            Comments regarding the visit.[optional]
        
        pathologynumber : string
            Surgical Pathology number. [optional]
        
        cohort : string
            Cohorts to which the visit belongs to. [optional]

        visitdate : string
            Date when the visit will occur, if empty takes the current date.[optional]
        
        pathology : string
            Pathologystatus of the Specimen.
        
        laterality : string
            The laterality of the specimen.
               
        recqlt : string
            The received quality.
   
        colltime : string
            Date and Time of the collection event, the format is in the OpenSpecimen's System configuration.[optional]
            
        rectime : string
            Date and Time of the received event, the format is in the OpenSpecimen's System configuration.[optional]
                        
        status : string
            Status of the Specimen, default is 'Collected'.
        
        stor_name : string
            Name of the container. [optional]
        
        storlocx : int
            Position of the specimen in the Container in x direction.[optional]

        storlocy : int
            Position of the specimen in the container in y direction.[optional]
            
        concetration  : int
            Concentration of the specimen[optional].
        
        biohazard : string
            Biohazards of that specimen.[optional]
                    
        comments : string
            Comments regarding to the specimen[optional].
        
        collproc : string
            The procedure of the collection[otpional].

        conttype : string
            Type of the storage container.
            
        extensionudn : string
            OpenSpecimen's boolean true/false. If true, the extension keys are the udn values of the corresponding form.[optional]
        
        extensionmap : string
            The name of the form which should be taken.[optional]

        extensiondict : dict
            The dictionary of the extensions, has to be created manually. Either with udn or name (as defined before). [optional]

        Returns
        -------
        dict
            Details of the visit and specimen as JSON dict or the Openspecimen's error message.
        """

        vis = self.jsons.add_visit_json(cprid=cprid, name=name, site=site, eventid=eventid, eventlabel=eventlabel, ppid=ppid, cptitle=cptitle, 
                                        cpshorttitle=cpshorttitle, diagnosis=diagnosis,clinicalstatus=clinicalstatus, activity=activity,
                                        visitstatus=visitstatus, missedreason=missedreason, missedby=missedby, comments=comments,
                                        pathologynumber=pathologynumber, cohort=cohort, visitdate=visitdate, cpid=cpid)
        
        if stor_name!=None:
            storloc = self.jsons.storage_location_json(name= stor_name, xpos=storlocx, ypos= storlocy)
        else:
            storloc=None

        speci = self.jsons.create_specimen_json(lineage=lineage,  avaqty=av_qty, userid=user, initqty=init_qty, colltime=colltime,
                                        specimenclass=spec_class, specimentype=spec_type, anatomic=anat_site, storloc = storloc,
                                        label=speclabel, status=status, conttype = conttype, collproc=collproc, recqlt=rec_qlt,
                                        concentration=concentration, pathology=path, laterality=laterality, rectime=rectime)

        vis = json.loads(vis)
        speci= json.loads(speci)

        params={}
        params={"visit":vis,
            "specimens":[speci]}

        params=json.dumps(params)
        
        r = self.visit.add_visit_specimen(params)

        return r
    

    def update_visit(self, visitid, name = None, site = None, eventid=None, eventlabel=None, cprid= None, ppid=None, cptitle=None, 
                    cpshorttitle=None, diagnosis=None, clinicalstatus=None, activity=None, visitstatus=None, missedreason=None,
                    missedby=None, comments=None, pathologynumber=None, cohort=None, visitdate=None, cpid=None):
        
        """Updating a visit

        Update an existing visit with ID visitid and the parameters params. All parameters are
        optional for updating and  those which are not passed stay the same. Those parameters and 
        the visit Id have to be known to use this function and can
        be found out in the GUI by clicking on a participant and the visit. It looks like:
        http(s)://<host>:<port>/openspeicmen/cp-view/{cpid}/participant/{cprid}/visits/detail/ocerview?visitId={visitid}&eventId={eventId} .
        Or via the function get_visit_namespr, when one knows the name of the visit and then extracts the id from there.

        Note
        ----
        All parameters are optional, except the visitid. The parameters which are not passed will stay the same.

        Parameters
        ----------
        visitid : int 
            Id of the visit, gets converted to a string
        
        name : string
            Name of the visit.
        
        site : string
            Site to which the visit belongs to.
        
        eventid : int
            ID of the event to which the visit belongs to.[optional]
        
        eventlabel : string
            Label of the event to which the visit belongs to.[optional]
        
        cprid : int
            Identifier of the Collection Protocoll Registration to which the visit belongs to.
            cprid or (cptitle and ppid) or (cpid and ppid) or (cpshorttitle and ppid) are mandatory.

        ppid : string
            Identifier of the Participant to whom the visit belongs to.
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
            Activity Status of the visit.[optional]

        visitstatus : string
            Status of the visit.[optional]

        missedreason : string
            Reason why the visit was missed.[optional]

        missedby : string
            Details of the person who missed the visit.[optional]

        comments : string
            Comments regarding the visit.[optional]
        
        pathologynumber : string
            Surgical Pathology number. [optional]
        
        cohort : string
            Cohorts to which the visit belongs to. [optional]

        visitdate : string
            Date when the visit will occur, if empty takes the current date.[optional]

        Returns
        -------
        dict
            JSON-dict with details of the updated visit or OpenSpecimens Error message
        """
        
        vis = self.jsons.add_visit_json(cprid=cprid, name=name, site=site, eventid=eventid, eventlabel=eventlabel, ppid=ppid, cptitle=cptitle, 
                                        cpshorttitle=cpshorttitle, diagnosis=diagnosis,clinicalstatus=clinicalstatus, activity=activity,
                                        visitstatus=visitstatus, missedreason=missedreason, missedby=missedby, comments=comments,
                                        pathologynumber=pathologynumber, cohort=cohort, visitdate=visitdate, cpid=cpid)
        r = self.visit.update_visit(visitid = visitid, params = vis)

        return r

    def search_visit_namespr(self, visitname=None, sprnumber=None):

        """Get a Visit by the name or the Surgical pathology number

        Get one or more visits by the name or the surgical pathology number. Those parameters have to be known 
        in order to know this function. If just the visitname is passed, one returns a visit with the corresponding name.
        If just the surgical pathology number is passed it returns all visits with this number. If both are passed
        it works as logical AND.

        Parameters
        ----------
        visitname : string
            Substring of the name of the visit.

        sprnumber : string
            Surgical Pathology number of the visits.

        Returns
        -------
        dict
            JSON-dict with details of the visits.
        """

        searchstring = self.url.search_visit_name_spr(visitname = visitname, sprnumber = sprnumber)

        r = self.visit.get_visit_namespr(search_string =searchstring)

        return r
    
    def search_visit_cprid(self, cprid, includestats = "false"):
        
        """Get a Visit by the Collection protocol Registration Id.

        Get a visit by the Collection Protocoll Registration ID. Those parameters have to be known 
        in order to know this function. They can be extracted from calling a search function in the 
        os_core class visits.

        Parameters
        ----------
        cprid : int
            Identifier of the collection protocol registration.
        
        includestats : string
            OpenSpecimen's boolean true/false. If true the stats of the participants, e.g. number of visits are included.
        
        Returns
        -------
        dict
            JSON-dict with details of the visit.
        """

        searchstring = self.url.search_visit_cprid(cprid = cprid, includestats = includestats)
        r = self.visit.get_visits_cpr(search_string = searchstring)

        return r
        

