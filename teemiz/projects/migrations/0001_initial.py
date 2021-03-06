# Generated by Django 2.0 on 2018-01-25 05:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('teemizone', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desired_tech', models.TextField(help_text='seperate each item with comma')),
                ('name', models.CharField(max_length=120)),
                ('excludes', models.TextField(blank=True, help_text='seperate each item with comma', null=True)),
                ('public', models.BooleanField(default=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('requrements', models.ManyToManyField(to='teemizone.Profession')),
                ('tools', models.ManyToManyField(to='teemizone.Tool')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-updated', '-timestamp'],
            },
        ),
    ]
