# Generated by Django 4.0.6 on 2022-07-09 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='extended',
            name='phone',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Phone Number'),
        ),
    ]
