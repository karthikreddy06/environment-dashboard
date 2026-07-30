import logging
import os
from pathlib import Path
from typing import Any, Optional

from django.db.models import Count

import django
import pandas as pd
from django.db import IntegrityError, transaction

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from environment.models import MarineProtectedArea

logger = logging.getLogger("wdpa_import")
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

BASE_DIR = Path(__file__).resolve().parent
DATASET_CANDIDATES = [
    BASE_DIR / "dataset" / "WDPA_Jul2026_Public_csv.csv",
    BASE_DIR / "dataset" / "WDPA_sources_Jul2026.csv",
    BASE_DIR / "dataset" / "marine_protected_area_clean.csv",
]

try:
    import pycountry  # type: ignore
except ImportError:  # pragma: no cover - optional dependency
    pycountry = None

ISO3_COUNTRY_MAP = {
    "ABW": "Aruba",
    "AFG": "Afghanistan",
    "AGO": "Angola",
    "AIA": "Anguilla",
    "ALA": "Åland Islands",
    "ALB": "Albania",
    "AND": "Andorra",
    "ARE": "United Arab Emirates",
    "ARG": "Argentina",
    "ARM": "Armenia",
    "ASM": "American Samoa",
    "ATA": "Antarctica",
    "ATF": "French Southern Territories",
    "ATG": "Antigua and Barbuda",
    "AUS": "Australia",
    "AUT": "Austria",
    "AZE": "Azerbaijan",
    "BDI": "Burundi",
    "BEL": "Belgium",
    "BEN": "Benin",
    "BES": "Bonaire, Sint Eustatius and Saba",
    "BFA": "Burkina Faso",
    "BGD": "Bangladesh",
    "BGR": "Bulgaria",
    "BHR": "Bahrain",
    "BHS": "Bahamas",
    "BIH": "Bosnia and Herzegovina",
    "BLM": "Saint Barthélemy",
    "BLR": "Belarus",
    "BLZ": "Belize",
    "BMU": "Bermuda",
    "BOL": "Bolivia",
    "BRA": "Brazil",
    "BRB": "Barbados",
    "BRN": "Brunei Darussalam",
    "BTN": "Bhutan",
    "BVT": "Bouvet Island",
    "BWA": "Botswana",
    "CAF": "Central African Republic",
    "CAN": "Canada",
    "CCK": "Cocos (Keeling) Islands",
    "CHE": "Switzerland",
    "CHL": "Chile",
    "CHN": "China",
    "CIV": "Côte d'Ivoire",
    "CMR": "Cameroon",
    "COD": "Democratic Republic of the Congo",
    "COG": "Republic of the Congo",
    "COK": "Cook Islands",
    "COL": "Colombia",
    "COM": "Comoros",
    "CPV": "Cabo Verde",
    "CRI": "Costa Rica",
    "CUB": "Cuba",
    "CUW": "Curaçao",
    "CXR": "Christmas Island",
    "CYM": "Cayman Islands",
    "CYP": "Cyprus",
    "CZE": "Czech Republic",
    "DEU": "Germany",
    "DJI": "Djibouti",
    "DMA": "Dominica",
    "DNK": "Denmark",
    "DOM": "Dominican Republic",
    "DZA": "Algeria",
    "ECU": "Ecuador",
    "EGY": "Egypt",
    "ERI": "Eritrea",
    "ESH": "Western Sahara",
    "ESP": "Spain",
    "EST": "Estonia",
    "ETH": "Ethiopia",
    "FIN": "Finland",
    "FJI": "Fiji",
    "FLK": "Falkland Islands (Malvinas)",
    "FRA": "France",
    "FRO": "Faroe Islands",
    "FSM": "Micronesia",
    "GAB": "Gabon",
    "GBR": "United Kingdom",
    "GEO": "Georgia",
    "GGY": "Guernsey",
    "GHA": "Ghana",
    "GIB": "Gibraltar",
    "GIN": "Guinea",
    "GLP": "Guadeloupe",
    "GMB": "Gambia",
    "GNB": "Guinea-Bissau",
    "GNQ": "Equatorial Guinea",
    "GRC": "Greece",
    "GRD": "Grenada",
    "GRL": "Greenland",
    "GTM": "Guatemala",
    "GUF": "French Guiana",
    "GUM": "Guam",
    "GUY": "Guyana",
    "HKG": "Hong Kong",
    "HMD": "Heard Island and McDonald Islands",
    "HND": "Honduras",
    "HRV": "Croatia",
    "HTI": "Haiti",
    "HUN": "Hungary",
    "IDN": "Indonesia",
    "IMN": "Isle of Man",
    "IND": "India",
    "IOT": "British Indian Ocean Territory",
    "IRL": "Ireland",
    "IRN": "Iran",
    "IRQ": "Iraq",
    "ISL": "Iceland",
    "ISR": "Israel",
    "ITA": "Italy",
    "JAM": "Jamaica",
    "JEY": "Jersey",
    "JOR": "Jordan",
    "JPN": "Japan",
    "KAZ": "Kazakhstan",
    "KEN": "Kenya",
    "KGZ": "Kyrgyzstan",
    "KHM": "Cambodia",
    "KIR": "Kiribati",
    "KNA": "Saint Kitts and Nevis",
    "KOR": "South Korea",
    "KWT": "Kuwait",
    "LAO": "Laos",
    "LBN": "Lebanon",
    "LBR": "Liberia",
    "LBY": "Libya",
    "LCA": "Saint Lucia",
    "LIE": "Liechtenstein",
    "LKA": "Sri Lanka",
    "LSO": "Lesotho",
    "LTU": "Lithuania",
    "LUX": "Luxembourg",
    "LVA": "Latvia",
    "MAC": "Macao",
    "MAF": "Saint Martin (French part)",
    "MAR": "Morocco",
    "MCO": "Monaco",
    "MDA": "Moldova",
    "MDG": "Madagascar",
    "MDV": "Maldives",
    "MEX": "Mexico",
    "MHL": "Marshall Islands",
    "MKD": "North Macedonia",
    "MLI": "Mali",
    "MLT": "Malta",
    "MMR": "Myanmar",
    "MNE": "Montenegro",
    "MNG": "Mongolia",
    "MNP": "Northern Mariana Islands",
    "MOZ": "Mozambique",
    "MRT": "Mauritania",
    "MSR": "Montserrat",
    "MTQ": "Martinique",
    "MUS": "Mauritius",
    "MWI": "Malawi",
    "MYS": "Malaysia",
    "MYT": "Mayotte",
    "NAM": "Namibia",
    "NCL": "New Caledonia",
    "NER": "Niger",
    "NFK": "Norfolk Island",
    "NGA": "Nigeria",
    "NIC": "Nicaragua",
    "NIU": "Niue",
    "NLD": "Netherlands",
    "NOR": "Norway",
    "NPL": "Nepal",
    "NRU": "Nauru",
    "NZL": "New Zealand",
    "OMN": "Oman",
    "PAK": "Pakistan",
    "PAN": "Panama",
    "PCN": "Pitcairn",
    "PER": "Peru",
    "PHL": "Philippines",
    "PLW": "Palau",
    "PNG": "Papua New Guinea",
    "POL": "Poland",
    "PRI": "Puerto Rico",
    "PRK": "North Korea",
    "PRT": "Portugal",
    "PRY": "Paraguay",
    "PSE": "Palestine",
    "PYF": "French Polynesia",
    "QAT": "Qatar",
    "REU": "Réunion",
    "ROU": "Romania",
    "RUS": "Russia",
    "RWA": "Rwanda",
    "SAU": "Saudi Arabia",
    "SDN": "Sudan",
    "SEN": "Senegal",
    "SGP": "Singapore",
    "SGS": "South Georgia and the South Sandwich Islands",
    "SHN": "Saint Helena",
    "SJM": "Svalbard and Jan Mayen",
    "SLB": "Solomon Islands",
    "SLE": "Sierra Leone",
    "SLV": "El Salvador",
    "SMR": "San Marino",
    "SOM": "Somalia",
    "SPM": "Saint Pierre and Miquelon",
    "SRB": "Serbia",
    "SSD": "South Sudan",
    "STP": "Sao Tome and Principe",
    "SUR": "Suriname",
    "SVK": "Slovakia",
    "SVN": "Slovenia",
    "SWE": "Sweden",
    "SWZ": "Eswatini",
    "SXM": "Sint Maarten (Dutch part)",
    "SYC": "Seychelles",
    "SYR": "Syria",
    "TCA": "Turks and Caicos Islands",
    "TCD": "Chad",
    "TGO": "Togo",
    "THA": "Thailand",
    "TJK": "Tajikistan",
    "TKL": "Tokelau",
    "TKM": "Turkmenistan",
    "TLS": "Timor-Leste",
    "TON": "Tonga",
    "TTO": "Trinidad and Tobago",
    "TUN": "Tunisia",
    "TUR": "Turkey",
    "TUV": "Tuvalu",
    "TWN": "Taiwan",
    "TZA": "Tanzania",
    "UGA": "Uganda",
    "UKR": "Ukraine",
    "UMI": "United States Minor Outlying Islands",
    "URY": "Uruguay",
    "USA": "United States",
    "UZB": "Uzbekistan",
    "VAT": "Holy See",
    "VCT": "Saint Vincent and the Grenadines",
    "VEN": "Venezuela",
    "VGB": "Virgin Islands (British)",
    "VIR": "Virgin Islands (U.S.)",
    "VNM": "Vietnam",
    "VUT": "Vanuatu",
    "WLF": "Wallis and Futuna",
    "WSM": "Samoa",
    "YEM": "Yemen",
    "ZAF": "South Africa",
    "ZMB": "Zambia",
    "ZWE": "Zimbabwe",
}


def resolve_dataset_path() -> Path:
    """Return the first available dataset path from the known candidates."""
    for path in DATASET_CANDIDATES:
        if path.exists():
            return path
    raise FileNotFoundError("No WDPA dataset file was found in the dataset directory.")


def detect_encoding(path: Path) -> str:
    """Detect a suitable CSV encoding without loading the full file into memory."""
    for encoding in ["utf-8-sig", "utf-8", "cp1252", "latin-1"]:
        try:
            with path.open("rb") as handle:
                handle.read(4096).decode(encoding)
            return encoding
        except UnicodeDecodeError:
            continue
    return "latin-1"


def clean_string(value: Any) -> Optional[str]:
    """Normalize string values and return None for empty or missing data."""
    if pd.isna(value):
        return None

    text = str(value).strip()
    if not text:
        return None

    text = text.replace("\x00", "").replace("\u0000", "")
    return text


def to_int(value: Any) -> Optional[int]:
    """Safely convert values into integers."""
    if pd.isna(value):
        return None

    if isinstance(value, str):
        cleaned = value.strip().replace(",", "")
        if not cleaned:
            return None
        try:
            return int(float(cleaned))
        except ValueError:
            return None

    try:
        return int(float(value))
    except (TypeError, ValueError):
        return None


def to_float(value: Any) -> Optional[float]:
    """Safely convert values into floats."""
    if pd.isna(value):
        return None

    if isinstance(value, str):
        cleaned = value.strip().replace(",", "")
        if not cleaned:
            return None
        try:
            return float(cleaned)
        except ValueError:
            return None

    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def normalize_column_name(column_name: Any) -> str:
    """Normalize a dataframe column name for consistent lookups."""
    text = str(column_name or "").strip().replace("\ufeff", "")
    return text.replace(" ", "_").replace("-", "_").lower()


def get_column_value(row: pd.Series, candidate_names: list[str]) -> Any:
    """Return a value from a row using normalized WDPA-like column names."""
    lookup = {normalize_column_name(column_name): column_name for column_name in row.index}
    for candidate_name in candidate_names:
        actual_name = lookup.get(normalize_column_name(candidate_name))
        if actual_name is not None:
            return row[actual_name]
    return None


def normalize_country_code(value: Any) -> Optional[str]:
    """Normalize country codes to uppercase ISO3 form when possible."""
    code = clean_string(value)
    if not code:
        return None
    return code.upper()


def resolve_country_name(country_code: Optional[str], fallback: Any) -> Optional[str]:
    """Resolve a country name using the internal mapping or pycountry when available."""
    if country_code:
        if pycountry is not None:
            try:
                country = pycountry.countries.get(alpha_3=country_code)
                if country is not None:
                    return country.name
            except Exception:
                pass

        mapped_name = ISO3_COUNTRY_MAP.get(country_code)
        if mapped_name:
            return mapped_name

        return country_code

    fallback_name = clean_string(fallback)
    return fallback_name or None


def build_record(row: pd.Series) -> Optional[MarineProtectedArea]:
    """Create a model instance from a cleaned dataframe row."""
    wdpa_pid = to_int(get_column_value(row, ["wdpa_pid", "WDPA_PID", "site_pid", "SITE_PID", "site_id", "SITE_ID", "wdpaid", "wdpa_id", "wdpa", "id"]))
    if wdpa_pid is None:
        return None

    country_code = normalize_country_code(get_column_value(row, ["iso3", "ISO3", "prnt_iso3", "PRNT_ISO3", "country_code", "country_iso3", "iso_3"]))
    country_name = resolve_country_name(
        country_code,
        get_column_value(row, ["country", "country_name", "name_eng", "NAME_ENG", "name", "NAME"]),
    )

    protected_area_name = clean_string(get_column_value(row, ["name_eng", "NAME_ENG", "name", "NAME", "site_name", "pa_name", "area_name"]))
    designation = clean_string(get_column_value(row, ["desig_eng", "DESIG_ENG", "desig", "DESIG", "designation", "designation_eng"]))
    designation_type = clean_string(get_column_value(row, ["desig_type", "DESIG_TYPE", "designation_type"]))
    iucn_category = clean_string(get_column_value(row, ["iucn_cat", "IUCN_CAT", "iucn_category", "category", "iucn"]))
    realm = clean_string(get_column_value(row, ["realm", "REALM"]))
    reported_area = to_float(get_column_value(row, ["rep_m_area", "REP_M_AREA", "rep_area", "REP_AREA", "reported_area", "rep_area_km2", "area_rep"]))
    gis_area = to_float(get_column_value(row, ["gis_m_area", "GIS_M_AREA", "gis_area", "GIS_AREA", "gis_area_km2", "area_gis", "area_sqkm"]))
    status = clean_string(get_column_value(row, ["status", "STATUS"]))
    status_year = to_int(get_column_value(row, ["status_yr", "STATUS_YR", "status_year", "year"]))
    governance_type = clean_string(get_column_value(row, ["gov_type", "GOV_TYPE", "governance_type", "governance"]))
    management_authority = clean_string(get_column_value(row, ["mang_auth", "MANG_AUTH", "management_authority", "management"]))

    return MarineProtectedArea(
        wdpa_pid=wdpa_pid,
        country_code=country_code,
        country=country_name,
        protected_area_name=protected_area_name,
        designation=designation,
        designation_type=designation_type,
        iucn_category=iucn_category,
        realm=realm,
        reported_area=reported_area,
        gis_area=gis_area,
        status=status,
        status_year=status_year,
        governance_type=governance_type,
        management_authority=management_authority,
    )


def validate_import_summary() -> dict[str, Any]:
    """Print and return a validation summary for the imported WDPA data."""
    queryset = MarineProtectedArea.objects
    total_records = queryset.count()

    countries = queryset.exclude(country_code__isnull=True).exclude(country_code="").values_list("country_code", flat=True).distinct().count()
    unique_designations = queryset.exclude(designation__isnull=True).exclude(designation="").values_list("designation", flat=True).distinct().count()
    unique_realms = queryset.exclude(realm__isnull=True).exclude(realm="").values_list("realm", flat=True).distinct().count()

    status_years = list(queryset.exclude(status_year__isnull=True).values_list("status_year", flat=True))
    earliest_year = min(status_years) if status_years else None
    latest_year = max(status_years) if status_years else None

    duplicate_wdpa_ids = (
        queryset.values("wdpa_pid")
        .annotate(duplicate_count=Count("wdpa_pid"))
        .filter(duplicate_count__gt=1)
        .count()
    )
    missing_country_codes = queryset.filter(country_code__isnull=True).count() + queryset.filter(country_code="").count()
    missing_names = queryset.filter(protected_area_name__isnull=True).count() + queryset.filter(protected_area_name="").count()
    missing_areas = queryset.filter(reported_area__isnull=True, gis_area__isnull=True).count()

    summary = {
        "total_records": total_records,
        "countries": countries,
        "unique_designations": unique_designations,
        "unique_realms": unique_realms,
        "earliest_status_year": earliest_year,
        "latest_status_year": latest_year,
        "duplicate_wdpa_ids": duplicate_wdpa_ids,
        "missing_country_codes": missing_country_codes,
        "missing_names": missing_names,
        "missing_areas": missing_areas,
    }

    logger.info("WDPA Import Summary")
    logger.info("Total Records: %s", summary["total_records"])
    logger.info("Countries: %s", summary["countries"])
    logger.info("Unique Designations: %s", summary["unique_designations"])
    logger.info("Unique Realms: %s", summary["unique_realms"])
    logger.info("Earliest Status Year: %s", summary["earliest_status_year"])
    logger.info("Latest Status Year: %s", summary["latest_status_year"])
    logger.info("Duplicate WDPA IDs: %s", summary["duplicate_wdpa_ids"])
    logger.info("Missing Country Codes: %s", summary["missing_country_codes"])
    logger.info("Missing Names: %s", summary["missing_names"])
    logger.info("Missing Areas: %s", summary["missing_areas"])

    passed = (
        total_records >= 0
        and duplicate_wdpa_ids == 0
        and missing_country_codes == 0
        and missing_names == 0
        and missing_areas == 0
    )
    logger.info("Database Status: %s", "PASS" if passed else "FAIL")
    return summary


def import_data() -> None:
    """Import WDPA data into the MarineProtectedArea model in batches."""
    dataset_path = resolve_dataset_path()
    logger.info("Reading dataset: %s", dataset_path)

    encoding = detect_encoding(dataset_path)
    logger.info("Using CSV encoding: %s", encoding)

    chunk_size = 10000
    batch_size = 5000
    logger.info("Streaming dataset in chunks of %s rows", chunk_size)

    imported_rows = 0
    skipped_rows = 0
    duplicate_rows = 0
    failed_rows = 0
    total_rows = 0

    reader = pd.read_csv(
        dataset_path,
        encoding=encoding,
        na_values=["", "NA", "N/A", "null", "None"],
        keep_default_na=True,
        chunksize=chunk_size,
        dtype=str,
    )

    try:
        with transaction.atomic():
            MarineProtectedArea.objects.all().delete()
            logger.info("Preparing import transaction")

            for chunk_number, chunk in enumerate(reader, start=1):
                total_rows += len(chunk)
                logger.info("Processing chunk %s with %s rows", chunk_number, len(chunk))

                batch: list[MarineProtectedArea] = []
                for row_number, row in chunk.iterrows():
                    try:
                        record = build_record(row)
                        if record is None:
                            skipped_rows += 1
                            continue

                        batch.append(record)
                    except Exception as exc:  # pragma: no cover - safety for import robustness
                        failed_rows += 1
                        logger.warning("Failed to build row %s: %s", row_number, exc)

                    if len(batch) >= batch_size:
                        created_objects = insert_batch(batch)
                        imported_rows += len(created_objects)
                        duplicate_rows += len(batch) - len(created_objects)
                        batch = []

                if batch:
                    created_objects = insert_batch(batch)
                    imported_rows += len(created_objects)
                    duplicate_rows += len(batch) - len(created_objects)

            logger.info(
                "Import summary - Imported: %s | Duplicates: %s | Skipped: %s | Failed: %s",
                imported_rows,
                duplicate_rows,
                skipped_rows,
                failed_rows,
            )
            validate_import_summary()
    except Exception as exc:  # pragma: no cover - safety for import robustness
        logger.exception("Import failed; transaction rolled back: %s", exc)
        raise


def insert_batch(batch: list[MarineProtectedArea]) -> list[MarineProtectedArea]:
    """Insert a batch of records using bulk_create with conflict handling."""
    if not batch:
        return []

    try:
        return MarineProtectedArea.objects.bulk_create(batch, batch_size=5000, ignore_conflicts=True)
    except IntegrityError as exc:
        logger.warning("Batch insert hit integrity error; retrying row-by-row: %s", exc)
    except Exception as exc:  # pragma: no cover - safety for import robustness
        logger.warning("Batch insert failed; retrying row-by-row: %s", exc)

    created_objects: list[MarineProtectedArea] = []
    for record in batch:
        try:
            MarineProtectedArea.objects.bulk_create([record], ignore_conflicts=True)
            created_objects.append(record)
        except IntegrityError:
            continue
        except Exception as exc:  # pragma: no cover - safety for import robustness
            logger.warning("Row insert failed for WDPA %s: %s", record.wdpa_pid, exc)
    return created_objects


if __name__ == "__main__":
    import_data()