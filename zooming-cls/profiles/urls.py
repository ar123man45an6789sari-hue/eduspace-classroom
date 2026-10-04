from django.urls import path
from . import views

urlpatterns = [
    path('register/',      views.register,      name='register'),
    path('profile/',       views.profile_view,  name='profile'),
    path('profile/edit/',  views.profile_edit,  name='profile_edit'),
    path('profile/<str:username>/', views.profile_view, name='profile_user'),
]
