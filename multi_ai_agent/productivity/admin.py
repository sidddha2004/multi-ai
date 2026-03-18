from django.contrib import admin

# Register your models here.
from .models import CalendarEvent,Reminder,Task
admin.site.register(Task)
admin.site.register(CalendarEvent)
admin.site.register(Reminder)

