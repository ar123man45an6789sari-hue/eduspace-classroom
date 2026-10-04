from django.urls import path
from . import views

urlpatterns = [
    # Teacher URLs
    path('classroom/<int:classroom_pk>/create/', views.create_assignment, name='create_assignment'),
    path('<int:pk>/edit/', views.edit_assignment, name='edit_assignment'),
    path('<int:pk>/delete/', views.delete_assignment, name='delete_assignment'),
    path('<int:pk>/submissions/', views.view_submissions, name='view_submissions'),
    path('submission/<int:pk>/grade/', views.grade_submission, name='grade_submission'),
    # Student URLs
    path('<int:pk>/', views.assignment_detail, name='assignment_detail'),
    path('<int:pk>/submit/', views.submit_assignment, name='submit_assignment'),
    path('my-submissions/', views.my_submissions, name='my_submissions'),
]
