import os
import requests
from typing import Dict
from base64 import urlsafe_b64encode

from .utils import throttle
from . import logger

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
PHISHTANK_API_KEY = os.getenv('PHISHTANK_API_KEY')
VIRUSTOTAL_API_KEY = os.getenv('VIRUSTOTAL_API_KEY')


def check_blacklists(url: str) -> Dict[str, str]:
    info = {}
    # Google Safe Browsing
    if GOOGLE_API_KEY:
        payload = {
            'client': {'clientId': 'analyst', 'clientVersion': '1.0'},
            'threatInfo': {
                'threatTypes': ['MALWARE', 'SOCIAL_ENGINEERING'],
                'platformTypes': ['ANY_PLATFORM'],
                'threatEntryTypes': ['URL'],
                'threatEntries': [{'url': url}],
            },
        }
        try:
            throttle()
            resp = requests.post(
                f'https://safebrowsing.googleapis.com/v4/threatMatches:find?key={GOOGLE_API_KEY}',
                json=payload,
                timeout=5,
            )
            if resp.status_code == 200 and resp.json().get('matches'):
                info['google_safe_browsing'] = 'listed'
            else:
                info['google_safe_browsing'] = 'clean'
            logger.info('Google Safe Browsing checked %s', url)
        except Exception as exc:
            info['google_safe_browsing'] = f'error: {exc}'
            logger.error('Google Safe Browsing check failed for %s: %s', url, exc)
    else:
        info['google_safe_browsing'] = 'no_api_key'

    # PhishTank
    if PHISHTANK_API_KEY:
        try:
            throttle()
            resp = requests.post(
                'https://checkurl.phishtank.com/checkurl/',
                data={'url': url, 'format': 'json', 'app_key': PHISHTANK_API_KEY},
                timeout=5,
            )
            data = resp.json().get('results', {})
            if data.get('in_database') and data.get('valid'):  # flagged
                info['phishtank'] = 'listed'
            else:
                info['phishtank'] = 'clean'
            logger.info('PhishTank checked %s', url)
        except Exception as exc:
            info['phishtank'] = f'error: {exc}'
            logger.error('PhishTank check failed for %s: %s', url, exc)
    else:
        info['phishtank'] = 'no_api_key'

    # URLhaus
    try:
        throttle()
        resp = requests.post('https://urlhaus-api.abuse.ch/v1/url/', data={'url': url}, timeout=5)
        if resp.status_code == 200 and resp.json().get('query_status') == 'ok':
            if resp.json().get('url_status') == 'online':
                info['urlhaus'] = 'listed'
            else:
                info['urlhaus'] = 'clean'
        else:
            info['urlhaus'] = 'clean'
        logger.info('URLhaus checked %s', url)
    except Exception as exc:
        info['urlhaus'] = f'error: {exc}'
        logger.error('URLhaus check failed for %s: %s', url, exc)

    # VirusTotal
    if VIRUSTOTAL_API_KEY:
        try:
            throttle()
            vid = urlsafe_b64encode(url.encode()).decode().strip('=')
            headers = {'x-apikey': VIRUSTOTAL_API_KEY}
            resp = requests.get(
                f'https://www.virustotal.com/api/v3/urls/{vid}', headers=headers, timeout=5
            )
            if resp.status_code == 200 and resp.json().get('data', {}).get('attributes', {}).get('last_analysis_stats', {}).get('malicious'):
                info['virustotal'] = 'listed'
            else:
                info['virustotal'] = 'clean'
            logger.info('VirusTotal checked %s', url)
        except Exception as exc:
            info['virustotal'] = f'error: {exc}'
            logger.error('VirusTotal check failed for %s: %s', url, exc)
    else:
        info['virustotal'] = 'no_api_key'

    return info
