from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    # Authentication endpoints
    path('auth/login/', views.LoginView.as_view(), name='login'),
    path('auth/logout/', views.user_logout, name='logout'),
    path('auth/profile/', views.ProfileView.as_view(), name='profile'),

    # Task endpoints
    path('tasks/sample/', views.run_sample_task, name='run_sample_task'),
    path('tasks/email/', views.send_email, name='send_email'),
    path('tasks/<str:task_id>/status/', views.task_status, name='task_status'),
]