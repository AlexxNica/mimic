"""
Networks API Plugin
"""

import json
from uuid import uuid4
from six import text_type
from zope.interface import implementer
from twisted.plugin import IPlugin
from mimic.rest.mimicapp import MimicApp
from mimic.catalog import Entry
from mimic.catalog import Endpoint
from mimic.imimic import IAPIMock


@implementer(IAPIMock, IPlugin)
class NetworksApi(object):
    """
    Rest endpoints for mocked Networks Api.
    """
    def __init__(self, regions=["ORD", "DFW", "IAD"]):
        """
        Create a NetworksApi.
        """
        self._regions = regions

    def catalog_entries(self, tenant_id):
        """
        List catalog entries for the Networks API.
        """
        return [
            Entry(
                tenant_id, "network", "cloudNetworks",
                [
                    Endpoint(tenant_id, region, text_type(uuid4()), prefix="v2")
                    for region in self._regions
                ]
            )
        ]

    def resource_for_region(self, region, uri_prefix, session_store):
        """
        Get an :obj:`twisted.web.iweb.IResource` for the given URI prefix;
        implement :obj:`IAPIMock`.
        """
        return NetworksMock(self, uri_prefix, session_store, region).app.resource()


class NetworksMock(object):
    """
    Klein routes for the Networking API.
    """
    def __init__(self, api_mock, uri_prefix, session_store, name):
        """
        Create a networks region with a given URI prefix
        """
        self.uri_prefix = uri_prefix
        self._api_mock = api_mock
        self._session_store = session_store
        self._name = name

    app = MimicApp()

    @app.route('/v2/<string:tenant_id>/networks', methods=['GET'])
    def get_networks(self, request, tenant_id):
        """
        Retrieves list of networks to which the specified tenant has access.
        https://developer.rackspace.com/docs/cloud-networks/v2/developer-guide/#retrieve-list-of-networks
        """
        request.setResponseCode(200)
        return json.dumps({"networks": []})
