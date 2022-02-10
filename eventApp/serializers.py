from rest_framework import serializers
from eventApp.models import Events

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
    