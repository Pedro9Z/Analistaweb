from typing import Dict
import requests
from bs4 import BeautifulSoup

from urllib.parse import urlparse

from .utils import throttle
from . import logger


def analyze_html(url: str) -> Dict[str, str]:
    info = {}
    try:
        throttle()
        resp = requests.get(url, timeout=5)
        soup = BeautifulSoup(resp.text, 'html.parser')
        info['title'] = soup.title.string if soup.title else ''
        scripts = soup.find_all('script')
        info['script_count'] = len(scripts)
        domain = urlparse(url).netloc
        external = [s for s in scripts if s.get('src') and domain not in s['src']]
        info['external_scripts'] = len(external)
        logger.info('HTML analysis of %s complete', url)
    except Exception as exc:
        info['error'] = str(exc)
        logger.error('HTML analysis failed for %s: %s', url, exc)
    return info
