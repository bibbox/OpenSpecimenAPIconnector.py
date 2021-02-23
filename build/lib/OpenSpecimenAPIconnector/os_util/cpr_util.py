#! /bin/python3

from ..os_core.collection_protocol_registration import collection_protocol_registration
from ..os_core.req_util import OS_request_gen
from ..os_core.jsons import Json_factory
from ..os_core.participant import participant
import json
import io
import pandas
import time

class cpr_util:

    """Handles the API calls to registrate participants to a Collection Protocol

    Handles the OpenSpecimen API calls to registrate paritcipants to a existing Collection Protocol.
    This class can create participants, register existing participants to another protocol,
    get the details of an existing participant or more existing pariticpants, update a participant.

    Notes
    -----
    In order to use this and also the other classes, the user has to know OpenSpecimen. 
    The API calls are documented in https://openspecimen.atlassian.net/wiki/spaces/CAT/pages/1116035/REST+APIs and 
    the calls refer to this site. More details can be seen in the documentation.

    Example
    -------

    A code example, where the Institutes are handled is in the Jupyter-Notebook:

        $ jupyter notebook main.ipynb
    """

    def __init__(self, base_url, auth):

        """Constructor of the Class cpr_util

        Constructor of the class cpr_util (Collection protocol Registration) can handle the  API-calls
        of the collection protocol registration in OpenSpecimen. It also connects this class to the os_core
        classes collection_protocol-registration, participant and Json_factory

        Parameters
        ----------
        base_url : string
            URL to openspecimen, has the format: http(s)://<host>:<port>/openspecimen/rest/ng
        auth : tuple
            Consits of two strings ( loginname , password)
        """

        self.cpr = collection_protocol_registration(base_url=base_url, auth=auth)
        self.participant = participant(base_url = base_url, auth = auth)
        self.jsons = Json_factory()


    def get_registrations(self, cpid = None, registrationdate = None, ppid = None, name = None, birthdate = None,
                            uid = None, specimen = None, includestats = None, startat = None, maxresults = None):

        """Search for one or more participants

        Get the details of one or more participants, which are sepecified with the parameters from the function.
        The parameters are optional and if its all empty 100 participants will get returned, default order is with PPID.

        Parameters
        ---------
        cpid : string or int
            The collection protocols Id where the participant is at.
        
        registrationdate : string
            The date of registration in the format, which is defined in the System settings.
        
        ppid : string
            The Participant protocoll ID.

        name : string
            Substring of the first, middle or last name.
        
        birthdate : string
            The date of registration in the format, which is defined in the System settings.
        
        uid : string
            Social Security Number or an other unique national ID.
        
        specimen : string
            The label or barcode of a specimen from the participant.
        
        includestats : string
            OpenSpecimen's boolean (true/false). If true it returns additional specimen, visit counts.
        
        startat : int
            Defines which line of the matches is the first to show, the rows before get ignored in the return.
        
        maxresults : int
            Defines how many rows should be displayed. OpenSpecimen's default is 100.

        Returns
        -------
        JSON-dict
            Details of the Participant, who are matching the search criteria.
        """

        params = self.jsons.get_registrations(cpid = cpid, registrationdate = registrationdate, ppid = ppid, name = name,
                        birthdate = birthdate, uid = uid, specimen = specimen, includestats = includestats, 
                        startat = startat, maxresults = maxresults)

        r = self.cpr.get_registrations(params = params)

        return r


    def get_participants(self, lastname=None, uid = None, birthdate = None, pmi = None, empi = None, reqreginfo = None):

        """Search for one or more participants

        Get the details of one or more participants, which are sepecified with the parameters from the function.
        The parameters are optional and if its all empty 100 participants will get returned, default order is with PPID.
        This function should be used before creating a participant to see if an participant is already in the system.

        Parameters
        ---------
        lastname : string
            Substring of the Lastname of a Paritcipant.
        
        uid : string
            Country specific unique social security number.

        birthdate : string
            The date of registration in the format, which is defined in the System settings.
        
        pmi : dict
            Dict with details of the Medical records number mrn and the assigned site with key siteName.

        empi : string
            Enterprise wide unique ID assigned to the participant.

               
        reqreginfo : string
            OpenSpecimen's boolean (true/false). If true it returns details of the participant
        
        Returns
        -------
        JSON-dict
            Details of the matching parameter, if reqreginfo is true return additional the participant info.
        """

        params = self.jsons.get_participants(lastname = lastname, uid = uid, birthdate = birthdate,
                                            pmi = pmi, empi = empi, reqreginfo = reqreginfo)
        r = self.participant.get_participant_matches(params)

        return r


    def create_registration(self, regdate, cpid = None, cptitle = None, cpshorttile = None, ppid = None,
                firstname = None, middlename = None, lastname = None, uid = None, birthdate = None, vitalstatus = None,
                deathdate = None, gender = None, race = None, ethnicities = None, sexgenotype = None, pmis = None,
                mrn = None, sitename = None, empi = None):
            
        """Register a participant to a Collection Protocol.

        This function can create a new participant to an already existing Collection Protocol. To use this function one
        has to known either the Colelction Protocoll id ::cpId::,the title of the Collection Protocol ::cpTitle:: or 
        the short title of the Collection Protocol ::cpshorttitle:: .
        Those values can be seen via GUI, extracted from the responses with the class collection_protocol in os_core or
        collection_protocol_util in os_util. 

        Notes
        ----- 
        Either cpid or cptitle or cpshorttitle are mandatory to identify the Collection Protocol.
        ppid has to be leaved empty if PPID is auto-generated at protocol level, else it is mandatory.
        regdate is mandatory.
        For creating a Participant, all Participant fields can be left empty, except the first five have special rules.

        Parameters
        ----------
        regdate : string
            Mandatory field with date of registration in the format which is defined in the systemsettings of openSpecimen.
        
        cpid : int
            Unique ID of the Collection Protocol, which is autogenerated from OpenSpecimen. cpid or cptitle or cpshorttile is mandatory.
        
        cptitle : string
            Unique title of the Collection Protocol. cpid or cptitle or cpshorttile is mandatory.

        cpshorttitle : string
            Unique Acronym of the Collection Protocol. cpid or cptitle or cpshorttile is mandatory.
        
        ppid : string
            Participant protocol ID, is mandatory if created manaully and have to be empty if it is autogenerated.
            This is a protocol setting.
        
        firstname : string
            Participants first name.
        
        middlename : string
            Participants middle name.
        
        lastname : string
            Participants last name.
        
        uid : string
            Unique identifier e.g. social security number.
        
        birthdate : string
            Birthdate in the format which is defined in the systemsettings of OpenSpecimen.

        vitalstatus : string
            Vital status of the Participant.
        
        deathdate : string
            Deathdate in the format which is defined in the systemsettings of OpenSpecimen.
        
        gender : string
            Gender of the participant, permissable values are Male, Female, Unknown, Unspecified.
        
        race : string
            Participants racial origination, permissable values are {American Indian or Alaska Native, Asian, black or Afro American, Native Hawaiian
            or other Pacific Islander, Not REported, Unknown, White}
        
        ethnicities : string
            Participants ethnicities, permissable values are: {Hispanic or Latino, Not Hispanic or Latino, Not Reported, Unknown}
        
        sexgenotype : string
            Participants sex Genotype, permissable values are {XX Genotype, XY Genotype, XXX, Klinefelter’s Syndrome, XXXY syndrome, 
            XXYY syndrome, Mosaic including XXXXY, Penta X syndrome}
        
        pmis : string
            Collection of the Participants medical record numner.
        
        mrn : string
            Participants medical record number.

        sitename : string
            Name of the site, where the participant is registrated.

        empi : string
            Enterprise master patient index number

        Returns
        -------
        JSON-dict
            Details of the created Participant or the OpenSpecimen error message as Dictornary.
        """

        params = self.jsons.create_participant_json(regdate = regdate, cpid = cpid, cptitle = cptitle, cpshorttitle =cpshorttitle,
                        ppid = ppid, firstname = firstname, middlename = middlename, lastname = lastname, uid = uid,
                        birthdate = birthdate, vitalstatus = vitalstatus, deathdate = deathdate, gender = gender,
                        race = race, ethnicities = ethnicities, sexgenotype = sexgenotype, pmis = pmis, mrn = mrn,
                        sitename = sitename, empi =empi)
        r = self.cpr.create_participant(params)

        return r


    def update_registration(self, regdate, cprid, cpid = None, cptitle = None, cpshorttile = None, ppid = None,
            firstname = None, middlename = None, lastname = None, uid = None, birthdate = None, vitalstatus = None,
            deathdate = None, gender = None, race = None, ethnicities = None, sexgenotype = None, pmis = None,
            mrn = None, sitename = None, empi = None):
            
        """Register a participant to a Collection Protocol.

        This function can create a new participant to an already existing Collection Protocol. To use this function one
        has to known either the Colelction Protocoll id ::cpId::,the title of the Collection Protocol ::cpTitle:: or 
        the short title of the Collection Protocol ::cpshorttitle:: .
        Those values can be seen via GUI, extracted from the responses with the class collection_protocol in os_core or
        collection_protocol_util in os_util.  For updating a participant the cprid has to be known. This can be seen via GUI
        or with searching the participant first.

        Notes
        ----- 
        Either cpid or cptitle or cpshorttitle are mandatory to identify the Collection Protocol.
        ppid has to be leaved empty if PPID is auto-generated at protocol level, else it is mandatory.
        regdate is mandatory.
        For creating a Participant, all Participant fields can be left empty, except the first five have special rules.

        Parameters
        ----------
        regdate : string
            Mandatory field with date of registration in the format which is defined in the systemsettings of openSpecimen.

        cprid : int
            Unique ID of the Participant's Registration.
        
        cpid : int
            Unique ID of the Collection Protocol, which is autogenerated from OpenSpecimen. cpid or cptitle or cpshorttile is mandatory.
        
        cptitle : string
            Unique title of the Collection Protocol. cpid or cptitle or cpshorttile is mandatory.

        cpshorttitle : string
            Unique Acronym of the Collection Protocol. cpid or cptitle or cpshorttile is mandatory.
        
        ppid : string
            Participant protocol ID, is mandatory if created manaully and have to be empty if it is autogenerated.
            This is a protocol setting.
        
        firstname : string
            Participants first name.
        
        middlename : string
            Participants middle name.
        
        lastname : string
            Participants last name.
        
        uid : string
            Unique identifier e.g. social security number.
        
        birthdate : string
            Birthdate in the format which is defined in the systemsettings of OpenSpecimen.

        vitalstatus : string
            Vital status of the Participant.
        
        deathdate : string
            Deathdate in the format which is defined in the systemsettings of OpenSpecimen.
        
        gender : string
            Gender of the participant, permissable values are Male, Female, Unknown, Unspecified.
        
        race : string
            Participants racial origination, permissable values are {American Indian or Alaska Native, Asian, black or Afro American, Native Hawaiian
            or other Pacific Islander, Not REported, Unknown, White}
        
        ethnicities : string
            Participants ethnicities, permissable values are: {Hispanic or Latino, Not Hispanic or Latino, Not Reported, Unknown}
        
        sexgenotype : string
            Participants sex Genotype, permissable values are {XX Genotype, XY Genotype, XXX, Klinefelter’s Syndrome, XXXY syndrome, 
            XXYY syndrome, Mosaic including XXXXY, Penta X syndrome}
        
        pmis : string
            Collection of the Participants medical record numner.
        
        mrn : string
            Participants medical record number.

        sitename : string
            Name of the site, where the participant is registrated.

        empi : string
            Enterprise master patient index number.

        Returns
        -------
        JSON-dict
            Details of the updated Participant or the OpenSpecimen error message as Dictornary.
        """

        params = self.jsons.create_participant_json(regdate = regdate, id = cprid, cpid = cpid, cptitle = cptitle, 
                        cpshorttitle =cpshorttitle, ppid = ppid, firstname = firstname, middlename = middlename, 
                        lastname = lastname, uid = uid, birthdate = birthdate, vitalstatus = vitalstatus, 
                        deathdate = deathdate, gender = gender, race = race, ethnicities = ethnicities, 
                        sexgenotype = sexgenotype, pmis = pmis, mrn = mrn, sitename = sitename, empi =empi)
        r = self.cpr.update_participant(cprid = cprid, params = params)

        return r
