from django.conf import settings
from django.db import models

from assignments.models import Assignment, Submission
from classroom.models import Classroom, Material


class AIInteraction(models.Model):
    STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ai_interactions')
    classroom = models.ForeignKey(Classroom, on_delete=models.SET_NULL, null=True, blank=True, related_name='ai_interactions')
    material = models.ForeignKey(Material, on_delete=models.SET_NULL, null=True, blank=True, related_name='ai_interactions')
    assignment = models.ForeignKey(Assignment, on_delete=models.SET_NULL, null=True, blank=True, related_name='ai_interactions')
    submission = models.ForeignKey(Submission, on_delete=models.SET_NULL, null=True, blank=True, related_name='ai_interactions')
    feature = models.CharField(max_length=40)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    model_name = models.CharField(max_length=100, blank=True, default='')
    input_metadata = models.JSONField(default=dict, blank=True)
    output_text = models.TextField(blank=True, default='')
    error_message = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.feature} by {self.user.username} ({self.status})'
