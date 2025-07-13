from urllib.parse import urljoin
from urllib.robotparser import RobotFileParser
from typing import Dict
import requests

from .utils import throttle
from . import logger


def check_robots(url: str) -> Dict[str, str]:
    """Return whether fetching the URL is allowed by robots.txt."""
    info: Dict[str, str] = {}
    robots_url = urljoin(url, '/robots.txt')
    try:
        throttle()
        resp = requests.get(robots_url, timeout=5)
        parser = RobotFileParser()
        parser.parse(resp.text.splitlines())
        allowed = parser.can_fetch('*', url)
        info['allowed'] = allowed
        logger.info('robots.txt for %s allows fetch: %s', url, allowed)
    except Exception as exc:
        info['error'] = str(exc)
        logger.error('robots check failed for %s: %s', url, exc)
    return info
