import argparse
import json
from urllib.parse import urlparse

from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn

from services import logger

from services.dns_service import check_dns
from services.whois_service import check_whois
from services.tls_service import check_tls
from services.redirect_service import follow_redirects
from services.blacklist_service import check_blacklists
from services.html_analyzer import analyze_html
from services.dynamic_analyzer import analyze_dynamic
from services.scoring_service import compute_score
from services.report_service import save_json, save_markdown
from services.robots_service import check_robots


def analyze(url: str) -> dict:
    parsed = urlparse(url)
    domain = parsed.netloc or parsed.path
    robots = check_robots(url)
    allowed = robots.get('allowed', True)
    results = {
        'dns': check_dns(domain),
        'whois': check_whois(domain),
        'tls': check_tls(domain),
        'redirect': follow_redirects(url),
        'blacklists': check_blacklists(url),
        'robots': robots,
        'html': analyze_html(url) if allowed else {'skipped': True},
        'dynamic': analyze_dynamic(url) if allowed else {'skipped': True},
    }
    results['score'] = compute_score(results)
    logger.info('Analysis for %s complete with score %s', url, results['score'])
    return results


def cli():
    parser = argparse.ArgumentParser(description='Analizador de seguridad web')
    parser.add_argument('url', help='URL a analizar')
    parser.add_argument('-o', '--output', help='archivo de salida JSON', default='report.json')
    parser.add_argument('--api', action='store_true', help='Iniciar API REST')
    args = parser.parse_args()

    if args.api:
        app = create_app()
        uvicorn.run(app, host='0.0.0.0', port=8000)
        return

    results = analyze(args.url)
    path_json = save_json(results, args.output)
    path_md = save_markdown(results, args.output.replace('.json', '.md'))
    print(json.dumps(results, indent=2))
    print(f'\nSe generaron:\n - {path_json}\n - {path_md}')
    logger.info('CLI analysis finished')


def create_app() -> FastAPI:
    app = FastAPI()

    @app.post('/scan')
    def scan(payload: dict):
        url = payload.get('url')
        if not url:
            return JSONResponse({'error': 'URL requerida'}, status_code=400)
        results = analyze(url)
        return results

    return app


if __name__ == '__main__':
    cli()
