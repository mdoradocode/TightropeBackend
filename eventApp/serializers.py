from rest_framework import serializers
from eventApp.models import Events, MindfulnessEvents, UserPreferences, StressSurvey, Streaks

class EventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = ('EventID',
                    'UserEmail',
                    'EventName',
                    'StartDate',
                    'EndDate',
                    'Location',
                    'EventType',
                    'StressLevel',
                    'Notes')

class MindfulnessEventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MindfulnessEvents
        fields = ('MindfulnessEventID',
                    'MindfulnessEventName',
                    'MindfulnessEventDuration',
                    'MindfulnessEventNotes')

class UserPreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreferences
        fields = ('UserPreferenceID',
                    'UserEmail',
                    'UserPreference',
                    'UserPreferenceDuration',
                    'UserPreferenceNotes')

class StressSurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = StressSurvey
        fields = ('SurveyID',
                    'UserEmail',
                    'SurveyValue')

class StreaksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Streaks
        fields = ('UserID',
                    'UserEmail',
                    'StreakCount',
                    'LastLogin')