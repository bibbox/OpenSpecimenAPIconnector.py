#! /bin/python3

import pandas
import json
from datetime import date

from ..os_core.specimen import specimen
from ..os_core.url import url_gen
from ..os_core.jsons import Json_factory
from ..os_core.users import users



class specimen_util:

    """Handles the calls for Specimens
    
    This class handles the API calls for OpenSpecimen Specimens. It can create, update, delete, 
    search specimens with different parameters. The other calls are in the os_core class specimens.
    The output is a JSON dict or the Error message as dict. It also can check if a
    specimen exists which returns a string which tells you if it exists.
    
    Note
    -----
    In order to use this and also the other classes, the user has to know OpenSpecimen. 
    The API calls are documented in https://openspecimen.atlassian.net/wiki/spaces/CAT/pages/1116035/REST+APIs and 
    the calls refer to this site. More details can be seen in the documentation.
    
    Examples
    --------
    A code Examples, where the Specimens/Derivatives/Aliquots are handled is in the Jupyter-Notebook
        $ jupyter notebook main.ipynb
    """

    def __init__(self):

        """Constructor of the Class specimens_util
        
        Constructor of the class specimen_util, can handle the basic API-calls
        of the specimensin OpenSpecimen. It also connects this class to the os_core classes
        specimen, url_gen and Json_factory.
        
        Parameters
        ----------
        base_url : string
            URL to openspecimen, has the format: http(s)://<host>:<port>/openspecimen/rest/ng
        auth : tuple
            Consists of two strings ( loginname , password)
        """

        self.specimen = specimen()
        self.url = url_gen()
        self.jsons = Json_factory()
        self.users = users()


    def search_specimens(self, label = None, cprid = None, eventid = None, visitid = None, maxres = "100", exact = "false", extension = "true"):

        """Search for Specimen with specific values.
        
        Search for one or more Specimens with the values in the search_string defined. The search string looks like:
        http(s)://<host>:<port>/openspecimen/rest/np/specimens?{param_1}={value_1}&...&{param_x}={value_x}
        
        
        Parameters
        ----------
        label : string
            Label of the specimen.

        cprid : int
            Collection Protocol Registration ID to what Participant the specimen belongs to.

        eventid : int
            Unique systemwide Identifier of the event.

        visitid : int
            Unique systemwide identifier of the visit.

        maxres : int
            Defines how many results are returned maximally.

        exact : string
            OpenSpecimen's boolean true/false. If true Parameters have to match exactly.

        extension : string
            OpenSpecimen's boolean true/false. If true extension Details will get returned too.

        Returns
        -------
        dict
            Details of the matching Specimens, if no one matches it is an empty list.
        """

        search_string = self.url.search_specimen(label = label, cprid = cprid, eventid = eventid, visitid = visitid,
                                             maxres = maxres, exact = exact, extension = extension)
        r = self.specimen.search_specimens(search_string = search_string)

        return r

    def create_specimen(self, specimenclass, specimentype , pathology , anatomic, laterality, initqty, avaqty, visitid, recqlt, userid, 
                        colltime = None, rectime = None, lineage = 'New', status = 'Collected', stor_name = None, storlocx = None,
                        storlocy = None, concetration = None, biohazard = None,  comments = None,  collproc=None, label = None,
                        conttype=None, extensionudn=None, extensionmap=None, extensiondict =None):

        """Create a Specimen to a visit

        Create a Specimen to an already existing Visit. In order to use this function one has to know,
        the mandatory details of the specimen e.g. the class of the Specimen.
        
        Note
        -----
        The label is mandatory if the Protocolsettings are such that the Label is created manually, otherwise
        it has to be left empty.

        Parameters
        ----------
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
        
        label : string
            The Label of the specimen, if automatically generated it has to be left empty, or else it is mandatory.
            
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
            Position of the specimen in the container in y direction.[optional]
            
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
            
        extensionudn : string
            OpenSpecimen's boolean true/false. If true, the extension keys are the udn values of the corresponding form.[optional]
        
        extensionmap : string
            The name of the Form which should be taken.[optional]

        extensiondict : dict
            The dictionary of the extensions, has to be created manually. Either with udn or name (as defined before). [optional]

        Returns
        -------
        dict
            Dictionary with details of the specimen or the OpenSpecimen's error meessage.
        """
               
        if rectime == None:
            rectime = date.today()
        
        if colltime == None:
            colltime = date.today()

        storloc = None
        if stor_name != None:
            storloc = self.jsons.storage_location_json(name = stor_name, xpos = storlocx, ypos = storlocy)

        extension =None
        if extensiondict != None:
            extension = self.jsons.create_extension(attrsmap = extensionmap, extensiondict = extensiondict, useudn = extensionudn)

        params = self.jsons.create_specimen_json(label = label, specimenclass = specimenclass, specimentype = specimentype, pathology =pathology,
                anatomic= anatomic, laterality = laterality, initqty = initqty, avaqty = avaqty, visitid = visitid, colltime = colltime,
                userid = userid, comments = comments, collproc = collproc, conttype = conttype, recqlt = recqlt, rectime = rectime,
                lineage = lineage, status = status, storloc = storloc, concentration = concetration, biohazard = biohazard,
                extension = extension)
        
        r = self.specimen.create_specimen(params = params)

        return r


    def update_specimen(self, specimenid, label = None, specimenclass = None, specimentype = None, pathology = None, anatomic = None, laterality = None,
                            initqty = None, avaqty = None, visitid = None, recqlt = None, colltime = None, rectime = None, lineage = 'New',
                            status = 'Collected', stor_name = None, storlocx = None, storlocy = None, concetration = None, biohazard = None,
                            userid = None, comments = None,  collproc=None, conttype=None, extensionudn=None, extensionmap=None, extensiondict =None):

        """Update an existing Specimen

        Update an existing Specimen in order to use this function one has to know the specimenid. This can be seen via the GUI
        by clicking on the desired specimen, and read from the URL: http(s)://<host>:<port>/openspecimen/cps/{cpid}/specimens/{specimenid}/... .
        Or via search Specimen, for Examples by name and then extract the ID via key ["id"].
        
        Note
        -----
        The specimenid is mandatory, all the other keys are otional for updating. If left empty nothing will be changed.

        Parameters
        ----------
        specimenid : int
            Unique Id of the specimen.

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
        
        label : string
            The Label of the specimen.
            
        colltime : string
            Date and Time of the collection event, the format is in the OpenSpecimen's System configuration.
            
        rectime : string
            Date and Time of the received event, the format is in the OpenSpecimen's System configuration.
            
        lineage : string
            Lineage of the specimen, default value is New.
            
        status : string
            Status of the Specimen, default is 'Collected'.
        
        stor_name : string
            Name of the container. 
        
        storlocx : int
            Position of the specimen in the Container in x direction.

        storlocy : int
            Position of the specimen in the container in y direction.
            
        concetration  : int
            Concentration of the specimen.
        
        biohazard : string
            Biohazards of that specimen.
        
        userid : int
            ID of the user who creates the specimen. If not specified the API user is taken.
            
        comments : string
            Comments regarding to the specimen.
        
        collproc : string
            The procedure of the collection.

        conttype : string
            Type of the storage container.
            
        extensionudn : string
            OpenSpecimen's boolean true/false. If true the extension keys are the udn values of the corresponding form.
        
        extensionmap : string
            The name of the Form which should be taken.

        extensiondict : dict
            The dictionary of the extensions, has to be created manually. Either with udn or name (as defined before). 

        Returns
        -------
        dict
            Dictionary with details of the specimen or the OpenSpecimen's error meessage.
        """

        storloc = None
        if stor_name != None:
            storloc = self.jsons.storage_location_json(name = stor_name, xpos = storlocx, ypos = storlocy)

        extension =None
        if extensiondict != None:
            extension = self.jsons.create_extension(attrsmap = extensionmap, extensiondict = extensiondict, useudn = extensionudn)

        params = self.jsons.create_specimen_json(label = label, specimenclass = specimenclass, specimentype = specimentype, pathology =pathology,
                anatomic= anatomic, laterality = laterality, initqty = initqty, avaqty = avaqty, visitid = visitid, colltime = colltime,
                userid = userid, comments = comments, collproc = collproc, conttype = conttype, recqlt = recqlt, rectime = rectime,
                lineage = lineage, status = status, storloc = storloc, concentration = concetration, biohazard = biohazard,
                extension = extension)
        
        r = self.specimen.update_specimen(specimenid = specimenid,params = params)

        return r

    def delete_specimens(self, specimenids):

        """Delete a Specimen/Derivative/Aliquot
        
        Delete an already existing Specimen/Derivative/Aliquot. The Parameters <specimenid> is the uniqe ID of the Specimen/
        Derivative/Aliquot which is generated automatically from OpenSpecimen. To get the ID one can click in the GUI on the 
        Specimen/Derivative/Aliquot and read it from the URL, with format:
        http(s)://<host>:<port>/openspecimen/cp-view/{cpid}/specimen/{specimenid}/... .
        Another possibility is to search via 'search_specimens' for a specific Parameters and then extract the ID
        from the JSON-dict which get returned. The function allows also to delete a list of specimen
        
        Parameters
        ----------
        specimenids: list or int 
            The unique ID(s) of the Specimen/Aliquot/Derivative which OpenSpecimen creates itself. 
            The URL of the specimens, which should be deleted, has the form "?id=specimenid_1+...+specimenid_n"
            
        Returns
        -------
        JSON-dict
            Details of the Specimens which are deleted or the OpenSpecimen error message as dict.
        """

        specids = self.url.delete_specimens(specimenids = specimenids)
        r = self.specimen.delete_specimen(specimenids = specids)

        return r

