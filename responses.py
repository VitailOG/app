from typing import NamedTuple


class GeoVPS(NamedTuple):
    distance: float
    server_name: str


class VPSInfo(NamedTuple):
    city: str
    longitude: float
    latitude: float
    ip: str
    user: str
    password: str


class NearVPSResponse(NamedTuple):
    vps: GeoVPS
    vps_info: VPSInfo
