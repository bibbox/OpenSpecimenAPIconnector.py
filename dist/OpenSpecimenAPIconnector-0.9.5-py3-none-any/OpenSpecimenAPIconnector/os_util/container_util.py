#! /bin/python3
import json
from ..os_core.jsons import Json_factory
from ..os_core.container import container 


class container_util():
    
    """Handles the container operations to and from OpenSpecimen

    This class handles the container based operations that can be done with OpenSpecimen.
    
    Note
    -----
    In order to use this and also the other classes, the user has to know OpenSpecimen. 
    The API calls are documented in https://openspecimen.atlassian.net/wiki/spaces/CAT/pages/1116035/REST+APIs and 
    the calls refer to this site. More details can be seen in the documentation.

    Examples
    --------

    A code Examples, where the Institutes are handled is in the Jupyter-Notebook:

    $ jupyter notebook main.ipynb
    """
    
    def __init__(self):

        self.containers = container()
        self.jsons = Json_factory()

    def create_container(self, name, sitename, numrows, numcols, storespecimens, barcode=None, typename=None, activitystatus=None, storageloc=None,
                        childcontainers=None, temp=None, columnlabelscheme=None, rowlablescheme=None,
                        comment=None, specimenclasses=None, specimentypes=None, collectionprotocols=None):

        """Create a container in Openspecimen

            Create a container in Openspecimen 

        Parameters
        ----------
        name : string
            Name of the sorage container
        barcode: string
            Barcode of the sotrage container
        typename : string
            Container type (e.g. Freezer see https://openspecimen.atlassian.net/wiki/spaces/CAT/overview 
            for available types and customization)
        activitystatus : string
            Whether the container is operational: Active or disabled; Default active
        sitename : string
            Site location of the container
        storageloc : dict
            used if conatiner is a child container gives the name, id and position of the child 
            within the parent container
        numcols : string
            Number of container columns (if type allows it)
        numrows : string
            Number of rows (if type allows it)
        storespecimens: string
            Boolean value (true, false) whether container can hold specimens or not
        childcontainers : string
            Filled if container sotres multiple other conatiners with different attributes
        temp : string
            Number literal giving the container temperature in celcius (e.g. -80, -20)
        columnlabelscheme : string
            Column labels - Numbers by default; 
            Permissible Values are {Numbers, Alphabets Upper Case, Alphabets Lower Case, Roman Upper Case, Roman Lower Case}
        rowlabelscheme : string
            Row labels - Numbers by default; 
            Permissible Values are {Numbers, Alphabets Upper Case, Alphabets Lower Case, Roman Upper Case, Roman Lower Case}
        comment : string
            Additional comments for the sorage container
        specimenclasses : list
            Specimen Classes allowed to be stored within the container
        specimentypes : list
            Specimen Types allowed to be stored within the container
        collecitonprotocols : list
            List of collection Protocols that can store samples within the given container
        
        Returns
        -------
        data: 
            Returns data of the created container or the OpenSpecimen Error Message
        """

        params = self.jsons.create_container_json(name=name, sitename=sitename, numrows=numrows, numcols=numcols, 
                            storespecimens=storespecimens, barcode=barcode, typename=typename, activitystatus=activitystatus, 
                            storageloc=storageloc, childcontainers=childcontainers, temp=temp, columnlabelscheme=columnlabelscheme, 
                            rowlablescheme=rowlablescheme, comment=comment, specimenclasses=specimenclasses, specimentypes=specimentypes, 
                            collectionprotocols=collectionprotocols)

        data = self.containers.create_container(params)

        return data

    def update_container(self, name, sitename, numrows, numcols, storespecimens, container_id, barcode=None, typename=None, 
                        activitystatus=None, storageloc=None, childcontainers=None, temp=None, columnlabelscheme=None, 
                        rowlablescheme=None, comment=None, specimenclasses=None, specimentypes=None, collectionprotocols=None):

        """Create a container in Openspecimen

            Create a container in Openspecimen 

        Parameters
        ----------
        name : string
            Name of the sorage container
        barcode: string
            Barcode of the sotrage container
        typename : string
            Container type (e.g. Freezer see https://openspecimen.atlassian.net/wiki/spaces/CAT/overview 
            for available types and customization)
        activitystatus : string
            Whether the container is operational: Active or disabled; Default active
        sitename : string
            Site location of the container
        storageloc : dict
            used if conatiner is a child container gives the name, id and position of the child 
            within the parent container
        numcols : string
            Number of container columns (if type allows it)
        numrows : string
            Number of rows (if type allows it)
        storespecimens: string
            Boolean value (true, false) whether container can hold specimens or not
        childcontainers : string
            Filled if container sotres multiple other conatiners with different attributes
        temp : string
            Number literal giving the container temperature in celcius (e.g. -80, -20)
        columnlabelscheme : string
            Column labels - Numbers by default; 
            Permissible Values are {Numbers, Alphabets Upper Case, Alphabets Lower Case, Roman Upper Case, Roman Lower Case}
        rowlabelscheme : string
            Row labels - Numbers by default; 
            Permissible Values are {Numbers, Alphabets Upper Case, Alphabets Lower Case, Roman Upper Case, Roman Lower Case}
        comment : string
            Additional comments for the sorage container
        specimenclasses : list
            Specimen Classes allowed to be stored within the container
        specimentypes : list
            Specimen Types allowed to be stored within the container
        collecitonprotocols : list
            List of collection Protocols that can store samples within the given container
        container_id : int
            Id of the given container
        
        Returns
        -------
        data: 
            Returns data of the created container or the OpenSpecimen Error Message
        """

        params = self.jsons.create_container_json(name=name, sitename=sitename, numrows=numrows, numcols=numcols, 
                            storespecimens=storespecimens, barcode=barcode, typename=typename, activitystatus=activitystatus, 
                            storageloc=storageloc, childcontainers=childcontainers, temp=temp, columnlabelscheme=columnlabelscheme, 
                            rowlablescheme=rowlablescheme, comment=comment, specimenclasses=specimenclasses, specimentypes=specimentypes, 
                            collectionprotocols=collectionprotocols)

        data = self.containers.update_container(params, container_id)

        return data
