# Generated by Django 4.0.1 on 2022-03-23 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventApp', '0007_alter_events_eventname_alter_events_location_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='events',
            name='EventName',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='mindfulnessevents',
            name='MindfulnessEventName',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='stresssurvey',
            name='UserEmail',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='userpreferences',
            name='UserEmail',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='userpreferences',
            name='UserPreference',
            field=models.CharField(max_length=100),
        ),
    ]
