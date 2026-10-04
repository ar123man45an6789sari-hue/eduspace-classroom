from django.contrib import admin
from .models import Classroom, Enrollment, Announcement, Material


@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'teacher', 'join_code', 'created_at', 'get_student_count']
    search_fields = ['name', 'subject', 'teacher__username', 'join_code']
    list_filter = ['created_at']


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'classroom', 'joined_at']
    list_filter = ['classroom']
    search_fields = ['student__username', 'classroom__name']


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['classroom', 'author', 'title', 'created_at']
    list_filter = ['classroom']


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['title', 'classroom', 'uploaded_by', 'uploaded_at']
    list_filter = ['classroom']
