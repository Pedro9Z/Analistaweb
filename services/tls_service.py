import ssl
import socket
from typing import Dict

from . import logger


def check_tls(domain: str) -> Dict[str, str]:
    info: Dict[str, str] = {}
    ctx = ssl.create_default_context()
    try:
        with ctx.wrap_socket(socket.socket(), server_hostname=domain) as s:
            s.settimeout(5)
            s.connect((domain, 443))
            cert = s.getpeercert()
            info['issuer'] = cert.get('issuer')
            info['notAfter'] = cert.get('notAfter')
            logger.info('TLS certificate for %s issuer %s', domain, info['issuer'])
    except Exception as exc:
        info['error'] = str(exc)
        logger.error('TLS check failed for %s: %s', domain, exc)
    return info
