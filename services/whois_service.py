import whois
from typing import Dict

from . import logger


def check_whois(domain: str) -> Dict[str, str]:
    info = {}
    try:
        w = whois.whois(domain)
        info['creation_date'] = str(w.creation_date)
        info['expiration_date'] = str(w.expiration_date)
        info['registrar'] = w.registrar
    except Exception as exc:
        info['error'] = str(exc)
        logger.error('WHOIS lookup failed for %s: %s', domain, exc)
    else:
        logger.info('WHOIS lookup for %s successful', domain)
    return info
