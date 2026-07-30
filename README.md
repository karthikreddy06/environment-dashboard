# Environmental Intelligence Dashboard

[![Python](https://img.shields.io/badge/Python-3.12%2B-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-6.0-092E20.svg)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)

A Django web application for importing, exploring, and reporting on marine protected-area and environmental datasets. It includes interactive dashboards, country comparisons, map views, CSV/Excel/PDF exports, and a pre-trained environmental prediction interface.

## Features

- Dashboard metrics and charts for protected-area data
- Country analytics, filtering, and comparison views
- Interactive map data endpoint and Leaflet-based map interface
- Filtered CSV, Excel, and PDF report exports
- WDPA-oriented streaming data import utility
- Pre-trained AI prediction module

## Technology

- Python 3.12+ and Django 6
- SQLite for local development
- pandas and scikit-learn for data processing and existing prediction assets
- openpyxl and ReportLab for exports
- WhiteNoise and Gunicorn for production serving

## Quick start

```bash
git clone https://github.com/karthikreddy06/environment-dashboard.git
cd environment-dashboard
python -m venv .venv
```

Activate the environment, then install dependencies:

```bash
# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

Copy `.env.example` to `.env` and set a unique `SECRET_KEY`. Then initialize and run the application:

```bash
python manage.py migrate
python manage.py runserver
```

Open <http://127.0.0.1:8000/>.

## Configuration

| Variable | Purpose | Required in production |
| --- | --- | --- |
| `SECRET_KEY` | Django cryptographic signing key | Yes |
| `DEBUG` | Enables Django debug mode | Yes (`False`) |
| `ALLOWED_HOSTS` | Comma-separated hostnames | Yes |

The project uses SQLite by default. `DATABASE_URL` and cache variables in `.env.example` are documentation placeholders; they are not currently consumed by application settings.

## Data import

Place supported source data in `dataset/`, then run:

```bash
python import_data.py
```

The repository includes small source and starter datasets used by the project. Verify the terms and provenance of refreshed WDPA data before redistributing it.

## Validation

```bash
python manage.py check
python manage.py test
```

## Security

Never commit secrets, local `.env` files, generated databases, or private datasets. See [SECURITY.md](SECURITY.md) for vulnerability reporting guidance.

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
