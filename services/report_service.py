import json
from datetime import datetime
from pathlib import Path
from typing import Dict

from weasyprint import HTML

from . import logger


REPORTS_DIR = Path('reports')
REPORTS_DIR.mkdir(exist_ok=True)


def save_json(data: Dict, filename: str) -> Path:
    path = REPORTS_DIR / filename
    with open(path, 'w') as fh:
        json.dump(data, fh, indent=2)
    logger.info('Saved JSON report to %s', path)
    return path


def save_markdown(data: Dict, filename: str) -> Path:
    summary = f"## Reporte {datetime.utcnow().isoformat()}\n\n"
    for key, value in data.items():
        summary += f"- **{key}**: {value}\n"
    path = REPORTS_DIR / filename
    with open(path, 'w') as fh:
        fh.write(summary)
    logger.info('Saved Markdown report to %s', path)
    return path


def save_pdf(markdown_path: Path, filename: str) -> Path:
    html = HTML(markdown_path.as_posix())
    path = REPORTS_DIR / filename
    html.write_pdf(path)
    logger.info('Saved PDF report to %s', path)
    return path
