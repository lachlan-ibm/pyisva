"""
@copyright: IBM
"""

import logging
import uuid

from pyisam.util.model import DataObject
from pyisam.util.restclient import RESTClient

POC_PROFILES = "/iam/access/v8/poc/profiles"
POC = "/iam/access/v8/poc"

logger = logging.getLogger(__name__)

class PointOfContact(object):

    def __init__(self, base_url, username, password):
        super(PointOfContact, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def get_profiles(self):

        endpoint = POC_PROFILES

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response

    def set_current_profile(self, profile_id):
        data = DataObject()

        data.add_value('currentProfileId',profile_id)

        endpoint = POC
        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 204

        return response


    def create_like_credential(self, name=None, description="", authenticate_callbacks=None, 
            local_id_callbacks=None, sign_out_callbacks=None, sign_in_callbacks=None):
        
        data = DataObject()

        initial_json = {
                "id": "",
                "name": name,
                "description": description,
                "isReadOnly": False,
                "signInCallbacks": [ {
                    "moduleReferenceId": "websealPocSignInCallback",
                    "index": 0,
                    "parameters": [
                      { "name": "fim.user.response.header.name", "value": "" },
                      { "name": "fim.user.session.id.response.header.name", "value": "" },
                      { "name": "fim.target.response.header.name", "value": "am-eai-redir-url" },
                      { "name": "fim.attributes.response.header.name", "value": "" },
                      { "name": "fim.groups.response.header.name", "value": "" },
                      { "name": "url.encoding.enabled", "value": "false" },
                      { "name": "fim.server.response.header.name", "value": "" },
                      { "name": "fim.cred.response.header.name", "value": "am-eai-pac" },
                      { "name": "fim.user.request.header.name", "value": "iv-user" }
                    ] } ],
                "signOutCallbacks": [ {
                    "moduleReferenceId": "websealPocSignOutCallback",
                    "index": 0,
                    "parameters": [
                      { "name": "fim.user.session.id.request.header.name", "value": "user_session_id" },
                      { "name": "fim.user.request.header.name", "value": "iv-user" }
                    ] } ],
                "localIdCallbacks": [ {
                    "moduleReferenceId": "websealPocLocalIdentityCallback",
                    "index": 0,
                    "parameters": [
                      { "name": "fim.attributes.request.header.name", "value": "" },
                      { "name": "fim.groups.request.header.name", "value": "iv-groups" },
                      { "name": "fim.cred.request.header.name", "value": "iv-creds" },
                      { "name": "fim.user.request.header.name", "value": "iv-user" }
                    ] } ],
                "authenticateCallbacks": [ {
                    "moduleReferenceId": "websealPocAuthenticateCallback",
                    "index": 0,
                    "parameters": [
                      { "name": "fim.user.request.header.name", "value": "iv-user" }
                    ] } ] }



        items_to_update = {'signInCallbacks':sign_in_callbacks,
                'authenticateCallbacks': authenticate_callbacks,
                'signOutCallbacks':sign_out_callbacks,
                'localIdCallbacks':local_id_callbacks}

        for work in items_to_update.items():
            if work[1] == None:
                    continue

            before = initial_json[work[0]][0]['parameters']
            during = map(lambda ent: (ent['name'], ent['value']), before)

            after = {}
            after.update(during)
            after.update(work[1])

            initial_json[work[0]][0]['parameters'] = list(map(lambda ent: {"name":ent[0], "value":ent[1]}, after.items()))

        data.from_json(initial_json)

        endpoint = POC_PROFILES 
        response = self.client.post_json(endpoint, data.data)
        response.success = response.status_code == 201

        return response



