from django.urls import path
from .views import accueil, sign_up, sign_in, log_out, inscription, moniteur_detail

urlpatterns = [
    path('', accueil, name='accueil'),
    path('register/', sign_up, name="sign_up"),
    path('login/', sign_in, name="sign_in"),
    path('logout/', log_out, name="log-out"),
    path('inscription/<int:activite_id>/', inscription, name='inscription'),
    path('moniteur/dashboard/', moniteur_detail, name='moniteur_dashboard'),
]
