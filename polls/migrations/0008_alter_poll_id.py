# Generated by Django 3.2.16 on 2022-10-30 18:50

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0007_auto_20221030_1550'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll',
            name='id',
            field=models.UUIDField(default=uuid.UUID('48875434-0df2-496d-ad17-1b410081b662'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
