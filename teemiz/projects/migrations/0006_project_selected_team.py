# Generated by Django 2.0 on 2018-01-29 00:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teammates', '0002_auto_20180126_2109'),
        ('projects', '0005_remove_project_selected_team'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='selected_team',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, related_name='selected_team', to='teammates.Team'),
        ),
    ]