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
