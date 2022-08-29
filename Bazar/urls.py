from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.LoginView.as_view(), name='index'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('eventos/', views.IndexView.as_view(), name='eventos'),
    path('eventos/<int:id>/', views.ItensView.as_view(), name='evento'),
    path('eventos/<int:id>/cadastrar_item/', views.CadastrarItemView.as_view(), name='cadastrar_item'),
    path('eventos/<int:id>/item/<int:item_id>/', views.ItemView.as_view(), name='item'),
    path('eventos/<int:id>/item/<int:item_id>/reservar/', views.ReservarItemView.as_view(), name='reservar'),
]
