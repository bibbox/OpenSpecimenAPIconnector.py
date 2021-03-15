
#! /bin/python3

import requests

class OS_request_gen():
    
    """Generates OpenSpecimen specific requests
     
    This class generates OpenSpecimen specific requests such that headers and authentification are created automatically.
    With this class the users have to specify which requests they do need, the url and the payload, which should be sent
    to OpenSpecimen. The payload alters for different requests and can be seen in the OpenSpecimen's API documentation.
    The class can handle the following requests: GET, POST(formdata, files, json-formatted string), PUT, DELETE, HEADER.
    
    Note
    -----
    In order to use this and also the other classes, the user has to know OpenSpecimen. The users have to know which requests
    are needed and what content should be uploaded. The API documentation of OpenSpecimen is in:
    https://openspecimen.atlassian.net/wiki/spaces/CAT/pages/1116035/REST+APIs
    
    Examples
    --------
    A code Examples, where those requests are used, is in the Jupyter-Notebook
        $ jupyter notebook main.ipynb
    """

    def __init__(self, auth):
        
        """Constructor of the class OS_request_gen()
        
        Constructor of the class OS_request_gen(). It generates the possible headers for the different requests,
        which are json_headers, zip_headers, form_data_headers, file_headers.
        
        Parameters
        ----------
        auth : string
            String as tuple with the format "( API-User, Password)"
        """
        
        self.json_headers = {
            'content-type': "application/json", 'cache-control': "no-cache"}
        self.zip_headers = {
            'content-type': "application/zip", 'cache-control': "no-cache"}
        self.form_data_headers = {
            'content-type': "form-data", 'cache-control': "no-cache"}
        self.file_headers={
            'cache-control': "no-cache"}

        self.auth = auth
        self.user_name = auth[0]


    def get_request(self, url, stream=False):
        
        """Generates GET requests for OpenSpecimen
        
        Generates GET request for OpenSpecimen, which always contains the URL in the format
        http(s)://<host>:<port>/openspecimen/rest/ng/... . It is used for searching objects and 
        downloading templates or collections. If one downloads a larger file, the Parameters
        stream has to be set to "True".
        
        Parameters
        ----------
        url : string
            URL for the get request as string has the form: http(s)://<host>:<port>/openspecimen/rest/ng/...
            
        stream : bool
            Can be set to "True" for larger files, which takes a while to download. Default value is "False".
            
        Returns
        -------
        http(s) response
            The response of the request consists of status code, header and body. The type of the body alters
            for different requests.
        """

        if stream:
            r = requests.request("GET", url, auth=self.auth,
            headers=self.zip_headers, stream=stream)

        else:
            r = requests.request("GET", url, auth=self.auth,
                                 headers=self.json_headers)

        return r


    def post_request(self, url, data=None, form_data=False, files=None, params=None):

        """Generates POST requests for OpenSpecimen
        
        Generates POST request for OpenSpecimen, which always contains the URL in the format
        http(s)://<host>:<port>/openspecimen/rest/ng/... . This request is most times used 
        for creating or updating objects in OpenSpecimen and the data is either a JSON-dict
        with the keys from OpenSpecimen or a binary-file content( this needs a second call to
        execute the job)
        
        Parameters
        ----------
        url : string
            URL for the get request as string has the form: http(s)://<host>:<port>/openspecimen/rest/ng/...
            
        data : json-formatted strings
            Json-formatted string, with the keys from OpenSpecimen.
            
        form_data : bool
            Default value is "False". Can be set to "True" if, for Examples, forms (.xml-files) are uploaded.
        
        files : binary
            Default value is "None". Contains tuple with name + ending and file itself.
        
        params : json formatted string
            Json-formatted string, with the keys from OpenSpecimen.
            
        Returns
        -------
        http(s) response
            The response of the request consists of status code, header and body. The type of the body alters
            for different requests.
        """
        
        if form_data:
            r = requests.request("POST", url, data=data, auth=self.auth,
                                 headers=self.form_data_headers, params=params)

        if form_data==False and files==None:
            r = requests.request("POST", url, data=data, auth=self.auth,
                                 headers=self.json_headers, params=params)
        if files!=None:
            r= requests.request("POST", url, auth=self.auth, 
                                 headers=self.file_headers,files=files, params=params)
        return r


    def put_request(self, url, data):
        
        """Generates PUT requests for OpenSpecimen
        
        Generates PUT request for OpenSpecimen, which always contains the URL in the format
        http(s)://<host>:<port>/openspecimen/rest/ng/... . This request is most times used 
        for updating objects in OpenSpecimen and the data is a JSON-dict with the keys 
        from OpenSpecimen.
        
        Parameters
        ----------
        url : string
            URL for the get request as string has the form: http(s)://<host>:<port>/openspecimen/rest/ng/...
            
        data : json-formatted strings
            Json-formatted string, with the keys from OpenSpecimen.
            
        Returns
        -------
        http(s) response
            The response of the request consists of status code, header and body. The type of the body alters
            for different request.
        """

        r = requests.request("PUT", url, data=data, auth=self.auth,
                             headers=self.json_headers)
        return r


    def delete_request(self, url):
        
        """Generates DELETE requests for OpenSpecimen
        
        Generates DELETE request for OpenSpecimen, which always contains the URL in the format
        http(s)://<host>:<port>/openspecimen/rest/ng/{entity}/{objectID} . Is used for deleting objects 
        of a desired entity e.g. specimens. Usually OpenSpecimen requires the ID of the object in the URL.
        
        Parameters
        ----------
        url : string
            URL for the get request as string has the form: http(s)://<host>:<port>/openspecimen/rest/ng/{entity}/{objectID}
            
        Returns
        -------
        http(s) response
            The response of the request consists of status code, header and body. The type of the body alters
            for different requests.
        """

        r = requests.request("DELETE", url, auth=self.auth)

        return r


    def head_request(self, url):
        
        """Generates HEAD requests for OpenSpecimen
        
        Generates a HEAD request for OpenSpecimen, which always contains the URL in the format
        http(s)://<host>:<port>/openspecimen/rest/ng/{entity} . It is used for getting
        the header of an object. Usually OpenSpecimen requires the entity of the object in the URL.
        
        Parameters
        ----------
        url : string
            URL for the get request as string has the form: http(s)://<host>:<port>/openspecimen/rest/ng/{entity}
            
        Returns
        -------
        http(s) response
            The response of the request consists of status code, header and body. The type of the body alters
            for different request.
        """

        r = requests.request("HEAD", url, auth=self.auth)

        return r

    def user_name(self):
        
        """Returns the OpenSpecimen Login name
        
        Returns the OpenSpecimen login name of the API-User.
        
        Returns
        -------
        string
            The API-User's login name.
        """
        
        return self.user_name

