from django.urls import path
from . import views
urlpatterns = [
    path('login-user/', views.LoginView.as_view()),
    path('logaout-user/', views.logoutView.as_view()),
    path('crear-user/', views.Crearusuarioview.as_view()),
    path('update-password/', views.Userupdateview.as_view()),
    
  
]
