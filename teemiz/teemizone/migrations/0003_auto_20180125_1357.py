# Generated by Django 2.0 on 2018-01-25 11:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teemizone', '0002_auto_20180125_0746'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profession',
            name='category',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='teemizone.Category'),
        ),
        migrations.AlterField(
            model_name='profession',
            name='industry',
            field=models.ManyToManyField(blank=True, to='teemizone.Industry'),
        ),
        migrations.AlterField(
            model_name='profession',
            name='skills',
            field=models.ManyToManyField(blank=True, to='teemizone.TechSkill'),
        ),
        migrations.AlterField(
            model_name='profession',
            name='tools',
            field=models.ManyToManyField(blank=True, to='teemizone.Tool'),
        ),
    ]
