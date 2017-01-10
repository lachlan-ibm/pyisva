"""
@copyright: IBM
"""

import logging

from pyisam.util.logger import Logger
from pyisam.util.restclient import RestClient
import pyisam.util.common as Utils

EMBEDDED_LDAP_PASSWORD = "/isam/embedded_ldap/change_pwd/v1"
PDADMIN = "/isam/pdadmin"
REVERSEPROXY = "/wga/reverseproxy"
RUNTIME_COMPONENT = "/isam/runtime_components"
WGA_DEFAULTS = "/isam/wga_templates/defaults"


class Manage(RestClient):

    logger = Logger("Manage")

    def __init__(self, base_url, username, password, log_level=logging.NOTSET):
        super(Manage, self).__init__(base_url, username, password, log_level)
        Manage.logger.set_level(log_level)

    #
    # Reverse Proxy
    #

    def create_reverse_proxy(
            self, inst_name=None, host=None, admin_id=None, admin_pwd=None,
            ssl_yn=None, key_file=None, cert_label=None, ssl_port=None,
            http_yn=None, http_port=None, https_yn=None, https_port=None,
            nw_interface_yn=None, ip_address=None):
        Manage.logger.enter()
        result = None

        success, status_code, content = self.get_wga_defaults()

        if success:
            listening_port = content.get("listening_port")
            domain = content.get("domain")

            data = {}
            Utils.add_value_string(data, "inst_name", inst_name)
            Utils.add_value_string(data, "host", host)
            Utils.add_value_string(data, "listening_port", listening_port)
            Utils.add_value_string(data, "domain", domain)
            Utils.add_value_string(data, "admin_id", admin_id)
            Utils.add_value_string(data, "admin_pwd", admin_pwd)
            Utils.add_value_string(data, "ssl_yn", ssl_yn)
            Utils.add_value_string(data, "key_file", key_file)
            Utils.add_value_string(data, "cert_label", cert_label)
            Utils.add_value_string(data, "ssl_port", ssl_port)
            Utils.add_value_string(data, "http_yn", http_yn)
            Utils.add_value_string(data, "http_port", http_port)
            Utils.add_value_string(data, "https_yn", https_yn)
            Utils.add_value_string(data, "https_port", https_port)
            Utils.add_value_string(data, "nw_interface_yn", nw_interface_yn)
            Utils.add_value_string(data, "ip_address", ip_address)

            status_code, content = self.http_post_json(REVERSEPROXY, data)

            result = (status_code == 200, status_code, content)
        else:
            result = (False, status_code, content)

        Manage.logger.exit(result)
        return result

    def delete_reverse_proxy(self, id, admin_id, admin_pwd):
        Manage.logger.enter()
        result = None

        data = {}
        Utils.add_value_string(data, "admin_id", admin_id)
        Utils.add_value_string(data, "admin_pwd", admin_pwd)
        Utils.add_value_string(data, "operation", "unconfigure")

        endpoint = "%s/%s" % (REVERSEPROXY, id)
        status_code, content = self.http_put_json(endpoint, data)

        result = (status_code == 200, status_code, content)

        Manage.logger.exit(result)
        return result

    def get_reverse_proxies(self):
        Manage.logger.enter()
        result = None

        status_code, content = self.http_get_json(REVERSEPROXY)

        result = (status_code == 200, status_code, content)

        Manage.logger.exit(result)
        return result

    def get_wga_defaults(self):
        Manage.logger.enter()
        result = None

        status_code, content = self.http_get_json(WGA_DEFAULTS)

        result = (status_code == 200, status_code, content)

        Manage.logger.exit(result)
        return result

    def restart_reverse_proxy(self, id):
        Manage.logger.enter()
        result = None

        data = {}
        Utils.add_value_string(data, "operation", "restart")

        endpoint = "%s/%s" % (REVERSEPROXY, id)
        status_code, content = self.http_put_json(endpoint, data)

        result = (status_code == 200, status_code, content)

        Manage.logger.exit(result)
        return result

    # Auto Configuration

    def configure_reverse_proxy_mmfa(
            self, webseal_id, lmi_hostname=None, lmi_port=None,
            lmi_username=None, lmi_password=None, runtime_hostname=None,
            runtime_port=None, runtime_username=None, runtime_password=None,
            reuse_certs=None,reuse_acls=None, reuse_pops=None):
        Manage.logger.enter()
        result = None

        lmi_data = {}
        Utils.add_value_string(lmi_data, "hostname", lmi_hostname)
        Utils.add_value_string(lmi_data, "username", lmi_username)
        Utils.add_value_string(lmi_data, "password", lmi_password)
        Utils.add_value(lmi_data, "port", lmi_port)

        runtime_data = {}
        Utils.add_value_string(runtime_data, "hostname", runtime_hostname)
        Utils.add_value_string(runtime_data, "username", runtime_username)
        Utils.add_value_string(runtime_data, "password", runtime_password)
        Utils.add_value(runtime_data, "port", runtime_port)

        data = {}
        Utils.add_value(data, "reuse_certs", reuse_certs)
        Utils.add_value(data, "reuse_acls", reuse_acls)
        Utils.add_value(data, "reuse_pops", reuse_pops)
        Utils.add_value_not_empty(data, "lmi", lmi_data)
        Utils.add_value_not_empty(data, "runtime", runtime_data)

        endpoint = "%s/%s/mmfa_config" % (REVERSEPROXY, webseal_id)
        status_code, content = self.http_post_json(endpoint, data)

        result = (status_code == 204, status_code, content)

        Manage.logger.exit(result)
        return result

    # Configuration

    def add_reverse_proxy_configuration_stanza_entry(
            self, webseal_id, stanza_id, entry_name, value):
        Manage.logger.enter()
        result = None

        data = {"entries": [[str(entry_name), str(value)]]}

        endpoint = ("%s/%s/configuration/stanza/%s/entry_name"
                    % (REVERSEPROXY, webseal_id, stanza_id))
        status_code, content = self.http_post_json(endpoint, data)

        result = (status_code == 200, status_code, content)

        Manage.logger.exit(result)
        return result

    def delete_reverse_proxy_configuration_stanza_entry(
            self, webseal_id, stanza_id, entry_name, value=None):
        Manage.logger.enter()
        result = None

        endpoint = ("%s/%s/configuration/stanza/%s/entry_name/%s"
                    % (REVERSEPROXY, webseal_id, stanza_id, entry_name))
        if value:
            endpoint = "%s/value/%s" % (endpoint, value)
        status_code, content = self.http_delete_json(endpoint)

        result = (status_code == 200, status_code, content)

        Manage.logger.exit(result)
        return result

    def update_reverse_proxy_configuration_stanza_entry(
            self, webseal_id, stanza_id, entry_name, value):
        Manage.logger.enter()
        result = None

        data = {}
        Utils.add_value_string(data, "value", value)

        endpoint = ("%s/%s/configuration/stanza/%s/entry_name/%s"
                    % (REVERSEPROXY, webseal_id, stanza_id, entry_name))
        status_code, content = self.http_put_json(endpoint, data)

        result = (status_code == 200, status_code, content)

        Manage.logger.exit(result)
        return result

    # Junction Management

    def create_reverse_proxy_junction(
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
        Manage.logger.enter()
        result = None

        data = {}
        Utils.add_value_string(data, "server_hostname", server_hostname)
        Utils.add_value_string(data, "junction_point", junction_point)
        Utils.add_value_string(data, "junction_type", junction_type)
        Utils.add_value_string(data, "basic_auth_mode", basic_auth_mode)
        Utils.add_value_string(data, "tfim_sso", tfim_sso)
        Utils.add_value_string(data, "stateful_junction", stateful_junction)
        Utils.add_value_string(data, "preserve_cookie", preserve_cookie)
        Utils.add_value_string(data, "cookie_include_path", cookie_include_path)
        Utils.add_value_string(
            data, "transparent_path_junction", transparent_path_junction)
        Utils.add_value_string(data, "mutual_auth", mutual_auth)
        Utils.add_value_string(data, "insert_ltpa_cookies", insert_ltpa_cookies)
        Utils.add_value_string(
            data, "insert_session_cookies", insert_session_cookies)
        Utils.add_value_string(data, "request_encoding", request_encoding)
        Utils.add_value_string(data, "enable_basic_auth", enable_basic_auth)
        Utils.add_value_string(data, "key_label", key_label)
        Utils.add_value_string(data, "gso_resource_group", gso_resource_group)
        Utils.add_value_string(
            data, "junction_cookie_javascript_block",
            junction_cookie_javascript_block)
        Utils.add_value_string(data, "client_ip_http", client_ip_http)
        Utils.add_value_string(data, "version_two_cookies", version_two_cookies)
        Utils.add_value_string(data, "ltpa_keyfile", ltpa_keyfile)
        Utils.add_value_string(data, "authz_rules", authz_rules)
        Utils.add_value_string(data, "fsso_config_file", fsso_config_file)
        Utils.add_value_string(data, "username", username)
        Utils.add_value_string(data, "password", password)
        Utils.add_value_string(data, "server_uuid", server_uuid)
        Utils.add_value_string(data, "virtual_hostname", virtual_hostname)
        Utils.add_value_string(data, "server_dn", server_dn)
        Utils.add_value_string(data, "local_ip", local_ip)
        Utils.add_value_string(data, "query_contents", query_contents)
        Utils.add_value_string(data, "case_sensitive_url", case_sensitive_url)
        Utils.add_value_string(data, "windows_style_url", windows_style_url)
        Utils.add_value_string(
            data, "ltpa_keyfile_password", ltpa_keyfile_password)
        Utils.add_value_string(data, "proxy_hostname", proxy_hostname)
        Utils.add_value_string(data, "sms_environment", sms_environment)
        Utils.add_value_string(data, "vhost_label", vhost_label)
        Utils.add_value_string(data, "force", force)
        Utils.add_value_string(data, "delegation_support", delegation_support)
        Utils.add_value_string(data, "scripting_support", scripting_support)
        Utils.add_value(data, "junction_hard_limit", junction_hard_limit)
        Utils.add_value(data, "junction_soft_limit", junction_soft_limit)
        Utils.add_value(data, "server_port", server_port)
        Utils.add_value(data, "https_port", https_port)
        Utils.add_value(data, "http_port", http_port)
        Utils.add_value(data, "proxy_port", proxy_port)
        Utils.add_value(data, "remote_http_header", remote_http_header)

        endpoint = "%s/%s/junctions" % (REVERSEPROXY, str(webseal_id))
        status_code, content = self.http_post_json(endpoint, data)

        result = (status_code == 200, status_code, content)

        Manage.logger.exit(result)
        return result

    def get_reverse_proxy_junctions(self, webseal_id):
        Manage.logger.enter()
        result = None

        endpoint = "%s/%s/junctions" % (REVERSEPROXY, webseal_id)
        status_code, content = self.http_get_json(endpoint)

        result = (status_code == 200, status_code, content)

        Manage.logger.exit(result)
        return result

    # Management Root

    def import_reverse_proxy_management_root_files(self, webseal_id, file_path):
        Manage.logger.enter()
        result = None

        endpoint = ("%s/%s/management_root" % (REVERSEPROXY, webseal_id))

        try:
            with open(file_path, 'rb') as pages:
                files = {"file": pages}

                status_code, content = self.http_post_file(
                    endpoint, files=files)

                result = (status_code == 200, status_code, content)
        except IOError as e:
            Manage.logger.error(e)
            result = (False, None, None)

        Manage.logger.exit(result)
        return result

    def update_reverse_proxy_management_root_file(
            self, webseal_id, page_id, contents):
        Manage.logger.enter()
        result = None

        data = {}
        Utils.add_value_string(data, "type", "file")
        Utils.add_value_string(data, "contents", contents)

        endpoint = ("%s/%s/management_root/%s"
                    % (REVERSEPROXY, webseal_id, page_id))
        status_code, content = self.http_put_json(endpoint, data)

        result = (status_code == 200, status_code, content)

        Manage.logger.exit(result)
        return result

    #
    # Runtime Component
    #

    def get_runtime_components(self):
        """
        Query the ISAM API to get the runtime components list.
        :return: The tuple of success flag, status code and response contents.
        """
        status_code, content = self.http_get_json(RUNTIME_COMPONENT)

        result = (status_code == 200, status_code, content)

        Manage.logger.exit(result)
        return result

    def configure_runtime_component(
            self, ps_mode=None, user_registry=None, admin_password=None,
            ldap_password=None, admin_cert_lifetime=None, ssl_compliance=None,
            ldap_host=None, ldap_port=None, isam_domain=None, ldap_dn=None,
            ldap_suffix=None, ldap_ssl_db=None, ldap_ssl_label=None,
            isam_host=None, isam_port=None):
        Manage.logger.enter()
        result = None

        data = {}
        Utils.add_value_string(data, "ps_mode", ps_mode)
        Utils.add_value_string(data, "user_registry", user_registry)
        Utils.add_value_string(data, "admin_cert_lifetime", admin_cert_lifetime)
        Utils.add_value_string(data, "ssl_compliance", ssl_compliance)
        Utils.add_value_string(data, "admin_pwd", admin_password)
        Utils.add_value_string(data, "ldap_pwd", ldap_password)
        Utils.add_value_string(data, "ldap_host", ldap_host)
        Utils.add_value_string(data, "domain", isam_domain)
        Utils.add_value_string(data, "ldap_dn", ldap_dn)
        Utils.add_value_string(data, "ldap_suffix", ldap_suffix)
        Utils.add_value_string(data, "ldap_ssl_db", ldap_ssl_db)
        Utils.add_value_string(data, "ldap_ssl_label", ldap_ssl_label)
        Utils.add_value_string(data, "isam_host", isam_host)
        Utils.add_value(data, "ldap_port", ldap_port)
        Utils.add_value(data, "isam_port", isam_port)

        status_code, content = self.http_post_json(RUNTIME_COMPONENT, data)

        result = (status_code == 200, status_code, content)

        Manage.logger.exit(result)
        return result

    def update_runtime_component_embedded_ldap_password(self, password):
        Manage.logger.enter()
        result = None

        data = {}
        Utils.add_value_string(data, "password", password)

        status_code, content = self.http_post_json(EMBEDDED_LDAP_PASSWORD, data)

        result = (status_code == 200, status_code, content)

        Manage.logger.exit(result)
        return result

    #
    # Policy Administation
    #

    def do_pdadmin_commands(self, admin_id, admin_pwd, commands):
        Manage.logger.enter()
        result = None

        data = {}
        Utils.add_value_string(data, "admin_id", admin_id)
        Utils.add_value_string(data, "admin_pwd", admin_pwd)
        Utils.add_value(data, "commands", commands)

        status_code, content = self.http_post_json(PDADMIN, data)

        result = (status_code == 200, status_code, content)

        Manage.logger.exit(result)
        return result
