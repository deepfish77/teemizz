# Generated by Django 2.0 on 2018-01-28 23:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_project_selected_team'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='selected_team',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='selected_team', to='teammates.Team'),
        ),
    ]
