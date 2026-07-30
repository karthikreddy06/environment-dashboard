# 🌊 Environmental Intelligence Dashboard with WDPA Integration

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-6.0-092E20.svg?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![SQLite](https://img.shields.io/badge/SQLite-Database-003B57.svg?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-ML%20Module-F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Chart.js](https://img.shields.io/badge/Chart.js-v4.4-FF6384.svg?style=for-the-badge&logo=chart.js&logoColor=white)](https://www.chartjs.org/)
[![Leaflet](https://img.shields.io/badge/Leaflet-v1.9.4-199900.svg?style=for-the-badge&logo=leaflet&logoColor=white)](https://leafletjs.com/)
[![License](https://img.shields.io/badge/License-MIT-purple.svg?style=for-the-badge)](LICENSE)

An enterprise-grade, high-performance Django web application and environmental analytics platform designed to ingest, process, visualize, and analyze the official **World Database on Protected Areas (WDPA)** dataset containing over **314,670+ Marine Protected Areas (MPAs)** worldwide alongside Machine Learning-driven environmental impact predictions.

---

## 📋 Table of Contents

- [📌 Overview](#-overview)
- [🚀 Key Features](#-key-features)
- [🛠️ Tech Stack](#️-tech-stack)
- [🏛️ Project Architecture](#️-project-architecture)
- [📂 Folder Structure](#-folder-structure)
- [📥 Installation & Setup](#-installation--setup)
- [⚡ Running Locally](#-running-locally)
- [🗄️ Database Setup](#️-database-setup)
- [📥 WDPA Dataset Import](#-wdpa-dataset-import)
- [📊 Dashboard Features](#-dashboard-features)
- [🤖 AI Prediction Module](#-ai-prediction-module)
- [📄 Reports & Export Center](#-reports--export-center)
- [📈 Advanced Analytics](#-advanced-analytics)
- [🗺️ Interactive World Map](#️-interactive-world-map)
- [📸 Screenshots](#-screenshots)
- [🔮 Future Enhancements](#-future-enhancements)
- [📄 License](#-license)

---

## 📌 Overview

The **Environmental Intelligence Dashboard** bridges data science and marine conservation management. By importing global WDPA data, the system provides real-time aggregations, spatial GIS mapping, comparative regional analysis, automated reporting engines, and AI risk prediction models. 

### Why This Project Matters
- **Global Marine Protection**: Tracks progress towards international environmental targets (e.g., 30x30 target for global marine protection).
- **High-Throughput Analytics**: Processes 300,000+ spatial data records in under 100 milliseconds using optimized indexed database queries and server-side memory caching.
- **Actionable Reporting**: Provides instant export capability to PDF, Excel (.xlsx), and CSV formats for environmental policymakers and researchers.

---

## 🚀 Key Features

- **🌐 Live Analytics Dashboard**: Dynamic KPI aggregations, Chart.js visualizations (Designations, IUCN Categories, Governance types, Status trends), and high-speed data tables.
- **🗺️ Interactive World Map**: Leaflet.js mapping with marker clustering (`L.markerClusterGroup`), density heatmap layers, 7 multi-select filter controls, real-time map statistics, and detailed WDPA metadata popups.
- **🌍 Country Analytics Module**: Deep-dive nation analytics across 273 countries/territories with nation-specific KPIs, custom comparison charts, and server-side pagination.
- **📄 Reports & Export Center**: Multi-criteria query builder with instant downloads in **CSV**, formatted **Excel (.xlsx)** (via `openpyxl`), and publication-ready **PDF** (via `ReportLab`).
- **📈 Advanced Analytics Engine**: Side-by-side comparative engine across Nations, Realms, Governance types, and IUCN classes with automatically generated environmental insights.
- **🤖 AI Environmental Predictor**: Scikit-Learn ML module using pre-trained regression models to forecast environmental risk and carbon/emission impacts based on country demographic and environmental parameters.
- **⚡ In-Memory Caching & Performance**: Integrated Django `LocMemCache` caching querysets and metadata dropdown choices for low latency.
- **🔒 Enterprise Security**: Environment-driven settings, WhiteNoise static asset compression, custom 404/500 handlers, and hardened security headers (`XSS Protection`, `NoSniff`, `X-Frame-Options`, `HTTPOnly`).

---

## 🛠️ Tech Stack

| Category | Technologies |
| :--- | :--- |
| **Backend Framework** | Python 3.10+, Django 6.0 |
| **Database** | SQLite (Indexed for high-speed aggregations on `wdpa_pid`, `country`, `realm`, `status_year`, `gis_area`) |
| **Data Engineering** | Python `pandas`, `chunked streaming CSV importer` |
| **Machine Learning** | `scikit-learn`, `joblib`, `numpy`, `pandas` |
| **Frontend & UI** | HTML5, Vanilla CSS, FontAwesome 6, Google Fonts (Inter) |
| **Data Visualization** | Chart.js v4.4, Leaflet.js v1.9.4, Leaflet MarkerCluster, Leaflet Heat |
| **Export Engines** | `ReportLab` (PDF), `openpyxl` (Excel), Python `csv` module (CSV) |
| **Production Serving** | `Gunicorn`, `WhiteNoise` (Compressed Manifest Static Storage) |

---

## 🏛️ Project Architecture

```
                                  +-----------------------+
                                  |     Client Browser    |
                                  +-----------+-----------+
                                              |
                                     HTTP Requests (REST/HTML)
                                              |
                                              v
                                  +-----------+-----------+
                                  | Gunicorn / WhiteNoise |
                                  +-----------+-----------+
                                              |
                                              v
                                  +-----------+-----------+
                                  |     Django 6.0 App    |
                                  |    (config & env)     |
                                  +-----+-----+-----+-----+
                                        |     |     |
            +---------------------------+     |     +---------------------------+
            |                                 |                                 |
            v                                 v                                 v
  +---------+---------+             +---------+---------+             +---------+---------+
  | In-Memory Cache   |             |   SQLite Database   |             |   Scikit-Learn    |
  |  (LocMemCache)    |             | (314k+ MPA Records) |             |  AI ML Predictor  |
  +-------------------+             +-------------------+             +-------------------+
```

---

## 📂 Folder Structure

```
environment_dashboard/
├── config/                     # Django Project Configuration
│   ├── __init__.py
│   ├── asgi.py                 # ASGI entry point
│   ├── settings.py             # App settings, CACHES, WhiteNoise, Security
│   ├── urls.py                 # Root URL routing & custom error handlers
│   └── wsgi.py                 # WSGI production entry point
├── environment/                # Core Django Application
│   ├── country_coordinates.py  # ISO3 Country Centroid lookup dictionary
│   ├── migrations/             # Database migration files
│   ├── ml/                     # AI Prediction Module
│   │   ├── encoder.pkl         # Trained Label Encoder
│   │   ├── model.pkl           # Trained ML Regression Model
│   │   ├── predict.py          # Standalone prediction test script
│   │   └── train_model.py      # ML Model training pipeline
│   ├── models.py               # MarineProtectedArea, Prediction, EnvironmentalData
│   ├── static/                 # CSS & JavaScript assets
│   ├── templates/              # HTML Templates
│   │   ├── 404.html            # Custom 404 Error Page
│   │   ├── 500.html            # Custom 500 Error Page
│   │   └── environment/        # Dashboard view templates
│   ├── tests.py                # Unit test suite (12 test cases)
│   ├── urls.py                 # Application routes & export endpoints
│   └── views.py                # View controllers & export engines
├── dataset/                    # Data Directory
│   ├── marine_protected_area_clean.csv # Cleaned WDPA dataset
│   ├── WDPA_sources_Jul2026.csv        # Metadata sources file
│   └── Environmental_AI_Dataset_Starter.xlsx # AI training dataset
├── import_data.py              # Streaming bulk data importer
├── manage.py                   # Django CLI management script
├── requirements.txt            # Locked project dependencies
├── .gitignore                  # Git exclusion rules
└── README.md                   # Comprehensive project documentation
```

---

## 📥 Installation & Setup

### 1. Prerequisites
- Python 3.10 or higher
- Git

### 2. Clone the Repository
```bash
git clone https://github.com/your-username/environment_dashboard.git
cd environment_dashboard
```

### 3. Create & Activate Virtual Environment
```bash
# Create virtual environment
python -m venv .venv

# Activate on Windows (PowerShell):
.venv\Scripts\Activate.ps1

# Activate on macOS / Linux:
source .venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## ⚡ Running Locally

### Start Development Server
```bash
python manage.py runserver
```
Open your browser and navigate to `http://127.0.0.1:8000/`.

---

## 🗄️ Database Setup

Run database migrations to initialize the schema:
```bash
python manage.py migrate
```

### Database Indexes Included:
- Primary key index on `id`
- Unique index on `wdpa_pid`
- Multi-column indexes on `country`, `country_code`, `realm`, `status_year`, `gis_area`

---

## 📥 WDPA Dataset Import

Import the World Database on Protected Areas dataset using the high-performance streaming importer:

```bash
python import_data.py
```

### Features of the Importer:
- Automatically detects candidate dataset files in `dataset/`.
- Uses chunked streaming (`chunksize=10000`) for memory-efficient loading.
- Pre-populates ISO3 country code mappings and centroid coordinates.
- Imports 300,000+ records in less than 60 seconds with bulk transaction committing.

---

## 📊 Dashboard Features

The primary landing page (`/`) presents executive-level metrics and interactive visual charts:

| Feature | Description |
| :--- | :--- |
| **KPI Metrics Cards** | Total MPAs, Total Protected Area (km²), Unique Countries, Designated Sites, IUCN Top Category, Dominant Realm. |
| **Designation Breakdown** | Pie chart illustrating National, International, and Regional protected designations. |
| **IUCN Categories Chart** | Bar chart breaking down IUCN conservation management levels (Ia, Ib, II, III, IV, V, VI). |
| **Governance Distribution** | Donut chart detailing Federal, State, Indigenous, and Private management. |
| **Designation Timeline** | Line chart tracking annual MPA creation over time. |

---

## 🤖 AI Prediction Module

The application features an integrated Machine Learning prediction engine located in `environment/ml/`:

- **Model Architecture**: Pre-trained regression models (`model.pkl`) using `scikit-learn` and `joblib`.
- **Inputs**: Country, Target Year, Population, GDP per Capita, Forest Area %, Renewable Energy %, PM2.5 levels, Average Temperature.
- **Outputs**: Forecasted CO2 Emissions (Million Tons) and Protected Area Expansion metrics.
- **Training Pipeline**: `train_model.py` provides a reproducible training pipeline using historical environmental indicators.

---

## 📄 Reports & Export Center

The Reports & Export Center (`/reports/`) provides multi-criteria filtering and instant document generation:

| Format | Endpoint | Technology | Features |
| :--- | :--- | :--- | :--- |
| **CSV** | `/export-csv/` | Native Python `csv` | Streaming chunked download of custom-filtered datasets. |
| **Excel** | `/export-excel/` | `openpyxl` | Formatted `.xlsx` spreadsheet with styled headers and dynamic columns. |
| **PDF** | `/export-pdf/` | `ReportLab` | Publication-grade executive summary report with tabular layout. |

---

## 📈 Advanced Analytics

The Advanced Analytics Dashboard (`/analytics/`) delivers high-level comparative insights:

- **Comparative Engine**: Side-by-side comparative analysis between two selected Nations, Governance types, or Realms.
- **Automated Insights**: Dynamically generated natural language summaries highlighting top performing conservation zones.
- **Data Drill-Down**: Direct inspection of individual WDPA records with full attribute inspection.

---

## 🗺️ Interactive World Map

The GIS Mapping module (`/map/`) offers visual exploration of global Marine Protected Areas:

- **Cluster Mapping**: Uses Leaflet `MarkerClusterGroup` for rendering thousands of spatial markers smoothly.
- **Density Heatmap**: Toggleable heatmap layer visualizing concentration of protected zones.
- **Filter Controls**: 7 interactive filter inputs (Country, Realm, IUCN Category, Designation Type, Status, Year Range, Area Range).
- **Metadata Popups**: Rich click popups containing 12 WDPA metadata fields including managing authority and GIS area.

---

## 📸 Screenshots

*(Add screenshot images of the dashboard interfaces here before publishing)*

| Interface | View Description |
| :--- | :--- |
| **Home Dashboard** | Executive summary metrics and real-time Chart.js charts. |
| **Interactive Map** | Global Leaflet cluster map with interactive filters. |
| **Country Analytics** | Nation-specific deep dive metrics and temporal trends. |
| **Reports Center** | Query builder and multi-format document exporter. |
| **AI Predictor** | Machine learning environmental forecasting interface. |

---

## 🔮 Future Enhancements

- [ ] **Real-time Satellite Feed Integration**: Incorporate Sentinel-2 satellite imagery overlays for active MPA monitoring.
- [ ] **PostGIS Spatial Database**: Migrate SQLite to PostgreSQL / PostGIS for advanced GIS spatial polygon queries.
- [ ] **Expanded ML Models**: Deep Learning model for ocean temperature anomaly predictions.
- [ ] **REST API Endpoints**: Django REST Framework (DRF) API for public data integration.

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.
