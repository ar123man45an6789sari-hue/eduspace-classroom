from django.urls import path

from . import views

app_name = 'ai_assistant'

urlpatterns = [
    path('study-assistant/', views.study_assistant, name='study_assistant'),
    path('assignment-generator/', views.assignment_generator, name='assignment_generator'),
    path('summarizer/', views.material_summarizer, name='material_summarizer'),
    path('quiz-generator/', views.quiz_generator, name='quiz_generator'),
    path('evaluate/submission/<int:pk>/', views.evaluate_submission, name='evaluate_submission'),
]
