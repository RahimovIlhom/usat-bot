# Generated by Django 4.2.13 on 2024-07-14 23:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_alter_applicant_passportimageback_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='olympian',
            name='result',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Imtihon natijasi'),
        ),
    ]
