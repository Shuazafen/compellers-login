from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('auth/register/', views.register, name='register'),
    path('auth/login/', views.login, name='login'),
    path('auth/logout/', views.logout, name='logout'),
    path('auth/profile/', views.profile, name='profile'),
    path('enroll/product-management/', views.enroll_product_management, name='enroll_product_management'),
    path('project-building/', views.submit_project_building, name='submit_project_building'),
]
