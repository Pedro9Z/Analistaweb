# Analistaweb

Aplicación CLI y API REST para analizar URLs y determinar su nivel de riesgo.

## Instalación

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Copie `.env.example` a `.env` y añada sus claves de API.

El analizador genera logs rotativos en `analistaweb.log` y respeta las restricciones de `robots.txt`.

## Uso CLI

```bash
python main.py https://ejemplo.com -o informe.json
```

Se generará también `informe.md` y puede convertirse a PDF.

## API REST

```bash
python main.py --api
```

Luego realizar un `POST` a `http://localhost:8000/scan` con JSON `{ "url": "https://ejemplo.com" }`.

## Makefile

- `make lint` ejecuta ruff.
- `make test` ejecuta pytest.
- `make run` ejecuta un análisis de ejemplo.
