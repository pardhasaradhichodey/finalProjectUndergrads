# Generated by Django 3.2.3 on 2021-07-09 19:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MedApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='testsoffered',
            unique_together={('CentreId', 'TestId')},
        ),
    ]