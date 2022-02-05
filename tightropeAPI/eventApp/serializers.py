from rest_framework import serializers
from eventApp.models import Events

class EventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = ('EventID',
                    'UserID',
                    'EventName',
                    'StartDate',
                    'EndDate',
                    'Description',
                    'Lesiure')
    