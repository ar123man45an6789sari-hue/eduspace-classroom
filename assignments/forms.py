from django import forms
from django.utils import timezone
from .models import Assignment, Submission


class AssignmentForm(forms.ModelForm):
    due_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M'],
    )

    class Meta:
        model = Assignment
        fields = ['title', 'description', 'due_date', 'max_marks', 'attachment']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['file', 'note']
        widgets = {
            'note': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Optional note to your teacher...'}),
        }


class GradeForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['marks', 'feedback', 'status']
        widgets = {
            'feedback': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_marks(self):
        marks = self.cleaned_data.get('marks')
        if marks is not None and self.instance.assignment_id and marks > self.instance.assignment.max_marks:
            raise forms.ValidationError(
                f'Marks cannot exceed the assignment maximum of {self.instance.assignment.max_marks}.'
            )
        return marks
