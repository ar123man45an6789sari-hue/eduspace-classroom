from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from classroom.models import Classroom


class Assignment(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateTimeField()
    attachment = models.FileField(upload_to='assignments/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    max_marks = models.PositiveIntegerField(default=100)

    class Meta:
        ordering = ['due_date']

    def __str__(self):
        return f"{self.title} ({self.classroom.name})"

    def is_overdue(self):
        return timezone.now() > self.due_date

    def submission_count(self):
        return self.submissions.count()


class Submission(models.Model):
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('graded', 'Graded'),
        ('late', 'Late Submission'),
    ]
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    file = models.FileField(upload_to='submissions/')
    note = models.TextField(blank=True, default='', help_text='Optional note to the teacher')
    submitted_at = models.DateTimeField(auto_now_add=True)
    marks = models.PositiveIntegerField(null=True, blank=True)
    feedback = models.TextField(blank=True, default='')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')

    class Meta:
        unique_together = ['assignment', 'student']
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.student.username} - {self.assignment.title}"

    def filename(self):
        import os
        return os.path.basename(self.file.name)
