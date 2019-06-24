""""
@copyright: IBM
"""

import logging
import urllib

from pyisam.util.model import DataObject
from pyisam.util.restclient import RESTClient


DSC_ADMIN_REPLICAS = "/isam/dsc/admin/replicas"

logger = logging.getLogger(__name__)


class DSCAdmin(object):

    def __init__(self, base_url, username, password):
        super(DSCAdmin, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def list_replica_sets(self):
        """
        List the replica sets in the DSC server.
        """
        response = self.client.get_json(DSC_ADMIN_REPLICAS)
        response.success = response.status_code == 200

        return response

    def list_servers(self, replica_set):
        """
        List the servers (WebSEALs) for a replica set.
        """
        replica_set = urllib.quote(replica_set, safe='')
        endpoint = "%s/%s/servers" % (DSC_ADMIN_REPLICAS, replica_set)

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response

    def list_user_sessions(self, replica_set, user_name_pattern, max_results):
        """
        List user sessions in a replica set.
        """
        parameters = DataObject()
        parameters.add_value_string("user", user_name_pattern)
        parameters.add_value_string("max", max_results)

        replica_set = urllib.parse.quote(replica_set, safe='')
        endpoint = "%s/%s/sessions" % (DSC_ADMIN_REPLICAS, replica_set)

        response = self.client.get_json(endpoint, parameters.data)
        response.success = response.status_code == 200

        return response

    def terminate_session(self, replica_set, session):
        """
        Terminate a specific session.
        """
        replica_set = urllib.parse.quote(replica_set, safe='')
        session = urllib.parse.quote(session, safe='')
        endpoint = "%s/%s/sessions/session/%s" % (DSC_ADMIN_REPLICAS, replica_set, session)

        response = self.client.delete_json(endpoint)
        response.success = (response.status_code == 200 or response.status_code == 204)

        return response

    def terminate_user_sessions(self, replica_set, user_name):
        """
        Terminate all sessions for the specified user.
        """
        replica_set = urllib.parse.quote(replica_set, safe='')
        user_name = urllib.parse.quote(user_name, safe='')
        endpoint = "%s/%s/sessions/user/%s" % (DSC_ADMIN_REPLICAS, replica_set, user_name)

        response = self.client.delete_json(endpoint)
        response.success = (response.status_code == 200 or response.status_code == 204)

        return response
