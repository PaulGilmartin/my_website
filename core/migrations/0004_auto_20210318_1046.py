# Generated by Django 3.1.7 on 2021-03-18 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_paper_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='paper',
            name='content_path',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='content_path',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
