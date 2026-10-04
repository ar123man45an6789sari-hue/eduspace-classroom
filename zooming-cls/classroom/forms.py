from django import forms
from .models import Classroom, Post, Comment, Assignment, Submission, Meeting, Attachment


class ClassroomForm(forms.ModelForm):
    class Meta:
        model  = Classroom
        fields = ['name', 'section', 'subject', 'description', 'banner_color']
        widgets = {
            'name':         forms.TextInput(attrs={'placeholder': 'e.g. Mathematics Grade 10'}),
            'section':      forms.TextInput(attrs={'placeholder': 'e.g. Morning Section A'}),
            'subject':      forms.TextInput(attrs={'placeholder': 'e.g. Mathematics'}),
            'description':  forms.Textarea(attrs={'rows': 3, 'placeholder': 'Optional description...'}),
            'banner_color': forms.Select(choices=[
                ('indigo', 'Indigo'),
                ('blue',   'Blue'),
                ('green',  'Green'),
                ('purple', 'Purple'),
                ('red',    'Red'),
                ('orange', 'Orange'),
                ('teal',   'Teal'),
            ]),
        }


class JoinClassroomForm(forms.Form):
    code = forms.CharField(
        max_length=10,
        min_length=5,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter class code (e.g. AB12XYZ)',
            'class': 'font-mono uppercase tracking-widest',
            'style': 'text-transform: uppercase;',
        })
    )

    def clean_code(self):
        return self.cleaned_data['code'].strip().upper()


class PostForm(forms.ModelForm):
    class Meta:
        model  = Post
        fields = ['post_type', 'content']
        widgets = {
            'content':   forms.Textarea(attrs={'rows': 3, 'placeholder': 'Share with your class...'}),
            'post_type': forms.Select(),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model  = Comment
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={'placeholder': 'Add a class comment...'}),
        }


class AssignmentForm(forms.ModelForm):
    due_date = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeLocalInput(attrs={'type': 'datetime-local'}),
    )

    class Meta:
        model  = Assignment
        fields = ['title', 'description', 'due_date', 'total_marks']
        widgets = {
            'title':       forms.TextInput(attrs={'placeholder': 'Assignment title'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class SubmissionForm(forms.ModelForm):
    class Meta:
        model  = Submission
        fields = ['text_answer', 'file']
        widgets = {
            'text_answer': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'Type your answer here... (optional if attaching a file)'
            }),
        }


class GradeForm(forms.ModelForm):
    class Meta:
        model  = Submission
        fields = ['marks', 'feedback']
        widgets = {
            'feedback': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Leave feedback for the student...'}),
        }


class MeetingForm(forms.ModelForm):
    scheduled_at = forms.DateTimeField(
        widget=forms.DateTimeLocalInput(attrs={'type': 'datetime-local'})
    )

    class Meta:
        model  = Meeting
        fields = ['title', 'description', 'scheduled_at', 'duration', 'meet_link', 'password']
        widgets = {
            'title':       forms.TextInput(attrs={'placeholder': 'e.g. Week 3 Live Session'}),
            'description': forms.Textarea(attrs={'rows': 2}),
            'meet_link':   forms.URLInput(attrs={'placeholder': 'https://zoom.us/j/...'}),
            'password':    forms.TextInput(attrs={'placeholder': 'Optional meeting password'}),
        }


class AttachmentForm(forms.ModelForm):
    class Meta:
        model  = Attachment
        fields = ['file']
