from django.urls import path
from .views import ContactCreateView, CourseListView

urlpatterns = [
    path('courses/', CourseListView.as_view(), name='course-list'),
    path('create-contact/', ContactCreateView.as_view(), name='create-contact'),

]