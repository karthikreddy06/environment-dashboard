from django.core.management.base import BaseCommand
from django.db import transaction, models
from environment.models import (
    MarineProtectedArea,
    DashboardSummary,
    CountrySummary,
    RealmSummary,
    DesignationSummary,
    GovernanceSummary,
    StatusSummary,
    YearSummary,
    IUCNSummary,
)


class Command(BaseCommand):
    help = "Build precomputed summary tables from MarineProtectedArea data"

    def handle(self, *args, **options):
        source_count = MarineProtectedArea.objects.count()
        self.stdout.write(f"Source records: {source_count}")

        if source_count == 0:
            self.stdout.write(self.style.ERROR("No MarineProtectedArea records found. Aborting."))
            return

        self.stdout.write("Clearing summary tables...")
        with transaction.atomic():
            DashboardSummary.objects.all().delete()
            CountrySummary.objects.all().delete()
            RealmSummary.objects.all().delete()
            DesignationSummary.objects.all().delete()
            GovernanceSummary.objects.all().delete()
            StatusSummary.objects.all().delete()
            YearSummary.objects.all().delete()
            IUCNSummary.objects.all().delete()

        self.stdout.write("Building DashboardSummary...")
        with transaction.atomic():
            agg = MarineProtectedArea.objects.aggregate(
                total_records=models.Count('wdpa_pid'),
                total_countries=models.Count('country_code', distinct=True),
                total_designations=models.Count('designation', distinct=True),
                total_governance_types=models.Count('governance_type', distinct=True),
                total_realms=models.Count('realm', distinct=True),
                total_statuses=models.Count('status', distinct=True),
                total_iucn_categories=models.Count('iucn_category', distinct=True),
                earliest_year=models.Min('status_year'),
                latest_year=models.Max('status_year'),
                total_reported_area=models.Sum('reported_area'),
                total_gis_area=models.Sum('gis_area'),
                avg_reported_area=models.Avg('reported_area'),
                avg_gis_area=models.Avg('gis_area'),
            )
            DashboardSummary.objects.create(
                id=1,
                total_records=agg['total_records'] or 0,
                total_countries=agg['total_countries'] or 0,
                total_designations=agg['total_designations'] or 0,
                total_realms=agg['total_realms'] or 0,
                total_governance_types=agg['total_governance_types'] or 0,
                total_iucn_categories=agg['total_iucn_categories'] or 0,
                earliest_year=agg['earliest_year'],
                latest_year=agg['latest_year'],
                # Note: model does not have area totals/averages fields; only defined fields.
                # We'll store only fields defined in model.
                # If model later extended, adjust accordingly.
                # updated_at auto_now
            )

        self.stdout.write("Building CountrySummary...")
        with transaction.atomic():
            qs = MarineProtectedArea.objects.values('country_code', 'country').annotate(
                record_count=models.Count('wdpa_pid')
            )
            objs = [
                CountrySummary(country_code=row['country_code'] or '', country=row['country'] or '', record_count=row['record_count'])
                for row in qs
            ]
            CountrySummary.objects.bulk_create(objs, ignore_conflicts=True)

        self.stdout.write("Building RealmSummary...")
        with transaction.atomic():
            qs = MarineProtectedArea.objects.values('realm').annotate(
                record_count=models.Count('wdpa_pid')
            )
            objs = [
                RealmSummary(realm=row['realm'] or '', record_count=row['record_count'])
                for row in qs
            ]
            RealmSummary.objects.bulk_create(objs, ignore_conflicts=True)

        self.stdout.write("Building DesignationSummary...")
        with transaction.atomic():
            qs = MarineProtectedArea.objects.values('designation').annotate(
                record_count=models.Count('wdpa_pid')
            )
            objs = [
                DesignationSummary(designation=row['designation'] or '', record_count=row['record_count'])
                for row in qs
            ]
            DesignationSummary.objects.bulk_create(objs, ignore_conflicts=True)

        self.stdout.write("Building GovernanceSummary...")
        with transaction.atomic():
            qs = MarineProtectedArea.objects.values('governance_type').annotate(
                record_count=models.Count('wdpa_pid')
            )
            objs = [
                GovernanceSummary(governance_type=row['governance_type'] or '', record_count=row['record_count'])
                for row in qs
            ]
            GovernanceSummary.objects.bulk_create(objs, ignore_conflicts=True)

        self.stdout.write("Building StatusSummary...")
        with transaction.atomic():
            qs = MarineProtectedArea.objects.values('status').annotate(
                record_count=models.Count('wdpa_pid')
            )
            objs = [
                StatusSummary(status=row['status'] or '', record_count=row['record_count'])
                for row in qs
            ]
            StatusSummary.objects.bulk_create(objs, ignore_conflicts=True)

        self.stdout.write("Building YearSummary...")
        with transaction.atomic():
            qs = MarineProtectedArea.objects.values('status_year').annotate(
                record_count=models.Count('wdpa_pid')
            )
            objs = [
                YearSummary(year=row['status_year'], record_count=row['record_count'])
                for row in qs if row['status_year'] is not None
            ]
            YearSummary.objects.bulk_create(objs, ignore_conflicts=True)

        self.stdout.write("Building IUCNSummary...")
        with transaction.atomic():
            qs = MarineProtectedArea.objects.values('iucn_category').annotate(
                record_count=models.Count('wdpa_pid')
            )
            objs = [
                IUCNSummary(iucn_category=row['iucn_category'] or '', record_count=row['record_count'])
                for row in qs
            ]
            IUCNSummary.objects.bulk_create(objs, ignore_conflicts=True)

        self.stdout.write(self.style.SUCCESS("\nSummary generation complete."))

        # Report counts
        self.stdout.write(f"DashboardSummary: {DashboardSummary.objects.count()}")
        self.stdout.write(f"CountrySummary: {CountrySummary.objects.count()}")
        self.stdout.write(f"RealmSummary: {RealmSummary.objects.count()}")
        self.stdout.write(f"DesignationSummary: {DesignationSummary.objects.count()}")
        self.stdout.write(f"GovernanceSummary: {GovernanceSummary.objects.count()}")
        self.stdout.write(f"StatusSummary: {StatusSummary.objects.count()}")
        self.stdout.write(f"YearSummary: {YearSummary.objects.count()}")
        self.stdout.write(f"IUCNSummary: {IUCNSummary.objects.count()}")

        after_count = MarineProtectedArea.objects.count()
        self.stdout.write(f"Source records before: {source_count}")
        self.stdout.write(f"Source records after: {after_count}")