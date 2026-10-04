from django.contrib import admin
from .models import Classroom, Enrollment, Post, Comment, Assignment, Submission, Meeting, Attachment


@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display  = ['name', 'teacher', 'code', 'get_student_count', 'is_active', 'created_at']
    list_filter   = ['is_active', 'created_at']
    search_fields = ['name', 'code', 'teacher__username']
    readonly_fields = ['code', 'created_at']


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display  = ['student', 'classroom', 'joined_at']
    list_filter   = ['classroom']
    search_fields = ['student__username', 'classroom__name']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display  = ['author', 'classroom', 'post_type', 'created_at']
    list_filter   = ['post_type', 'created_at']


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display  = ['title', 'classroom', 'total_marks', 'due_date', 'created_at']
    list_filter   = ['classroom']


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display  = ['student', 'assignment', 'status', 'marks', 'submitted_at']
    list_filter   = ['status']


@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display  = ['title', 'classroom', 'scheduled_at', 'status']
    list_filter   = ['status']


admin.site.register(Comment)
admin.site.register(Attachment)
