# Generated by Django 2.0 on 2018-01-25 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teemizone', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='techskill',
            name='industry',
        ),
        migrations.AddField(
            model_name='techskill',
            name='industry',
            field=models.ManyToManyField(to='teemizone.Industry'),
        ),
    ]
