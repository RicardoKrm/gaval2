import uuid
from django.db import migrations, models

def gen_uuid(apps, schema_editor):
    Empresa = apps.get_model('tenants', 'Empresa')
    for row in Empresa.objects.all():
        row.api_key = uuid.uuid4()
        row.save(update_fields=['api_key'])

class Migration(migrations.Migration):

    dependencies = [
        ("tenants", "0001_initial"),
    ]

    operations = []
