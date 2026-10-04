import random
import string
from django.db import models
from django.contrib.auth.models import User


def generate_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))


class Classroom(models.Model):
    name        = models.CharField(max_length=200)
    section     = models.CharField(max_length=100, blank=True)
    subject     = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    code        = models.CharField(max_length=10, unique=True, default=generate_code, editable=False)
    teacher     = models.ForeignKey(User, on_delete=models.CASCADE, related_name='taught_classrooms')
    students    = models.ManyToManyField(User, through='Enrollment', related_name='enrolled_classrooms', blank=True)
    banner_color = models.CharField(max_length=20, default='indigo', blank=True)
    is_active   = models.BooleanField(default=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.teacher.username})"

    def get_student_count(self):
        return self.students.count()


class Enrollment(models.Model):
    student   = models.ForeignKey(User, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'classroom')
        ordering = ['joined_at']

    def __str__(self):
        return f"{self.student.username} in {self.classroom.name}"


class Post(models.Model):
    POST_TYPES = [
        ('announcement', 'Announcement'),
        ('material', 'Material'),
        ('question', 'Question'),
    ]

    classroom  = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='posts')
    author     = models.ForeignKey(User, on_delete=models.CASCADE)
    post_type  = models.CharField(max_length=20, choices=POST_TYPES, default='announcement')
    content    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.post_type}] {self.classroom.name} — {self.author.username}"


class Attachment(models.Model):
    post        = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='attachments',
                                    null=True, blank=True)
    assignment  = models.ForeignKey('Assignment', on_delete=models.CASCADE,
                                    related_name='attachments', null=True, blank=True)
    file        = models.FileField(upload_to='attachments/')
    name        = models.CharField(max_length=255)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def is_image(self):
        return self.name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp'))

    def is_pdf(self):
        return self.name.lower().endswith('.pdf')


class Comment(models.Model):
    post       = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author     = models.ForeignKey(User, on_delete=models.CASCADE)
    content    = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.author.username}: {self.content[:40]}"


class Assignment(models.Model):
    classroom   = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='assignments')
    title       = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    due_date    = models.DateTimeField(null=True, blank=True)
    total_marks = models.PositiveIntegerField(default=100)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} — {self.classroom.name}"

    def is_overdue(self):
        from django.utils import timezone
        if self.due_date:
            return timezone.now() > self.due_date
        return False

    def submission_for(self, user):
        return self.submissions.filter(student=user).first()


class Submission(models.Model):
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('late', 'Late'),
        ('graded', 'Graded'),
        ('missing', 'Missing'),
    ]

    assignment   = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student      = models.ForeignKey(User, on_delete=models.CASCADE)
    file         = models.FileField(upload_to='submissions/', null=True, blank=True)
    text_answer  = models.TextField(blank=True)
    status       = models.CharField(max_length=15, choices=STATUS_CHOICES, default='submitted')
    marks        = models.PositiveIntegerField(null=True, blank=True)
    feedback     = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    graded_at    = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('assignment', 'student')
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.student.username} → {self.assignment.title}"


class Meeting(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('live', 'Live'),
        ('ended', 'Ended'),
    ]

    classroom    = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='meetings')
    title        = models.CharField(max_length=255)
    description  = models.TextField(blank=True)
    scheduled_at = models.DateTimeField()
    duration     = models.PositiveIntegerField(default=60, help_text='Minutes')
    meet_link    = models.URLField(blank=True, help_text='Zoom / Google Meet link')
    password     = models.CharField(max_length=30, blank=True)
    status       = models.CharField(max_length=15, choices=STATUS_CHOICES, default='scheduled')
    created_by   = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-scheduled_at']

    def __str__(self):
        return f"{self.title} ({self.classroom.name})"
