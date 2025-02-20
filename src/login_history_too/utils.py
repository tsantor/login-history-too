import requests
from django.conf import settings
from requests.exceptions import JSONDecodeError


def get_ip_info(ip_address: str) -> dict:
    """Return IP data as a dict using the IP Stack API."""
    params = {
        "fields": "main",
        "hostname": 1,
        "access_key": settings.IPSTACK_ACCESS_KEY,
    }
    r = requests.get(
        f"https://api.ipstack.com/{ip_address}",
        params=params,
        timeout=5,
    )
    r.raise_for_status()
    try:
        return r.json()
    except JSONDecodeError:
        return {}


def get_ip_info_free(ip_address: str) -> dict:
    """Return IP data as a dict using the IP API."""
    r = requests.get(
        f"https://ipapi.co/{ip_address}/json/",
        timeout=5,
    )
    r.raise_for_status()
    try:
        return r.json()
    except JSONDecodeError:
        return {}
