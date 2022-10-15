from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('recsysweb', '0002_interaction'),
    ]

    operations = [
        migrations.RunSQL("ALTER TABLE recsys.auth_user AUTO_INCREMENT=5000")
    ]