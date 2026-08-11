from django.db import models
from django.utils import timezone


class MarineProtectedArea(models.Model):
    wdpa_pid = models.BigIntegerField(unique=True, db_index=True)
    country_code = models.CharField(max_length=3, blank=True, null=True, db_index=True)
    country = models.CharField(max_length=150, blank=True, null=True, db_index=True)
    protected_area_name = models.CharField(max_length=255, blank=True, null=True)
    designation = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    designation_type = models.CharField(max_length=100, blank=True, null=True)
    iucn_category = models.CharField(max_length=50, blank=True, null=True, db_index=True)
    realm = models.CharField(max_length=100, blank=True, null=True, db_index=True)
    reported_area = models.FloatField(blank=True, null=True)
    gis_area = models.FloatField(blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True, db_index=True)
    status_year = models.IntegerField(blank=True, null=True, db_index=True)
    governance_type = models.CharField(max_length=100, blank=True, null=True, db_index=True)
    management_authority = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        ordering = ["country_code", "protected_area_name", "wdpa_pid"]
        verbose_name = "Marine Protected Area"
        verbose_name_plural = "Marine Protected Areas"

    def __str__(self) -> str:
        return self.protected_area_name or f"WDPA {self.wdpa_pid}"


class Prediction(models.Model):
    country = models.CharField(max_length=100)
    year = models.IntegerField()
    population = models.FloatField()
    gdp = models.FloatField()
    forest = models.FloatField()
    renewable = models.FloatField()
    pm25 = models.FloatField()
    temperature = models.FloatField()
    prediction = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)


class EnvironmentalData(models.Model):
    country = models.CharField(max_length=100)
    year = models.IntegerField()
    population = models.FloatField()
    gdp_per_capita = models.FloatField()
    forest_area = models.FloatField()
    renewable_energy = models.FloatField()
    pm25 = models.FloatField()
    average_temperature = models.FloatField()
    co2_emissions = models.FloatField()

    class Meta:
        unique_together = ("country", "year")
        ordering = ["country", "year"]

    def __str__(self) -> str:
        return f"{self.country} ({self.year})"


class DashboardSummary(models.Model):
    id = models.IntegerField(primary_key=True, default=1, editable=False)
    total_records = models.BigIntegerField(default=0)
    total_countries = models.BigIntegerField(default=0)
    total_designations = models.BigIntegerField(default=0)
    total_realms = models.BigIntegerField(default=0)
    total_governance_types = models.BigIntegerField(default=0)
    total_iucn_categories = models.BigIntegerField(default=0)
    latest_year = models.IntegerField(blank=True, null=True)
    earliest_year = models.IntegerField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Dashboard Summary"
        verbose_name_plural = "Dashboard Summaries"

    def __str__(self) -> str:
        return "Dashboard Summary"


class CountrySummary(models.Model):
    country_code = models.CharField(max_length=3, unique=True, db_index=True)
    country = models.CharField(max_length=150)
    record_count = models.BigIntegerField(default=0)

    class Meta:
        ordering = ["country_code"]
        verbose_name = "Country Summary"
        verbose_name_plural = "Country Summaries"

    def __str__(self) -> str:
        return f"{self.country_code} - {self.record_count}"


class RealmSummary(models.Model):
    realm = models.CharField(max_length=100, unique=True, db_index=True)
    record_count = models.BigIntegerField(default=0)

    class Meta:
        ordering = ["realm"]
        verbose_name = "Realm Summary"
        verbose_name_plural = "Realm Summaries"

    def __str__(self) -> str:
        return f"{self.realm} - {self.record_count}"


class DesignationSummary(models.Model):
    designation = models.CharField(max_length=255, unique=True, db_index=True)
    record_count = models.BigIntegerField(default=0)

    class Meta:
        ordering = ["designation"]
        verbose_name = "Designation Summary"
        verbose_name_plural = "Designation Summaries"

    def __str__(self) -> str:
        return f"{self.designation} - {self.record_count}"


class GovernanceSummary(models.Model):
    governance_type = models.CharField(max_length=100, unique=True, db_index=True)
    record_count = models.BigIntegerField(default=0)

    class Meta:
        ordering = ["governance_type"]
        verbose_name = "Governance Summary"
        verbose_name_plural = "Governance Summaries"

    def __str__(self) -> str:
        return f"{self.governance_type} - {self.record_count}"


class StatusSummary(models.Model):
    status = models.CharField(max_length=100, unique=True, db_index=True)
    record_count = models.BigIntegerField(default=0)

    class Meta:
        ordering = ["status"]
        verbose_name = "Status Summary"
        verbose_name_plural = "Status Summaries"

    def __str__(self) -> str:
        return f"{self.status} - {self.record_count}"


class YearSummary(models.Model):
    year = models.IntegerField(unique=True, db_index=True)
    record_count = models.BigIntegerField(default=0)

    class Meta:
        ordering = ["year"]
        verbose_name = "Year Summary"
        verbose_name_plural = "Year Summaries"

    def __str__(self) -> str:
        return f"{self.year} - {self.record_count}"


class IUCNSummary(models.Model):
    iucn_category = models.CharField(max_length=50, unique=True, db_index=True)
    record_count = models.BigIntegerField(default=0)

    class Meta:
        ordering = ["iucn_category"]
        verbose_name = "IUCN Summary"
        verbose_name_plural = "IUCN Summaries"

    def __str__(self) -> str:
        return f"{self.iucn_category} - {self.record_count}"
