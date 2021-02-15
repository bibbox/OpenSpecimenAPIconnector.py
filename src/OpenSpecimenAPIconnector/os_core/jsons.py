import requests
import json
import pickle
import json
import requests
import uuid
import faker
from faker import Factory
import names
import random
import time
import datetime
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta

from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta




class Json_factory():

    def __init__(self):
        pass

    ##TODO Decide upon way of json creation/storage for OS operations, the current idea is to set mandatory values to
    ## boolean true by default. than a random generator can create the values in fixed order and they can be set
    ## according to the boolean. Even better would be the restriction to use pandas data frames directly and create the
    ## json once data entry is done. Another important question is how to deal with custom value fields in various cases.
    ## Further, where possible, the csv import option should be used and json creation should be left to the numerous
    ## methods within Open Specimen
    ## first approach to be overhauled

    # creation jsons:
    # participant
    def create_participant_json(self, regdate = None, id = None, cpid = None, cptitle = None, 
                        cpshorttitle =None, ppid = None, firstname = None, middlename = None, 
                        lastname = None, uid = None, birthdate = None, vitalstatus = None, 
                        deathdate = None, gender = None, race = None, ethnicities = None, 
                        sexgenotype = None, pmis = None, mrn = None, sitename = None, empi =None):

        """Creates a JSON-formated string for participant creation

        This function creates the json corresponding to the cpr_util function

        Notes
        ----- 
        Mandatory parameters are passed as positional arguments in the caliing function

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

        if registeredCps is None:
            registeredCps = []

        participantRegistration = {
            "participant": {
                "id": id,
                "firstName": firstname,
                "middleName": middlename,
                "lastName": lastname,
                "uid":uid,
                "birthDate": birthdate,
                "vitalStatus": vitalstatus,
                "deathDate": death_date,
                "gender": gender,
                "race": race,
                "sexGenotype": sexgenotype,
                "ethnicities": ethnicities,
                "pmis": pmis,
                "mrn": mrn,
                "siteName": sitename,
                "empi": empi                
            },
            "cpId": cp_id,
            "registrationDate": regdate,
            "ppid": pp_id,
            "cpShortTitle": cpshorttile,
            "cpTitle": cptitle
        }

        return participantRegistration

    # Collection Protocoll

    def create_CP_json(self, short_title = None, title=None, pi_mail=None, time_start=None, time_end=None, sites=None, man_id=False, coords=None,
                           consentsWaived=False,eth_cons_id=None, part_no=None, desc_url=None, visitNameFmt=None,
                           man_visit_name=False, man_spec_label=True, aliquots_in_same=None, activity="Active"):

        """Creates the JSON-formated string corresponding to the collection_protocol_util funciton create_CP
        
        Notes
        -----
        Mandatory paramters are passed as positional args within the calling util class

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
            Sites which are assigned to the collection Protocol.
        
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
        JSON-formated-string containing the collection protocol information neccesary for creation
        """

        site_arr = []
        for item in sites:
            site_arr.append(
                {
                    "siteName": item[0],
                    "code": item[1]
                }
            )

        CP_reg = {
            "shortTitle": short_title,
            "title": title,
            "code": None,
            "principalInvestigator":
                {
                    "loginName": pi_mail,
                    "domain": "openspecimen"
                },
            "startDate": time_start,
            "endDate": time_end,
            "ppidFmt": "DWP%05d",
            "manualPpidEnabled": man_id,
            "coordinators": coords,
            "cpSites": site_arr,
            "consentsWaived": consentsWaived,
            "irbId": eth_cons_id,
            "anticipatedParticipantsCount": part_no,
            "descriptionUrl": desc_url,
            "specimenLabelFmt": "%PPI%.%SP_TYPE%.%SYS_UID%",
            "derivativeLabelFmt": "%PPI%.%SP_TYPE%.%SYS_UID%",
            "aliquotLabelFmt": "%PSPEC_LABEL%.%PSPEC_UID%",
            "visitNameFmt": visitNameFmt,
            "manualVisitNameEnabled": man_visit_name,
            "manualSpecLabelEnabled": man_spec_label,
            "aliquotsInSameContainer": aliquots_in_same,
            "activityStatus": activity
        }

        return json.dumps(CP_reg)

    # Collection Protocol event

    def create_cp_event_json(self, label=None, point=None, cp=None, site=None, diagnosis=None, status=None, activity=None, unit=None, code=None):
        
         """Create JSON-formated string needed for event creation
        
        Create an event for a given Collection Protocol. Details of the parameters can be found in
        the parameters section.

        Notes
        -----
        Mandatory paramters are passed as positional args within the calling util class

        Parameters
        ----------
        label : string
            Label of the Event, has to be unique.
        
        point : string or int
            Starting Point of the event, Value + unit (e.g. DAYS).
        
        cp : string
            title of the collection protocol.
        
        site : string
            The default Site of the event.
        
        diagnosis : string
            Defines the permissable values of the diagnosis.
        
        status : string
            Defines the permissable values of the clinical status.
        
        acitivity : string
            DEfines the activity status of the event.
        
        unit : string
            Defines which unit has the starting point.
        
        code : string
            the Event code, is optional. In order to define condionals in the workflow, one need the Event code.

        Returns
        -------
        JSON-formated string
            Returns a JSON-formated string with the given details for cp event creation
        """

        params = {
            "eventLabel": label,
            "clinicalDiagnosis": diagnosis,
            "clinicalStatus": status,
            "collectionProtocol": cp,
            "defaultSite": site,
            "activityStatus": activity,
            "eventPoint": point,
            "eventPointUnit": unit
        }

        return json.dumps(params)


    def create_specimen_json(self, label=None, specimenclass=None, specimentype=None, pathology=None, anatomic=None,
                            laterality=None, initqty=None, avaqty=None, visitid=None, userid=None, colltime=None,
                            rectime=None, recqlt=None, lineage='New', status='Collected', storloc=None, concentration=None,
                            biohazard=None, comments=None,  collproc=None, conttype=None, extension =None):


        """Create a API Json String for a Specimen

        Create the JSON String neccesary for creating a specimen
        
        Notes
        -----
        Mandatory paramters are passed as positional args within the calling util class

        Parameters
        ----------

        label : string
            UUID of specimen generated automatically if not set to manual in corresponding collection protocol
        
        specimenclass : string
            Class of the specimen.
        
        specimentype : string
            Type of the specimen, belongs to the class.
        
        pathology : string
            Pathologystatus of the Specimen.

        anatomic : string
            The anatomic site of the specimen.
        
        laterality : string
            The laterality of the specimen.
        
        initqty : int
            The initial quantity of a specimen.
        
        avaqty : int
            The available quantity of a specimen.
        
        visitid : int
            The unique identifier of the visit.

        recqlt : string
            The received quality.
            
        colltime : string
            Date and Time of the collection event, the format is in the OpenSpecimen's System configuration.[optional]
            
        rectime : string
            Date and Time of the received event, the format is in the OpenSpecimen's System configuration.[optional]
            
        lineage : string
            Lineage of the specimen, default value is New.
            
        status : string
            Status of the Specimen, default is 'Collected'.
        
        stor_name : string
            Name of the container. [optional]
        
        storlocx : int
            Position of the specimen in the Container in x direction.[optional]

        storlocy : int
            Position of the specimen int the container in y direction.[optional]
            
        concetration  : int
            Concentration of the specimen[optional].
        
        biohazard : string
            Biohazards of that specimen.[optional]
        
        userid : int
            ID of the user who creates the specimen. If not specified the API user is taken.
            
        comments : string
            Comments regarding to the specimen[optional].
        
        collproc : string
            The procedure of the collection[otpional].

        conttype : string
            Type of the storage conatiner.
            
        extension : JSON-String
            JSON-formated-string containing the dict of specimnen extensions created during call to the corresponding util class 
        
        Returns
        -------
        dict
            JSON-formated-string with the complete specimen to be created
        """

        spec = {
            "label": label,
            "specimenClass": specimenclass,
            "type": specimentype,
            "pathology": pathology,
            "anatomicSite": anatomic,
            "laterality": laterality,
            "initialQty": initqty,
            "availableQty": avaqty,
            "visitId": visitid,
            "status": status,
            "storageLocation": {storloc},
            "concetration": concentration,
            "biohazard": biohazard,
            "comments": comments,
            "collevent": {
                "user": {"id": user},
                    "time": colltime,
                    "container": conttype,
                    "procedure": procedure
                     },
            "receivedEvent":{
                "user":{"id": userid},
                "time": rectime,
                "receivedQuality": recqlt
            },
            "extensionDetail": {extension}
            }

        return json.dumps(spec)

    def create_extension(self, attrsmap, extensiondict, useudn="false"):

        data = {
            "useUdn": useudn,
            "attryMap": attrsmap,
            "value": extensiondict
        }

        return json.dumps(data)

    # Export Institute CSV
    def create_institue_export_job_json(self):
        
        """Create JSON formated string neccesary for

        Parameters
        cp_id: string Collection protocoll id pof export target
        ----------
        Returns
        JSON-formated-string needed for creating an export job for the given entity
        -------
        
        institute_json = {"objectType": "institute"}

        return json.dumps(institute_json)

    # Export Sites CSV
    def create_site_export_job_json(self, record_ids=None):
        
        """Create JSON formated string neccesary for

        Parameters
        cp_id: string Collection protocoll id pof export target
        ----------
        Returns
        JSON-formated-string needed for creating an export job for the given entity
        -------
        site_json = {"objectType": "site"}

        return json.dumps(site_json)

    # Export User CSV
    def create_user_export_job(self):

        """Create JSON formated string neccesary for

        Parameters
        cp_id: string Collection protocoll id pof export target
        ----------
        Returns
        JSON-formated-string needed for creating an export job for the given entity
        -------

        user_json = {"objectType": "user"}

        return json.dumps(user_json)

    # Export CP Registaration CSV
    def create_cp_export_job_json(self, cp_id=None):
        """Create JSON formated string neccesary for

        Parameters
        cp_id: string Collection protocoll id pof export target
        ----------
        Returns
        JSON-formated-string needed for creating an export job for the given entity
        -------
        json dict
        cp_json = {"objectType": "cp", "params": {"cpId": cp_id}}

        return json.dumps(cp_json)

    # Export CP Registaration CSV
    def create_cpr_export_job_json(self, cp_id=None):

        """Create JSON formated string neccesary for

        Parameters
        cp_id: string Collection protocoll id pof export target
        ----------
        Returns
        JSON-formated-string needed for creating an export job for the given entity
        -------
        cpr_json = {"objectType": "cpr", "params": {"cpId": cp_id}}

        return json.dumps(cpr_json)

    # Export Vist CSV
    def create_visit_export_job_json(self, cp_id=None):

        """Create JSON formated string neccesary for

        Parameters
        cp_id: string Collection protocoll id pof export target
        ----------
        Returns
        JSON-formated-string needed for creating an export job for the given entity
        -------
        visit_json = {"objectType": "specimen", "params": {"cpId": cp_id}}

        return json.dumps(visit_json)

    # Export Specimen CSV
    def create_specimen_export_job_json(self, cp_id=None):

        """Create JSON formated string neccesary for

        Parameters
        cp_id: string Collection protocoll id pof export target
        ----------
        Returns
        JSON-formated-string needed for creating an export job for the given entity
        -------
        specimen_json = {"objectType": "specimen", "params": {"cpId": cp_id}}

        return json.dumps(specimen_json)

    ##TODO

    # Import collection protocols
    def create_site_import_job_json(self, record_ids=None):

        """Create JSON formated string neccesary for

        Parameters
        cp_id: string Collection protocoll id pof export target
        ----------
        Returns
        JSON-formated-string needed for creating an import job for the given entity
        -------

        site_json = {"objectType": "site", "recordIds": record_ids}

        return json.dumps(site_json)
    
    # Create  Any AQL Query
    def create_aql(self, cpid, aql, rowmode='OFF', coloumexpr='true', isodate='true'):

        params = {
            "cpId" : cpid,
            "aql" : aql,
            "wideRowMode" : rowmode,
            "outputColoumnExprs" : coloumexpr,
            "outputIsoDateTime" : isodate
        }

        return json.dumps(params)

    # Execute Saved Query
    def execute_query(self, start, results, drivingform="Participant", rowmode="OFF"):

        params= {
            "drivingForm": drivingform,
            "wideRowMode": rowmode,
            "startAt": start,
            "maxResults":results
        }

        return json.dumps(params)

    def create_cpr_part_import_job(self, schemaname=None, operation=None, fileid=None,
                                   dateformat=None, timeformat=None):

        """Create JSON formated string neccesary for

        Parameters
        cp_id: string Collection protocoll id pof export target
        ----------
        Returns
        JSON-formated-string needed for creating an export job for the given entity
        -------

        part_cpr_json = {"objectType": schemaname,
                    "importType": operation,
                    "inputFileId": fileid,
                    "dateFormat":dateformat,
                    "timeFormat":timeformat
                    }

        return json.dumps(part_cpr_json)

    def get_registrations(self, cpid=None, registrationdate=None, ppid=None, name=None, birthdate=None, uid=None, specimen=None,
                                    includestats=None, startat=None,maxresults=None):

        params = {
            "cpId": cpid,
            "registrationDate": registrationdate,
            "ppid": ppid,
            "name": name,
            "dob": birthdate,
            "uid": uid,
            "specimen": specimen,
            "includeStats": includestats,
            "startAt": startat,
            "maxResults": maxresults
        }

        return json.dumps(params)

    def add_visit_json(self,cprid, name, site,eventid=None,eventlabel=None,ppid=None, cptitle=None, cpshorttitle=None,
                        diagnosis=None, clinicalstatus=None, activity=None, visitstatus="COMPLETE", missedreason=None,
                        missedby=None, comments=None,pathologynumber=None,cohort=None, visitdate=None, cpid=None):

        params = {
            "cprId": cprid,
            "eventId": eventid,
            "eventLabel": eventlabel,
            "ppid": ppid,
            "cpTitle": cptitle,
            "cpShortTitle":cpshorttitle,
            "cpId": cpid,
            "name": name,
            "clinicalDiagnoses": diagnosis,
            "clinicalStatus": clinicalstatus,
            "activityStatus": activity,
            "site": site,
            "status": visitstatus,
            "missedReason": missedreason,
            "missedBy": missedby,
            "comments": comments,
            "surgicalPathologyNumber": pathologynumber,
            "cohort": cohort,
            "visitDate": visitdate
        }
        
        return json.dumps(params)

    def storage_location_json(self, id=None, name=None, xpos=None, ypos=None):

        params = {
            "id": id,
            "name": name,
            "positionX": xpos,
            "positionY": ypos
        }

        return json.dumps(params)

    def create_cp_csv_export_job(self, objecttype, cpid, entitytype=None, formname=None):

        """Create JSON formated string neccesary for

        Parameters
        cp_id: string Collection protocoll id pof export target
        ----------
        Returns
        JSON-formated-string needed for creating an export job for the given entity
        -------

        data = {
            "objectType": objecttype,
            "params":{
                "entityType": entitytype,
                "formName": formname,
                "cpId": cpid
            }
        }

        return json.dumps(data)

    def merge_cps(self, src_cp, trg_cp):
        
        data = {
            "srcCpShortTitle": src_cp,
            "tgtCpShortTitle": trg_cp
        }

        return json.dumps(data)

    def create_institute(self, institutename):

        data = {
            "name": institutename
        }

        return json.dumps(data)

    def get_participants(self, lastname = None, uid = None, birthdate = None, pmi = None, empi = None, reqreginfo = None):

        data ={
            "lastName" : lastname,
            "pmi":{
                "mrn" : str(pmi[0]),
                "siteName" : pmi[1]
            },
            "birthDate" : birthdate,
            "uid" : uid,
            "empi" : empi,
            "reqRegInfo" : reqreginfo
        }
        
        return json.dumps(data)



