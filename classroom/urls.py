from django.urls import path
from . import views

urlpatterns = [
    # Teacher URLs
    path('teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('create/', views.create_classroom, name='create_classroom'),
    path('<int:pk>/edit/', views.edit_classroom, name='edit_classroom'),
    path('<int:pk>/delete/', views.delete_classroom, name='delete_classroom'),
    path('<int:pk>/teacher/', views.classroom_detail_teacher, name='classroom_detail_teacher'),
    path('<int:pk>/announce/', views.post_announcement, name='post_announcement'),
    path('<int:pk>/announce/<int:ann_pk>/delete/', views.delete_announcement, name='delete_announcement'),
    path('<int:pk>/material/upload/', views.upload_material, name='upload_material'),
    path('<int:pk>/material/<int:mat_pk>/delete/', views.delete_material, name='delete_material'),
    path('<int:pk>/student/<int:student_pk>/remove/', views.remove_student, name='remove_student'),
    # Student URLs
    path('student/', views.student_dashboard, name='student_dashboard'),
    path('join/', views.join_classroom, name='join_classroom'),
    path('<int:pk>/student/', views.classroom_detail_student, name='classroom_detail_student'),
    path('<int:pk>/leave/', views.leave_classroom, name='leave_classroom'),
]
