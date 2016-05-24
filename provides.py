# from charmhelpers.core import hookenv
from charms.reactive import RelationBase
from charms.reactive import hook
from charms.reactive import scopes
# from charms.reactive import is_state
# from charms.reactive import not_unless


class CephOsdProvider(RelationBase):
    scope = scopes.UNIT

    @hook('{provides:ceph-osd}-relation-{joined,changed}')
    def changed(self):
        self.set_state('{relation_name}.connected')
        # service = hookenv.remote_service_name()
        # conversation = self.conversation()

    def provide_auth(self,
                     osd,
                     fsid,
                     osd_bootstrap_key,
                     auth,
                     public_address, osd_upgrade_key):
        """
        Provide a token to a requesting service.
        :param str osd: The osd which requested the auth
        :param str fsid: FSID for the Ceph cluster
        :param str osd_bootstrap_key: Bootstrap key for this OSD
        :param str auth: The auth to access Ceph
        :param str public_address: Ceph's public address
        :param str osd_upgrade_key: Upgrade key for this OSD
        """
        conversation = self.conversation(scope=osd)
        conversation.set_remote(**{
            'fsid': fsid,
            'osd_bootstrap_key': osd_bootstrap_key,
            'auth': auth,
            'ceph-public-address': public_address,
            'osd_upgrade_key': osd_upgrade_key,
        })

    def requested_auths(self):
        """
        Return a list of tuples mapping a service name to the auth name
        requested by that service.
        Example usage::
            for service, auth in ceph.requested_auths():
                ceph.provide_auth(service, auth, auth, public_address)
        """
        for conversation in self.conversations():
            service = conversation.scope
            auth = self.requested_auth(service)
            if auth is None:
                yield service, auth

    def requested_auth(self, service):
        """
        Return the auth provided to the requesting service.
        """
        return self.conversation(scope=service).get_remote('auth')
