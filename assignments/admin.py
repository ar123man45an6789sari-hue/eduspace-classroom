from django.contrib import admin
from .models import Assignment, Submission


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'classroom', 'due_date', 'max_marks', 'submission_count']
    list_filter = ['classroom', 'due_date']
    search_fields = ['title', 'classroom__name']


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['student', 'assignment', 'submitted_at', 'marks', 'status']
    list_filter = ['status', 'assignment__classroom']
    search_fields = ['student__username', 'assignment__title']
