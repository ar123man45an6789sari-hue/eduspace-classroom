from django import forms

from classroom.models import Classroom, Material


class StudyAssistantForm(forms.Form):
    classroom = forms.ModelChoiceField(queryset=Classroom.objects.none(), label='Classroom')
    question = forms.CharField(
        label='Your question',
        max_length=2000,
        widget=forms.Textarea(attrs={'rows': 5, 'placeholder': 'Ask about the lessons or materials in this classroom...'}),
    )


class AssignmentGeneratorForm(forms.Form):
    classroom = forms.ModelChoiceField(queryset=Classroom.objects.none(), label='Classroom')
    topic = forms.CharField(max_length=200, label='Topic', widget=forms.TextInput(attrs={'placeholder': 'e.g. Photosynthesis'}))
    difficulty = forms.ChoiceField(choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')])
    max_marks = forms.IntegerField(min_value=1, max_value=1000, initial=100, label='Maximum marks')


class MaterialSummarizerForm(forms.Form):
    material = forms.ModelChoiceField(queryset=Material.objects.none(), label='Study material')


class QuizGeneratorForm(forms.Form):
    material = forms.ModelChoiceField(queryset=Material.objects.none(), label='Study material')
    number_questions = forms.IntegerField(min_value=1, max_value=20, initial=5, label='Number of questions')
