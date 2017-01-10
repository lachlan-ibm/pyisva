"""
@copyright: IBM
"""

import logging

from pyisam.util.common import add_value, add_value_not_empty, add_value_string
from pyisam.util.restclient import RestClient


REVERSEPROXY = "/wga/reverseproxy"
WGA_DEFAULTS = "/isam/wga_templates/defaults"


logger = logging.getLogger(__name__)


class ReverseProxy(RestClient):

    def __init__(self, base_url, username, password):
        super(ReverseProxy, self).__init__(base_url, username, password)

    def create_instance(
            self, inst_name=None, host=None, admin_id=None, admin_pwd=None,
            ssl_yn=None, key_file=None, cert_label=None, ssl_port=None,
            http_yn=None, http_port=None, https_yn=None, https_port=None,
            nw_interface_yn=None, ip_address=None):
        #logger.enter()
        result = None

        success, status_code, content = self.get_wga_defaults()

        if success:
            listening_port = content.get("listening_port")
            domain = content.get("domain")

            data = {}
            add_value_string(data, "inst_name", inst_name)
            add_value_string(data, "host", host)
            add_value_string(data, "listening_port", listening_port)
            add_value_string(data, "domain", domain)
            add_value_string(data, "admin_id", admin_id)
            add_value_string(data, "admin_pwd", admin_pwd)
            add_value_string(data, "ssl_yn", ssl_yn)
            add_value_string(data, "key_file", key_file)
            add_value_string(data, "cert_label", cert_label)
            add_value_string(data, "ssl_port", ssl_port)
            add_value_string(data, "http_yn", http_yn)
            add_value_string(data, "http_port", http_port)
            add_value_string(data, "https_yn", https_yn)
            add_value_string(data, "https_port", https_port)
            add_value_string(data, "nw_interface_yn", nw_interface_yn)
            add_value_string(data, "ip_address", ip_address)

            status_code, content = self.http_post_json(REVERSEPROXY, data)

            result = (status_code == 200, status_code, content)
        else:
            result = (False, status_code, content)

        #logger.exit(result)
        return result

    def delete_instance(self, id, admin_id, admin_pwd):
        #logger.enter()
        result = None

        data = {}
        add_value_string(data, "admin_id", admin_id)
        add_value_string(data, "admin_pwd", admin_pwd)
        add_value_string(data, "operation", "unconfigure")

        endpoint = "%s/%s" % (REVERSEPROXY, id)
        status_code, content = self.http_put_json(endpoint, data)

        result = (status_code == 200, status_code, content)

        #logger.exit(result)
        return result

    def get_instances(self):
        #logger.enter()
        result = None

        status_code, content = self.http_get_json(REVERSEPROXY)

        result = (status_code == 200, status_code, content)

        #logger.exit(result)
        return result

    def get_wga_defaults(self):
        #logger.enter()
        result = None

        status_code, content = self.http_get_json(WGA_DEFAULTS)

        result = (status_code == 200, status_code, content)

        #logger.exit(result)
        return result

    def restart_instance(self, id):
        #logger.enter()
        result = None

        data = {}
        add_value_string(data, "operation", "restart")

        endpoint = "%s/%s" % (REVERSEPROXY, id)
        status_code, content = self.http_put_json(endpoint, data)

        result = (status_code == 200, status_code, content)

        #logger.exit(result)
        return result

    # Auto Configuration

    def configure_mmfa(
            self, webseal_id, lmi_hostname=None, lmi_port=None,
            lmi_username=None, lmi_password=None, runtime_hostname=None,
            runtime_port=None, runtime_username=None, runtime_password=None,
            reuse_certs=None,reuse_acls=None, reuse_pops=None):
        #logger.enter()
        result = None

        lmi_data = {}
        add_value_string(lmi_data, "hostname", lmi_hostname)
        add_value_string(lmi_data, "username", lmi_username)
        add_value_string(lmi_data, "password", lmi_password)
        add_value(lmi_data, "port", lmi_port)

        runtime_data = {}
        add_value_string(runtime_data, "hostname", runtime_hostname)
        add_value_string(runtime_data, "username", runtime_username)
        add_value_string(runtime_data, "password", runtime_password)
        add_value(runtime_data, "port", runtime_port)

        data = {}
        add_value(data, "reuse_certs", reuse_certs)
        add_value(data, "reuse_acls", reuse_acls)
        add_value(data, "reuse_pops", reuse_pops)
        add_value_not_empty(data, "lmi", lmi_data)
        add_value_not_empty(data, "runtime", runtime_data)

        endpoint = "%s/%s/mmfa_config" % (REVERSEPROXY, webseal_id)
        status_code, content = self.http_post_json(endpoint, data)

        result = (status_code == 204, status_code, content)

        #logger.exit(result)
        return result

    # Configuration

    def add_configuration_stanza_entry(
            self, webseal_id, stanza_id, entry_name, value):
        #logger.enter()
        result = None

        data = {"entries": [[str(entry_name), str(value)]]}

        endpoint = ("%s/%s/configuration/stanza/%s/entry_name"
                    % (REVERSEPROXY, webseal_id, stanza_id))
        status_code, content = self.http_post_json(endpoint, data)

        result = (status_code == 200, status_code, content)

        #logger.exit(result)
        return result

    def delete_configuration_stanza_entry(
            self, webseal_id, stanza_id, entry_name, value=None):
        #logger.enter()
        result = None

        endpoint = ("%s/%s/configuration/stanza/%s/entry_name/%s"
                    % (REVERSEPROXY, webseal_id, stanza_id, entry_name))
        if value:
            endpoint = "%s/value/%s" % (endpoint, value)
        status_code, content = self.http_delete_json(endpoint)

        result = (status_code == 200, status_code, content)

        #logger.exit(result)
        return result

    def update_configuration_stanza_entry(
            self, webseal_id, stanza_id, entry_name, value):
        #logger.enter()
        result = None

        data = {}
        add_value_string(data, "value", value)

        endpoint = ("%s/%s/configuration/stanza/%s/entry_name/%s"
                    % (REVERSEPROXY, webseal_id, stanza_id, entry_name))
        status_code, content = self.http_put_json(endpoint, data)

        result = (status_code == 200, status_code, content)

        #logger.exit(result)
        return result

    # Junction Management

    def create_junction(
            self, webseal_id, server_hostname=None, junction_point=None,
            junction_type=None, basic_auth_mode=None, tfim_sso=None,
            stateful_junction=None, preserve_cookie=None,
            cookie_include_path=None, transparent_path_junction=None,
            mutual_auth=None, insert_ltpa_cookies=None,
            insert_session_cookies=None, request_encoding=None,
            enable_basic_auth=None, key_label=None, gso_resource_group=None,
            junction_cookie_javascript_block=None, client_ip_http=None,
            version_two_cookies=None, ltpa_keyfile=None, authz_rules=None,
            fsso_config_file=None, username=None, password=None,
            server_uuid=None, virtual_hostname=None, server_dn=None,
            local_ip=None, query_contents=None, case_sensitive_url=None,
            windows_style_url=None, ltpa_keyfile_password=None,
            proxy_hostname=None, sms_environment=None, vhost_label=None,
            force=None, delegation_support=None, scripting_support=None,
            junction_hard_limit=None, junction_soft_limit=None,
            server_port=None, https_port=None, http_port=None, proxy_port=None,
            remote_http_header=None):
        #logger.enter()
        result = None

        data = {}
        add_value_string(data, "server_hostname", server_hostname)
        add_value_string(data, "junction_point", junction_point)
        add_value_string(data, "junction_type", junction_type)
        add_value_string(data, "basic_auth_mode", basic_auth_mode)
        add_value_string(data, "tfim_sso", tfim_sso)
        add_value_string(data, "stateful_junction", stateful_junction)
        add_value_string(data, "preserve_cookie", preserve_cookie)
        add_value_string(data, "cookie_include_path", cookie_include_path)
        add_value_string(
            data, "transparent_path_junction", transparent_path_junction)
        add_value_string(data, "mutual_auth", mutual_auth)
        add_value_string(data, "insert_ltpa_cookies", insert_ltpa_cookies)
        add_value_string(data, "insert_session_cookies", insert_session_cookies)
        add_value_string(data, "request_encoding", request_encoding)
        add_value_string(data, "enable_basic_auth", enable_basic_auth)
        add_value_string(data, "key_label", key_label)
        add_value_string(data, "gso_resource_group", gso_resource_group)
        add_value_string(
            data, "junction_cookie_javascript_block",
            junction_cookie_javascript_block)
        add_value_string(data, "client_ip_http", client_ip_http)
        add_value_string(data, "version_two_cookies", version_two_cookies)
        add_value_string(data, "ltpa_keyfile", ltpa_keyfile)
        add_value_string(data, "authz_rules", authz_rules)
        add_value_string(data, "fsso_config_file", fsso_config_file)
        add_value_string(data, "username", username)
        add_value_string(data, "password", password)
        add_value_string(data, "server_uuid", server_uuid)
        add_value_string(data, "virtual_hostname", virtual_hostname)
        add_value_string(data, "server_dn", server_dn)
        add_value_string(data, "local_ip", local_ip)
        add_value_string(data, "query_contents", query_contents)
        add_value_string(data, "case_sensitive_url", case_sensitive_url)
        add_value_string(data, "windows_style_url", windows_style_url)
        add_value_string(data, "ltpa_keyfile_password", ltpa_keyfile_password)
        add_value_string(data, "proxy_hostname", proxy_hostname)
        add_value_string(data, "sms_environment", sms_environment)
        add_value_string(data, "vhost_label", vhost_label)
        add_value_string(data, "force", force)
        add_value_string(data, "delegation_support", delegation_support)
        add_value_string(data, "scripting_support", scripting_support)
        add_value(data, "junction_hard_limit", junction_hard_limit)
        add_value(data, "junction_soft_limit", junction_soft_limit)
        add_value(data, "server_port", server_port)
        add_value(data, "https_port", https_port)
        add_value(data, "http_port", http_port)
        add_value(data, "proxy_port", proxy_port)
        add_value(data, "remote_http_header", remote_http_header)

        endpoint = "%s/%s/junctions" % (REVERSEPROXY, str(webseal_id))
        status_code, content = self.http_post_json(endpoint, data)

        result = (status_code == 200, status_code, content)

        #logger.exit(result)
        return result

    def get_junctions(self, webseal_id):
        #logger.enter()
        result = None

        endpoint = "%s/%s/junctions" % (REVERSEPROXY, webseal_id)
        status_code, content = self.http_get_json(endpoint)

        result = (status_code == 200, status_code, content)

        #logger.exit(result)
        return result

    # Management Root

    def import_management_root_files(self, webseal_id, file_path):
        #logger.enter()
        result = None

        endpoint = ("%s/%s/management_root" % (REVERSEPROXY, webseal_id))

        try:
            with open(file_path, 'rb') as pages:
                files = {"file": pages}

                status_code, content = self.http_post_file(
                    endpoint, files=files)

                result = (status_code == 200, status_code, content)
        except IOError as e:
            logger.error(e)
            result = (False, None, None)

        #logger.exit(result)
        return result

    def update_management_root_file(self, webseal_id, page_id, contents):
        #logger.enter()
        result = None

        data = {}
        add_value_string(data, "type", "file")
        add_value_string(data, "contents", contents)

        endpoint = ("%s/%s/management_root/%s"
                    % (REVERSEPROXY, webseal_id, page_id))
        status_code, content = self.http_put_json(endpoint, data)

        result = (status_code == 200, status_code, content)

        #logger.exit(result)
        return result
