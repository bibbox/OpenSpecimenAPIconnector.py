   #! /bin/python3




   def cp_get_cps_json(self):
        endpoint = "/collection-protocols"
        url = self.base_url + endpoint
        r = self.Req_Fact.get_request(url)
        req_json = json.loads(r.text)

        return req_json

    # basic filtering is tolerable on core layer or not ?
    def cp_get_cp_ids(self, record_ids=None):

        endpoint = "/collection-protocols"
        url = self.base_url + endpoint
        r = self.Req_Fact.get_request(url)
        req_json = json.loads(r.text)
        ids = np.zeros(len(req_json))
        for i, item in enumerate(req_json):
            ids[i] = item["id"]

        return ids


    def class_method_module_post_entity_operation(self):
        pass

    def class_method_module_put_entity_operation(self):
        pass

    def class_method_module_delete_entity(self):
        pass