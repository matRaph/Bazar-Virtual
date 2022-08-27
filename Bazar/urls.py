from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.LoginView.as_view(), name='index'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('eventos/', views.IndexView.as_view(), name='eventos'),
    path('eventos/<int:id>/', views.EventoView.as_view(), name='evento'),
]
