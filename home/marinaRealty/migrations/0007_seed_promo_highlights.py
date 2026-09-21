from django.db import migrations


def seed_highlights(apps, schema_editor):
    ProjectPromo = apps.get_model('marinaRealty', 'ProjectPromo')
    highlights_by_project = {
        'Lodha Malad Heights': {
            'highlight': 'Most Selling in Malad',
            'highlights': 'Premium Amenities\nReady to Move\nLimited Units',
        },
        'Oberoi Andheri Skies': {
            'highlights': 'Skyline Views\n5-Star Clubhouse\nSample Flat Available',
        },
        'Godrej Borivali Exquisite': {
            'highlights': 'Affordable Luxury\nBank Approvals Ready\nEarly-Bird Offers',
        },
        'Piramal Goregaon Residences': {
            'highlights': 'RERA Registered\nHigh Rental Yield\n24x7 Security',
        },
        'Runwal Thane Gardens': {
            'highlights': 'Lakeside Locality\nFlexible Payment Plan\nPossession 2027',
        },
    }
    for promo in ProjectPromo.objects.all():
        data = highlights_by_project.get(promo.project_name)
        if not data:
            continue
        if data.get('highlight'):
            promo.highlight = data['highlight']
        if data.get('highlights'):
            promo.highlights = data['highlights']
        promo.save()


def unseed_highlights(apps, schema_editor):
    ProjectPromo = apps.get_model('marinaRealty', 'ProjectPromo')
    ProjectPromo.objects.update(highlights='')


class Migration(migrations.Migration):

    dependencies = [
        ('marinaRealty', '0006_projectpromo_highlights_alter_projectpromo_highlight_and_more'),
    ]

    operations = [
        migrations.RunPython(seed_highlights, unseed_highlights),
    ]