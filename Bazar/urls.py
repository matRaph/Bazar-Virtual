from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.LoginView.as_view(), name='index'),
    path('eventos/', views.IndexView.as_view(), name='eventos'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
]
