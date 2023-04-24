import operator as op
from http import HTTPStatus
from ipaddress import IPv4Address
from typing import Any, ClassVar, Literal

import requests
from geopy.distance import geodesic

from config import VPS_SERVERS
from responses import GeoVPS, NearVPSResponse, VPSInfo


class HTTPStatusError(Exception):
    pass


class BaseFetcher:
    url: str
    context: ClassVar[dict[str, Any]]
    method: ClassVar[Literal['get', 'post', 'patch', 'put']]

    def fetch(self):
        response = getattr(requests, self.method)(self.url, **self.context)

        if response.status_code != HTTPStatus.OK:
            raise HTTPStatusError

        return response.json()


class UserCoordinateFetcher(BaseFetcher):
    method = "get"
    url = "http://api.ipapi.com/api/"
    context = {
        "params": {
            "access_key": "65df7c82ddb887fad4c61c3fb1459039"
        }
    }

    def __init__(self, ip: IPv4Address):
        self.url = f"{self.url}{ip}"


def get_near_vps(ip: IPv4Address) -> NearVPSResponse:
    user_info = UserCoordinateFetcher(ip).fetch()
    user_coordinates = (user_info['longitude'], user_info['latitude'])
    distances = []
    for server in VPS_SERVERS:
        server_coordinates = (VPS_SERVERS[server]["longitude"], VPS_SERVERS[server]["latitude"])
        distances.append(
            GeoVPS(
                distance=geodesic(user_coordinates, server_coordinates).km,
                server_name=server
            )
        )
    near_vps = sorted(distances, key=op.attrgetter('distance'))[0]
    return NearVPSResponse(
        vps=near_vps,
        vps_info=VPSInfo(**VPS_SERVERS[near_vps.server_name])
    )
