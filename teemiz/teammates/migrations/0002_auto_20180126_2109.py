# Generated by Django 2.0 on 2018-01-26 19:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teammates', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobreview',
            name='related_job',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teammates.TeamRequiredProfession'),
        ),
    ]