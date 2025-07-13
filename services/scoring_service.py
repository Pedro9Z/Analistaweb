from typing import Dict

from . import logger


def compute_score(results: Dict[str, Dict[str, str]]) -> int:
    score = 0
    bl = results.get('blacklists', {})
    if any(bl.get(key) == 'listed' for key in ['google_safe_browsing', 'phishtank', 'urlhaus', 'virustotal']):
        score += 50
        logger.info('Blacklist hit detected')
    if results.get('redirect', {}).get('history'):
        score += 10
    if 'error' in results.get('tls', {}):
        score += 20
    if not results.get('dns', {}).get('SPF'):
        score += 5
    final_score = min(score, 100)
    logger.info('Computed risk score: %s', final_score)
    return final_score
