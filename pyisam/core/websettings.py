"""
@copyright: IBM
"""


import logging

from .web.policyadmin import PolicyAdmin
from .web.reverseproxy import ReverseProxy
from .web.runtimecomponent import RuntimeComponent


logger = logging.getLogger(__name__)


class WebSettings9020(object):

    def __init__(self, base_url, username, password):
        self.policy_administration = PolicyAdmin(base_url, username, password)
        self.reverse_proxy = ReverseProxy(base_url, username, password)
        self.runtime_component = RuntimeComponent(base_url, username, password)

    def create_reverse_proxy(
            self, inst_name=None, host=None, admin_id=None, admin_pwd=None,
            ssl_yn=None, key_file=None, cert_label=None, ssl_port=None,
            http_yn=None, http_port=None, https_yn=None, https_port=None,
            nw_interface_yn=None, ip_address=None):
        logger.warning("Call to deprecated method create_reverse_proxy")
        return self.reverse_proxy.create_instance(
            inst_name=inst_name, host=host, admin_id=admin_id,
            admin_pwd=admin_pwd, ssl_yn=ssl_yn, key_file=key_file,
            cert_label=cert_label, ssl_port=ssl_port, http_yn=http_yn,
            http_port=http_port, https_yn=https_yn, https_port=https_port,
            nw_interface_yn=nw_interface_yn, ip_address=ip_address)

    def delete_reverse_proxy(self, id, admin_id, admin_pwd):
        logger.warning("Call to deprecated method delete_reverse_proxy")
        return self.reverse_proxy.delete_instance(id, admin_id, admin_pwd)

    def get_reverse_proxies(self):
        logger.warning("Call to deprecated method get_reverse_proxies")
        return self.reverse_proxy.get_instances()

    def restart_reverse_proxy(self, id):
        logger.warning("Call to deprecated method restart_reverse_proxy")
        return self.reverse_proxy.restart_instance(id)

    def configure_reverse_proxy_mmfa(
            self, webseal_id, lmi_hostname=None, lmi_port=None,
            lmi_username=None, lmi_password=None, runtime_hostname=None,
            runtime_port=None, runtime_username=None, runtime_password=None,
            reuse_certs=None,reuse_acls=None, reuse_pops=None):
        logger.warning("Call to deprecated method configure_reverse_proxy_mmfa")
        return self.reverse_proxy.configure_mmfa(
            webseal_id, lmi_hostname=lmi_hostname, lmi_port=lmi_port,
            lmi_username=lmi_username, lmi_password=lmi_password,
            runtime_hostname=runtime_hostname, runtime_port=runtime_port,
            runtime_username=runtime_username,
            runtime_password=runtime_password, reuse_certs=reuse_certs,
            reuse_acls=reuse_acls, reuse_pops=reuse_pops)

    def add_reverse_proxy_configuration_stanza_entry(
            self, webseal_id, stanza_id, entry_name, value):
        logger.warning("Call to deprecated method add_reverse_proxy_configuration_stanza_entry")
        return self.reverse_proxy.add_configuration_stanza_entry(
            webseal_id, stanza_id, entry_name, value)

    def delete_reverse_proxy_configuration_stanza_entry(
            self, webseal_id, stanza_id, entry_name, value=None):
        logger.warning("Call to deprecated method delete_reverse_proxy_configuration_stanza_entry")
        return self.reverse_proxy.delete_configuration_stanza_entry(
            webseal_id, stanza_id, entry_name, value)

    def update_reverse_proxy_configuration_stanza_entry(
            self, webseal_id, stanza_id, entry_name, value):
        logger.warning("Call to deprecated method update_reverse_proxy_configuration_stanza_entry")
        return self.reverse_proxy.update_configuration_stanza_entry(
            webseal_id, stanza_id, entry_name, value)

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
        logger.warning("Call to deprecated method create_reverse_proxy_junction")
        return self.reverse_proxy.create_junction(
            webseal_id, server_hostname=server_hostname,
            junction_point=junction_point, junction_type=junction_type,
            basic_auth_mode=basic_auth_mode, tfim_sso=tfim_sso,
            stateful_junction=stateful_junction,
            preserve_cookie=preserve_cookie,
            cookie_include_path=cookie_include_path,
            transparent_path_junction=transparent_path_junction,
            mutual_auth=mutual_auth, insert_ltpa_cookies=insert_ltpa_cookies,
            insert_session_cookies=insert_session_cookies,
            request_encoding=request_encoding,
            enable_basic_auth=enable_basic_auth, key_label=key_label,
            gso_resource_group=gso_resource_group,
            junction_cookie_javascript_block=junction_cookie_javascript_block,
            client_ip_http=client_ip_http,
            version_two_cookies=version_two_cookies, ltpa_keyfile=ltpa_keyfile,
            authz_rules=authz_rules, fsso_config_file=fsso_config_file,
            username=username, password=password, server_uuid=server_uuid,
            virtual_hostname=virtual_hostname, server_dn=server_dn,
            local_ip=local_ip, query_contents=query_contents,
            case_sensitive_url=case_sensitive_url,
            windows_style_url=windows_style_url,
            ltpa_keyfile_password=ltpa_keyfile_password,
            proxy_hostname=proxy_hostname, sms_environment=sms_environment,
            vhost_label=vhost_label, force=force,
            delegation_support=delegation_support,
            scripting_support=scripting_support,
            junction_hard_limit=junction_hard_limit,
            junction_soft_limit=junction_soft_limit, server_port=server_port,
            https_port=https_port, http_port=http_port, proxy_port=proxy_port,
            remote_http_header=remote_http_header)

    def get_reverse_proxy_junctions(self, webseal_id):
        logger.warning("Call to deprecated method get_reverse_proxy_junctions")
        return self.reverse_proxy.get_junctions(webseal_id)

    def import_reverse_proxy_management_root_files(self, webseal_id, file_path):
        logger.warning("Call to deprecated method import_reverse_proxy_management_root_files")
        return self.reverse_proxy.import_management_root_files(
            webseal_id, file_path)

    def update_reverse_proxy_management_root_file(
            self, webseal_id, page_id, contents):
        logger.warning("Call to deprecated method update_reverse_proxy_management_root_file")
        return self.reverse_proxy.update_management_root_file(
            webseal_id, page_id, contents)

    def configure_runtime_component(
            self, ps_mode=None, user_registry=None, admin_password=None,
            ldap_password=None, admin_cert_lifetime=None, ssl_compliance=None,
            ldap_host=None, ldap_port=None, isam_domain=None, ldap_dn=None,
            ldap_suffix=None, ldap_ssl_db=None, ldap_ssl_label=None,
            isam_host=None, isam_port=None):
        logger.warning("Call to deprecated method configure_runtime_component")
        return self.runtime_component.configure(
            ps_mode=ps_mode, user_registry=user_registry,
            admin_password=admin_password, ldap_password=ldap_password,
            admin_cert_lifetime=admin_cert_lifetime,
            ssl_compliance=ssl_compliance, ldap_host=ldap_host,
            ldap_port=ldap_port, isam_domain=isam_domain, ldap_dn=ldap_dn,
            ldap_suffix=ldap_suffix, ldap_ssl_db=ldap_ssl_db,
            ldap_ssl_label=ldap_ssl_label, isam_host=isam_host,
            isam_port=isam_port)

    def update_runtime_component_embedded_ldap_password(self, password):
        logger.warning("Call to deprecated method update_runtime_component_embedded_ldap_password")
        return self.runtime_component.update_embedded_ldap_password(password)

    def do_pdadmin_commands(self, admin_id, admin_pwd, commands):
        logger.warning("Call to deprecated method do_pdadmin_commands")
        return self.policy_administration.do_commands(
            admin_id, admin_pwd, commands)


class WebSettings9021(WebSettings9020):

    def __init__(self, base_url, username, password):
        super(WebSettings9021, self).__init__(base_url, username, password)
