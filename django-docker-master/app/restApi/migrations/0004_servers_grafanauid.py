# Generated by Django 3.0.5 on 2021-05-20 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restApi', '0003_auto_20210520_1422'),
    ]

    operations = [
        migrations.AddField(
            model_name='servers',
            name='grafanaUid',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
