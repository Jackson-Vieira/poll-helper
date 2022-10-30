# Generated by Django 3.2.16 on 2022-10-20 00:02

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_alter_topic_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='topic',
            options={'ordering': ['-created'], 'verbose_name': 'Topic', 'verbose_name_plural': 'Topics'},
        ),
        migrations.AlterField(
            model_name='topic',
            name='id',
            field=models.UUIDField(default=uuid.UUID('84aae8fa-4be0-4829-afba-2bd9212bc10b'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
