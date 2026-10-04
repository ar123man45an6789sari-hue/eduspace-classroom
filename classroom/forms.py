from django import forms
from .models import Classroom, Announcement, Material

COLOR_CHOICES = [
    ('#4f46e5', 'Indigo'),
    ('#0ea5e9', 'Sky Blue'),
    ('#10b981', 'Emerald'),
    ('#f59e0b', 'Amber'),
    ('#ef4444', 'Red'),
    ('#8b5cf6', 'Purple'),
    ('#ec4899', 'Pink'),
    ('#14b8a6', 'Teal'),
]


class ClassroomForm(forms.ModelForm):
    cover_color = forms.ChoiceField(choices=COLOR_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = Classroom
        fields = ['name', 'subject', 'description', 'cover_color']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Share something with your class...'}),
        }


class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['title', 'description', 'file']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2}),
        }


class JoinClassroomForm(forms.Form):
    join_code = forms.CharField(
        max_length=10,
        label='Classroom Code',
        widget=forms.TextInput(attrs={'placeholder': 'Enter class code (e.g. AB12CD34)'})
    )
