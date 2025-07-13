from typing import Dict
import requests

from .utils import throttle
from . import logger


def analyze_dynamic(url: str) -> Dict[str, str]:
    """Simplified dynamic analysis using requests.

    A real implementation would use a headless browser. Here we just check if
    the server attempts a direct download.
    """
    info: Dict[str, str] = {}
    try:
        throttle()
        resp = requests.get(url, stream=True, timeout=5)
        content_type = resp.headers.get('Content-Type', '')
        if 'application/octet-stream' in content_type:
            info['download_attempt'] = True
        else:
            info['download_attempt'] = False
        info['status_code'] = resp.status_code
        logger.info('Dynamic analysis of %s complete', url)
    except Exception as exc:
        info['error'] = str(exc)
        logger.error('Dynamic analysis failed for %s: %s', url, exc)
    return info
