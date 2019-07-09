"""
@copyright: IBM
"""

import ntpath
import logging

from pyisam.util.model import DataObject, Response
from pyisam.util.restclient import RESTClient


"""
Allows basic management of FIDO2 relying party configurations and metadata
"""
FIDO2_RELYING_PARTIES="/iam/access/v8/fido2/relying-parties"
FIDO2_METADATA="/iam/access/v8/fido2/metadata"

logger = logging.getLogger(__name__)


class FIDO2Config(object):

    def __init__(self, base_url, username, password):
        super(FIDO2Config, self).__init__()
        self.client = RESTClient(base_url, username, password)


    def get_relying_parties(self):
        response = self.client.get_json(FIDO2_RELYING_PARTIES)
        response.success = response.status_code == 200

        return response


    def create_relying_party(
            self, name=None, rpId=None, origins=None, metadataSet=None, metadataSoftFail=True,
            mediatorMappingRuleId=None, attestationStatementTypes=None, attestationStatementFormats=None,
            attestationPublicKeyAlgorithms=None, attestationAndroidSafetyNetMaxAge=None,
            attestationAndroidSafetyNetClockSkew=None, relyingPartyImpersonationGroup=None ):
        data = DataObject()
        data.add_value("name", name)
        data.add_value("rpId", rpId)

        fidoServerOptions = DataObject()
        fidoServerOptions.add_value_not_empty("origins", origins)
        fidoServerOptions.add_value("metadataSet", metadataSet)
        fidoServerOptions.add_value("metadataSoftFail", metadataSoftFail)
        fidoServerOptions.add_value("mediatorMappingRuleId", mediatorMappingRuleId)

        attestation = DataObject()        
        attestation.add_value("statementTypes", attestationStatementTypes)
        attestation.add_value("statementFormats", attestationStatementFormats)
        attestation.add_value("publicKeyAlgorithms", attestationPublicKeyAlgorithms)
        attestation.add_value("publicKeyAlgorithms", attestationPublicKeyAlgorithms)
        fidoServerOptions.add_value("attestation", attestation.data)

        attestationAndroidSafetyNetOptions = DataObject()
        attestationAndroidSafetyNetOptions.add_value("attestationMaxAge", attestationAndroidSafetyNetMaxAge)
        attestationAndroidSafetyNetOptions.add_value("clockSkew", attestationAndroidSafetyNetClockSkew)
        fidoServerOptions.add_value("android-safetynet", attestationAndroidSafetyNetOptions.data)

        data.add_value("fidoServerOptions", fidoServerOptions.data)

        relyingPartyOptions = DataObject()
        relyingPartyOptions.add_value("impersonationGroup", relyingPartyImpersonationGroup)
        data.add_value("relyingPartyOptions", relyingPartyOptions.data)

        response = self.client.post_json(FIDO2_RELYING_PARTIES, data.data)
        response.success = response.status_code == 201

        return response


    def update_relying_party(
            self, id, name=None, rpId=None, origins=None, metadataSet=None, metadataSoftFail=True,
            mediatorMappingRuleId=None, attestationStatementTypes=None, attestationStatementFormats=None,
            attestationPublicKeyAlgorithms=None, attestationAndroidSafetyNetMaxAge=None,
            attestationAndroidSafetyNetClockSkew=None, relyingPartyImpersonationGroup=None ):
        data = DataObject()
        data.add_value("id", id)
        data.add_value("name", name)
        data.add_value("rpId", rpId)

        fidoServerOptions = DataObject()
        fidoServerOptions.add_value_not_empty("origins", origins)
        fidoServerOptions.add_value("metadataSet", metadataSet)
        fidoServerOptions.add_value("metadataSoftFail", metadataSoftFail)
        fidoServerOptions.add_value("mediatorMappingRuleId", mediatorMappingRuleId)

        attestation = DataObject()        
        attestation.add_value("statementTypes", attestationStatementTypes)
        attestation.add_value("statementFormats", attestationStatementFormats)
        attestation.add_value("publicKeyAlgorithms", attestationPublicKeyAlgorithms)
        attestation.add_value("publicKeyAlgorithms", attestationPublicKeyAlgorithms)
        fidoServerOptions.add_value("attestation", attestation.data)

        attestationAndroidSafetyNetOptions = DataObject()
        attestationAndroidSafetyNetOptions.add_value("attestationMaxAge", attestationAndroidSafetyNetMaxAge)
        attestationAndroidSafetyNetOptions.add_value("clockSkew", attestationAndroidSafetyNetClockSkew)
        fidoServerOptions.add_value("android-safetynet", attestationAndroidSafetyNetOptions.data)

        data.add_value("fidoServerOptions", fidoServerOptions.data)

        relyingPartyOptions = DataObject()
        relyingPartyOptions.add_value("impersonationGroup", relyingPartyImpersonationGroup)
        data.add_value("relyingPartyOptions", relyingPartyOptions.data)

        endpoint = "%s/%s" % (FIDO2_RELYING_PARTIES, id)

        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 204

        return response


    def get_fido2_metadata(self):
        endpoint = FIDO2_METADATA

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def create_fido2_metadata(self, filename=None):
        response = Response()
        try:
            with open(filename, 'rb') as content:
                data = DataObject()
                data.add_value_string("filename", ntpath.basename(filename))
                data.add_value_string("contents", content.read().decode('utf-8'))

                endpoint = FIDO2_METADATA

                response = self.client.post_json(endpoint, data.data)
                response.success = response.status_code == 201

        except IOError as e:
            logger.error(e)
            response.success = False

        return response

    def update_fido2_metadata(self, id, filename=None):
        response = Response()
        try:
            with open(filename, 'rb') as content:
                files = {"file": content}

                endpoint = ("%s/%s/file" % (FIDO2_METADATA, id))

                response = self.client.post_file(endpoint, accept_type="application/json,text/html,application/*", files=files)
                response.success = response.status_code == 200

        except IOError as e:
            logger.error(e)
            response.success = False

        return response

