# Generated by Django 4.0.4 on 2022-08-28 14:57

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Application', '0002_dokumenti_korisnik_alter_dokumenti_kreator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dokumenti',
            name='Korisnik',
            field=models.ManyToManyField(related_name='Korisnik', through='Application.Student_Dokument', to=settings.AUTH_USER_MODEL),
        ),
    ]
