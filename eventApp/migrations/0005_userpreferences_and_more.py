# Generated by Django 4.0.1 on 2022-02-28 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventApp', '0004_mindfulnessevents_remove_events_leisure_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserPreferences',
            fields=[
                ('UserPreferenceID', models.AutoField(primary_key=True, serialize=False)),
                ('UserEmail', models.CharField(max_length=25)),
                ('UserPreference', models.CharField(max_length=50)),
                ('UserPreferenceDuration', models.IntegerField()),
                ('UserPreferenceNotes', models.CharField(max_length=500)),
            ],
        ),
        migrations.AlterField(
            model_name='mindfulnessevents',
            name='MindfulnessEventNotes',
            field=models.CharField(max_length=500),
        ),
    ]
