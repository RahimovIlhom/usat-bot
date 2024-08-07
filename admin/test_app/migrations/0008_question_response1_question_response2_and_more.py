# Generated by Django 4.2.13 on 2024-07-25 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0007_alter_examresult_totalscore'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='response1',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Javob 1'),
        ),
        migrations.AddField(
            model_name='question',
            name='response2',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Javob 2'),
        ),
        migrations.AddField(
            model_name='question',
            name='response3',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Javob 3'),
        ),
        migrations.AddField(
            model_name='question',
            name='response4',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Javob 4'),
        ),
        migrations.AlterField(
            model_name='question',
            name='trueResponse',
            field=models.CharField(choices=[('a', 'a'), ('b', 'b'), ('c', 'c'), ('d', 'd')], default='a', max_length=1, verbose_name="To'g'ri javob"),
        ),
    ]
