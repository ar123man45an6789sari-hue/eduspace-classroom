from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('dashboard/',                           views.dashboard,              name='dashboard'),

    # Classroom CRUD
    path('classrooms/create/',                   views.classroom_create,       name='classroom_create'),
    path('classrooms/join/',                     views.classroom_join,         name='classroom_join'),
    path('classrooms/<int:pk>/',                 views.classroom_detail,       name='classroom_detail'),
    path('classrooms/<int:pk>/edit/',            views.classroom_edit,         name='classroom_edit'),
    path('classrooms/<int:pk>/delete/',          views.classroom_delete,       name='classroom_delete'),
    path('classrooms/<int:pk>/leave/',           views.classroom_leave,        name='classroom_leave'),
    path('classrooms/<int:pk>/members/',         views.classroom_members,      name='classroom_members'),
    path('classrooms/<int:pk>/remove/<int:student_id>/', views.remove_student, name='remove_student'),

    # Posts & Comments
    path('classrooms/<int:classroom_pk>/post/', views.post_create,             name='post_create'),
    path('posts/<int:pk>/delete/',              views.post_delete,             name='post_delete'),
    path('posts/<int:post_pk>/comment/',        views.comment_create,          name='comment_create'),

    # Assignments
    path('classrooms/<int:classroom_pk>/assignments/',        views.assignment_list,   name='assignment_list'),
    path('classrooms/<int:classroom_pk>/assignments/create/', views.assignment_create, name='assignment_create'),
    path('assignments/<int:pk>/',                             views.assignment_detail, name='assignment_detail'),
    path('assignments/<int:pk>/submit/',                      views.assignment_submit, name='assignment_submit'),
    path('assignments/<int:pk>/delete/',                      views.assignment_delete, name='assignment_delete'),
    path('submissions/<int:submission_pk>/grade/',            views.assignment_grade,  name='assignment_grade'),

    # Meetings
    path('classrooms/<int:classroom_pk>/meetings/',        views.meeting_list,   name='meeting_list'),
    path('classrooms/<int:classroom_pk>/meetings/create/', views.meeting_create, name='meeting_create'),
    path('meetings/<int:pk>/delete/',                      views.meeting_delete, name='meeting_delete'),
]
