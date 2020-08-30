
"""
Discover Hue Bridges on the Network
"""
import json
import logging
import sys
from typing import List

from huehue.utils import http
from . import Bridge


class Discover():
    """This Component is used to discover Hue Bridges on the local network.

    TODO: Make sure the logging here is accurate.
    TODO: Make sure verbosity level is accounted for here.
    """
    API_ENDPOINT = "https://discovery.meethue.com/"

    def discover_bridges(self) -> List[Bridge]:
        discovery_strategies = ['upnp', 'api']
        bridges = []

        for strategy in discovery_strategies:
            if bridges:
                break
            method = f"_{strategy}_discovery"
            if hasattr(self, method):
                try:
                    bridges = getattr(self, method)()
                except Exception as e:
                    logging.log(e, file=sys.stderr)
                    pass  # Do nothing.
        return bridges

    def _upnp_discovery(self):
        raise NotImplementedError

    def _api_discovery(self):
        # TODO: Add Error Handling
        r = http.request('GET', self.API_ENDPOINT_DISCOVERY)

        data = json.loads(r.data.decode('utf-8'))[0]

        return data['internalipaddress']