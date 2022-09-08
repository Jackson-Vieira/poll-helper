from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('perfil/', views.perfil, name='perfil'),
    path('topics/', views.topics, name='topics')
]
