from rest_framework import serializers

from app.utils import validate_http
from .models import Contact, Course

class CourseSerializer(serializers.ModelSerializer):
    trailer = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'duration', 'start_date', 'end_date', 'trailer']

    def get_trailer(self, obj):
        request = self.context.get('request')
        if obj.trailer and request:
            return validate_http(request.build_absolute_uri(obj.trailer.url))
        return None



class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['name', 'phone_number', 'details']
