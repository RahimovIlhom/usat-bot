# Generated by Django 4.2.13 on 2024-06-25 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_applicant_birthcountry_applicant_birthplace_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='science',
            name='deleted',
            field=models.BooleanField(default=False, verbose_name="Fan o'chirilganmi?"),
        ),
    ]
