from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("student_id", "student_name", "college", "batch", "semester")
    search_fields = ("student_id", "student_name")
    list_filter = ("college", "batch", "semester")
