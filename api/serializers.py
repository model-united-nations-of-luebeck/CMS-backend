from rest_framework import serializers
from api.models import Conference

# Serializers convert to JSON and validate data passed

class ConferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conference
        fields = ['id', 'year', 'startdate', 'enddate', 'annual_session', 'theme', 'pre_registration_deadline', 'final_registration_deadline', 'position_paper_deadline', 'chairhuman', 'vice_chairhuman', 'treasurer', 'vice_treasurer']
