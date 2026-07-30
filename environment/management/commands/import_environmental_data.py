import os
import pandas as pd

from django.conf import settings
from django.core.management.base import BaseCommand

from environment.models import EnvironmentalData


class Command(BaseCommand):
    help = "Import Environmental AI Dataset into SQLite"

    def handle(self, *args, **kwargs):

        dataset_path = os.path.join(
            settings.BASE_DIR,
            "dataset",
            "Environmental_AI_Dataset_Starter.xlsx"
        )

        if not os.path.exists(dataset_path):
            self.stdout.write(
                self.style.ERROR(
                    f"Dataset not found:\n{dataset_path}"
                )
            )
            return

        df = pd.read_excel(dataset_path)

        inserted = 0
        updated = 0

        for _, row in df.iterrows():

            obj, created = EnvironmentalData.objects.update_or_create(
                country=row["Country"],
                year=int(row["Year"]),
                defaults={
                    "population": float(row["Population_Millions"]),
                    "gdp_per_capita": float(row["GDP_per_Capita_USD"]),
                    "forest_area": float(row["Forest_Area_Percent"]),
                    "renewable_energy": float(row["Renewable_Energy_Percent"]),
                    "pm25": float(row["PM2_5"]),
                    "average_temperature": float(row["Average_Temperature_C"]),
                    "co2_emissions": float(row["CO2_Emissions_Mt"]),
                },
            )

            if created:
                inserted += 1
            else:
                updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"\nImport completed successfully!"
            )
        )

        self.stdout.write(f"Inserted : {inserted}")
        self.stdout.write(f"Updated  : {updated}")
        self.stdout.write(
            f"Total Rows: {EnvironmentalData.objects.count()}"
        )