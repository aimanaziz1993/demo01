# Generated by Django 3.0.4 on 2020-03-26 02:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0002_auto_20200326_0822'),
    ]

    operations = [
        migrations.AddField(
            model_name='dun',
            name='code_name',
            field=models.CharField(max_length=3, null=True, verbose_name='DUN Code'),
        ),
    ]
