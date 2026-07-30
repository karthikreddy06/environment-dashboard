from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("analytics/", views.analytics, name="analytics"),
    path("countries/", views.countries, name="countries"),
    path("map/", views.map, name="map"),
    path("map/data/", views.map_data, name="map_data"),
    path("reports/", views.reports, name="reports"),

    path("export-csv/", views.export_csv, name="export_csv"),
    path("export-excel/", views.export_excel, name="export_excel"),
    path("export-pdf/", views.export_pdf, name="export_pdf"),

    path("ai-prediction/", views.ai_prediction, name="ai_prediction"),

    # AJAX API
    path(
        "get-environment-data/",
        views.get_environment_data,
        name="get_environment_data",
    ),
]