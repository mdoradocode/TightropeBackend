from rest_framework import serializers
from eventApp.models import Events, MindfulnessEvents

class EventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = ('EventID',
                    'UserEmail',
                    'EventName',
                    'StartDate',
                    'EndDate',
                    'Location',
                    'Leisure',
                    'StressLevel',
                    'Notes')

class MindfulnessEventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MindfulnessEvents
        fields = ('MindfulnessEventID',
                    'MindfulnessEventName',
                    'MindfulnessEventDuration',
                    'MindfulnessEventNotes')
