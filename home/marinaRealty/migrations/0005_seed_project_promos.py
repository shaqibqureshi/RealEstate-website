from django.db import migrations


def seed_promos(apps, schema_editor):
    ProjectPromo = apps.get_model('marinaRealty', 'ProjectPromo')
    promos = [
        {
            'project_name': 'Lodha Malad Heights',
            'builder_name': 'Lodha Group',
            'location': 'Malad West, Mumbai',
            'configuration': '2 & 3 BHK',
            'starting_price': '₹1.25 Cr onwards',
            'highlight': '🔥 Most Selling in Malad',
            'order': 0,
        },
        {
            'project_name': 'Oberoi Andheri Skies',
            'builder_name': 'Oberoi Realty',
            'location': 'Andheri West, Mumbai',
            'configuration': '3 & 4 BHK',
            'starting_price': '₹3.40 Cr onwards',
            'highlight': 'New Launch',
            'order': 1,
        },
        {
            'project_name': 'Godrej Borivali Exquisite',
            'builder_name': 'Godrej Properties',
            'location': 'Borivali East, Mumbai',
            'configuration': '1 & 2 BHK',
            'starting_price': '₹85 L onwards',
            'highlight': 'Selling Fast',
            'order': 2,
        },
        {
            'project_name': 'Piramal Goregaon Residences',
            'builder_name': 'Piramal Realty',
            'location': 'Goregaon West, Mumbai',
            'configuration': '2 & 3 BHK',
            'starting_price': '₹1.90 Cr onwards',
            'highlight': 'Featured Project',
            'order': 3,
        },
        {
            'project_name': 'Runwal Thane Gardens',
            'builder_name': 'Runwal Group',
            'location': 'Thane West, Thane',
            'configuration': '1/2/3 BHK',
            'starting_price': '₹62 L onwards',
            'highlight': 'Most Selling in Thane',
            'order': 4,
        },
    ]
    for entry in promos:
        ProjectPromo.objects.get_or_create(
            project_name=entry['project_name'], defaults=entry
        )


def unseed_promos(apps, schema_editor):
    ProjectPromo = apps.get_model('marinaRealty', 'ProjectPromo')
    ProjectPromo.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('marinaRealty', '0004_projectpromo'),
    ]

    operations = [
        migrations.RunPython(seed_promos, unseed_promos),
    ]