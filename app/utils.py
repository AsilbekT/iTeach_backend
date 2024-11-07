from rest_framework.response import Response
from django.core.exceptions import ValidationError
import re

def standard_response(data=None, status=True, message=""):
    return Response({
        "status": status,
        "message": message,
        "data": data
    })



def validate_video_file_size(file):
    max_size_mb = 100
    if file.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f"File size should not exceed {max_size_mb} MB.")


def validate_http(name):
    if "http://" in name:
        name = name.replace("http://", "https://")
    return name
