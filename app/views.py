from rest_framework.views import APIView
from .models import Course
from .serializers import ContactSerializer, CourseSerializer
from .utils import standard_response
from django.conf import settings

class CourseListView(APIView):
    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True, context={'request': request})
        return standard_response(
            data=serializer.data,
            status=True,
            message="Courses retrieved successfully"
        )
    


class ContactCreateView(APIView):
    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            # Save the contact
            contact = serializer.save()

            return standard_response(
                    data=serializer.data,
                    status=True,
                    message="Contact created and sent to Telegram successfully"
                )
        return standard_response(
            data=serializer.errors,
            status=False,
            message="Invalid data"
        )
