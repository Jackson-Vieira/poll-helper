# Generated by Django 4.1 on 2022-08-20 21:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='choice',
            options={'ordering': ['-votes']},
        ),
    ]
