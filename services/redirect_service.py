import requests
from typing import Dict

from .utils import throttle
from . import logger


def follow_redirects(url: str) -> Dict[str, str]:
    info = {}
    try:
        throttle()
        resp = requests.get(url, allow_redirects=True, timeout=5)
        info['final_url'] = resp.url
        info['status_code'] = resp.status_code
        info['history'] = [r.status_code for r in resp.history]
        logger.info('Redirect chain for %s: %s', url, info['history'])
    except Exception as exc:
        info['error'] = str(exc)
        logger.error('Redirect check failed for %s: %s', url, exc)
    return info
