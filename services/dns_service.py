import dns.resolver
from typing import Dict

from . import logger


def check_dns(domain: str) -> Dict[str, str]:
    """Resolve domain and return DNS information."""
    info = {}
    try:
        a_records = dns.resolver.resolve(domain, 'A')
        info['A'] = ', '.join([r.to_text() for r in a_records])
        logger.info('DNS A records for %s: %s', domain, info['A'])
    except Exception as exc:
        info['A'] = f'error: {exc}'
        logger.error('DNS resolution failed for %s: %s', domain, exc)
    # SPF record
    try:
        txt_records = dns.resolver.resolve(domain, 'TXT')
        for r in txt_records:
            if r.to_text().startswith('"v=spf1'):
                info['SPF'] = r.to_text().strip('"')
                logger.info('SPF record for %s: %s', domain, info['SPF'])
    except Exception as exc:
        info.setdefault('SPF', 'not found')
        logger.error('SPF lookup failed for %s: %s', domain, exc)
    return info
