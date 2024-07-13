from django.urls import path
from . import views

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('register/', views.sign_up, name="sign_up"),
    path('login/', views.sign_in, name="sign_in"),
    path('logout/', views.log_out, name="log-out"),
    path('inscription/<int:activite_id>/', views.inscription, name='inscription'),
    path('inscription_activite/<int:activite_id>/', views.inscription_activite, name='inscription_activite'),
    path('moniteur/login/', views.moniteur_login, name='moniteur_login'),
    path('moniteur/', views.moniteur, name='moniteur'),
    
    # path('confirmation_activite/<int:inscription_id>/', views.confirmation_activite, name='confirmation_activite'),
]
