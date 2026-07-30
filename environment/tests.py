import json
from django.test import TestCase, Client
from django.urls import reverse
from environment.models import MarineProtectedArea, Prediction, EnvironmentalData


class EnvironmentDashboardTests(TestCase):
    def setUp(self):
        self.client = Client()

        # Create sample WDPA records for testing
        self.mpa1 = MarineProtectedArea.objects.create(
            wdpa_pid=1001,
            country_code="AUS",
            country="Australia",
            protected_area_name="Great Barrier Reef Marine Park",
            designation="Marine Park",
            designation_type="National",
            iucn_category="VI",
            realm="Marine",
            reported_area=344400.0,
            gis_area=344400.0,
            status="Designated",
            status_year=1975,
            governance_type="Federal Authority",
            management_authority="GBRMPA",
        )

        self.mpa2 = MarineProtectedArea.objects.create(
            wdpa_pid=1002,
            country_code="NZL",
            country="New Zealand",
            protected_area_name="Kermadec Islands Marine Reserve",
            designation="Marine Reserve",
            designation_type="National",
            iucn_category="Ia",
            realm="Marine",
            reported_area=7450.0,
            gis_area=7450.0,
            status="Designated",
            status_year=1990,
            governance_type="National Government",
            management_authority="DOC NZ",
        )

        self.env_data = EnvironmentalData.objects.create(
            country="Australia",
            year=2020,
            population=25.6,
            gdp_per_capita=51800.0,
            forest_area=17.4,
            renewable_energy=10.5,
            pm25=8.2,
            average_temperature=21.6,
            co2_emissions=15.4,
        )

    def test_model_creation(self):
        """Test MarineProtectedArea model representation and values."""
        self.assertEqual(str(self.mpa1), "Great Barrier Reef Marine Park")
        self.assertEqual(MarineProtectedArea.objects.count(), 2)

    def test_home_view(self):
        """Test Dashboard (home) view renders successfully with context metrics."""
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Great Barrier Reef Marine Park")
        self.assertIn("total_records", response.context)
        self.assertIn("total_countries", response.context)
        self.assertIn("top_countries_labels", response.context)

    def test_map_view(self):
        """Test World Map view renders successfully."""
        response = self.client.get(reverse("map"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("filter_countries", response.context)
        self.assertIn("filter_realms", response.context)

    def test_map_data_api(self):
        """Test Map Data API JSON endpoint returns markers and counts."""
        response = self.client.get(reverse("map_data"), {"country": "AUS"})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data["status"], "success")
        self.assertGreaterEqual(data["filtered_count"], 1)
        self.assertIn("markers", data)

    def test_countries_view(self):
        """Test Countries analytics view with search and pagination."""
        response = self.client.get(reverse("countries"), {"search": "Australia"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Australia")
        self.assertIn("page_obj", response.context)

    def test_reports_view(self):
        """Test Reports & Export Center view with multi-field filters."""
        response = self.client.get(reverse("reports"), {"country": "Australia", "realm": "Marine"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("total_filtered", response.context)
        self.assertEqual(response.context["total_filtered"], 1)

    def test_export_csv(self):
        """Test CSV export endpoint streams matching records."""
        response = self.client.get(reverse("export_csv"), {"country": "Australia"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/csv; charset=utf-8")
        self.assertIn("attachment; filename=", response["Content-Disposition"])
        self.assertIn(b"Great Barrier Reef Marine Park", response.content)

    def test_export_excel(self):
        """Test Excel (.xlsx) export endpoint generates valid spreadsheet."""
        response = self.client.get(reverse("export_excel"), {"country": "Australia"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response["Content-Type"],
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        self.assertGreater(len(response.content), 1000)

    def test_export_pdf(self):
        """Test PDF export endpoint generates valid PDF bytes."""
        response = self.client.get(reverse("export_pdf"), {"country": "Australia"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")
        self.assertGreater(len(response.content), 500)

    def test_analytics_view(self):
        """Test Advanced Analytics view with comparative analysis and drill-down."""
        response = self.client.get(
            reverse("analytics"),
            {"comp_type": "country", "item_a": "Australia", "item_b": "New Zealand"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("stats_a", response.context)
        self.assertIn("stats_b", response.context)

    def test_ai_prediction_view(self):
        """Test AI Prediction view status 200."""
        response = self.client.get(reverse("ai_prediction"))
        self.assertEqual(response.status_code, 200)

    def test_custom_404_handler(self):
        """Test non-existent route returns 404."""
        response = self.client.get("/non-existent-path-12345/")
        self.assertEqual(response.status_code, 404)
