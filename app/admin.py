from django.contrib import admin
from .models import Course, Contact, HelpGroup

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'duration', 'start_date', 'end_date')
    search_fields = ('title',)
    fields = ('title', 'description', 'duration', 'start_date', 'end_date', 'trailer')


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'help_group')
    search_fields = ('name', 'phone_number')

@admin.register(HelpGroup)
class HelpGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'chat_id')
    search_fields = ('name',)