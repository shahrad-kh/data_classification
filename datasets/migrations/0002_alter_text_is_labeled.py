# Generated by Django 4.2.16 on 2024-10-30 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='text',
            name='is_labeled',
            field=models.BooleanField(default=False),
        ),
    ]
