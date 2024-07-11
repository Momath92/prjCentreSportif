from django.shortcuts import render, redirect, get_object_or_404
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from datetime import date


def accueil(request):
    activite = Activite.objects.all()
    return render(request, 'accueil.html', {'activite': activite})


def sign_up(request):
    errors = {}
    suggestions = []
    message = ""
    user = None
    
    if request.method == 'POST':
        nom = request.POST.get('nom_client', None)
        prenom = request.POST.get('prenom_client', None)
        username = request.POST.get('username', None)
        email = request.POST.get('email', None)
        age = request.POST.get('age', None)
        choix_sport = request.POST.get('choix_sport', None)
        password = request.POST.get('password')

        # Validation du nom
        if not nom or len(nom) < 2:
            errors['nom'] = "Le nom doit contenir au moins 2 caractères"

        # Validation du prénom
        if not prenom or len(prenom) < 2:
            errors['prenom'] = "Le prénom doit contenir au moins 2 caractères"

        # Validation de l'email
        try:
            validate_email(email)
            if User.objects.filter(email=email).exists():
                errors['email'] = "Cet email est déjà utilisé"
        except ValidationError:
            errors['email'] = "L'email n'est pas dans le bon format"

        # Validation de l'âge
        if not age or not age.isdigit() or int(age) < 0:
            errors['age'] = "L'âge doit être un nombre positif"

        # Validation du choix de sport
        if not choix_sport or len(choix_sport) < 2:
            errors['choix_sport'] = "Le choix de sport doit contenir au moins 2 caractères"

        # Validation du mot de passe
        if not password or len(password) < 8:
            errors['password'] = "Le mot de passe doit contenir au moins 8 caractères"

        # Validation du nom d'utilisateur
        if User.objects.filter(username=username).exists():
            errors['username'] = "Ce nom d'utilisateur existe déjà. Voici quelques suggestions :"
            for i in range(10):
                suggestion = f"{username}{i}"
                if not User.objects.filter(username=suggestion).exists():
                    suggestions.append(suggestion)

        if not errors:
            user = User.objects.create_user(username=username, email=email, password=password)
            client = Client(
                nom_client=nom,
                prenom_client=prenom,
                email=email,
                age=int(age),
                choix_sport=choix_sport,
                password=password,
                user=user
            )
            client.save()
            return redirect('accueil')

    data = {
        'errors': errors,
        'suggestions': suggestions,
        'message': message,
        'user': user  
    }
    return render(request, 'register.html', data)
@login_required
def inscription(request, activite_id):
    client = Client.objects.filter(user=request.user).first()
    if not client:
        return redirect('sign_up')  
    return redirect('inscription_activite', activite_id=activite_id)

@login_required
def inscription_activite(request, activite_id):
    activite = get_object_or_404(Activite, id=activite_id)
    message = None  

    if request.method == 'POST':
        client = request.user.client  
        horaire_id = request.POST.get('horaire_id')

        if not horaire_id:
            return render(request, 'inscription_activite.html', {
                'activite': activite,
                'horaires': Horaire.objects.filter(activite=activite),
                'error': 'Veuillez sélectionner un horaire.'
            })

        horaire = get_object_or_404(Horaire, id=horaire_id)
        statut_inscription = 'en cours'

        inscription = Inscription(
            client=client,
            activite=activite,
            horaire=horaire,
            statut_inscription=statut_inscription
        )
        inscription.save()
        message = "Inscription réussie !"  

    context = {
        'activite': activite,
        'horaires': Horaire.objects.filter(activite=activite),
        'message': message  
    }
    return render(request, 'inscription_activite.html', context)

# @login_required
# def confirmation_activite(request, inscription_id):
#     inscription = get_object_or_404(Inscription, id=inscription_id)
#     return render(request, 'confirmation_activite.html', {'inscription': inscription})

def sign_in(request):
    errors = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('accueil')
        else:
            errors['login'] = "Nom d'utilisateur ou mot de passe incorrect"
    
    return render(request, 'login.html', {'errors': errors})

def log_out(request):
    return render(request, 'login.html', {})

def dashboard(request):
    return render(request, 'admin.html', {})








# from django.shortcuts import render, redirect
# # from django.http import HttpResponse
# from .models import Activite, Client
# from django.core.validators import validate_email
# from django.core.exceptions import ValidationError
# from django.contrib.auth.models import User

# def accueil(request):
#     activite = Activite.objects.all()
#     return render(request, 'accueil.html', {'activite': activite})

# def sign_up(request):
#     errors = {}
#     message = ""
#     if request.method == 'POST':
#         nom = request.POST.get('nom_client', None)
#         prenom = request.POST.get('prenom_client', None)
#         email = request.POST.get('email', None)
#         age = request.POST.get('age', None)
#         choix_sport = request.POST.get('choix_sport', None)
#         password = request.POST.get('password')

#         # Validation du nom
#         if not nom or len(nom) < 2:
#             errors['nom'] = "Le nom doit contenir au moins 2 caractères"

#         # Validation du prénom
#         if not prenom or len(prenom) < 2:
#             errors['prenom'] = "Le prénom doit contenir au moins 2 caractères"

#         # Validation de l'email
#         try:
#             validate_email(email)
#             if User.objects.filter(email=email).exists():
#                 errors['email'] = "Cet email est déjà utilisé"
#         except ValidationError:
#             errors['email'] = "L'email n'est pas dans le bon format"
#         # Validation de l'âge
#         if not age or not age.isdigit() or int(age) < 0:
#             errors['age'] = "L'âge doit être un nombre positif"

#         # Validation du choix de sport
#         if not choix_sport or len(choix_sport) < 2:
#             errors['choix_sport'] = "Le choix de sport doit contenir au moins 2 caractères"

#         # Validation du mot de passe
#         if not password or len(password) < 8:
#             errors['password'] = "Le mot de passe doit contenir au moins 8 caractères"
#     else:
#         errors = {}
#         message = ""
#     print("=="*5, "NEW POST: ",nom, prenom, email, age, choix_sport, password, "=="*5)
#     data = {
#             'errors':errors,
#             'message':message
#         }    
#     return render(request, 'register.html', data)
    

# def sign_in(request):
#     return render(request, 'login.html', {})

# def log_out(request):
#     return render(request,'login.html', {})

# def dashboard(request):
#     return render(request, 'admin.html', {})



# def sign_up(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             messages.success(request, 'Votre compte a été créé avec succès.')
#             return redirect('accueil')  # Redirige vers la page d'accueil après inscription
#     else:
#         form = UserCreationForm()
#     return render(request, 'registration/signup.html', {'form': form})

# def sign_in(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             messages.success(request, 'Connexion réussie.')
#             return redirect('accueil')  # Redirige vers la page d'accueil après connexion
#     else:
#         form = AuthenticationForm()
#     return render(request, 'registration/login.html', {'form': form})

# def log_out(request):
#     if request.method == 'POST':
#         logout(request)
#         messages.success(request, 'Déconnexion réussie.')
#         return redirect('accueil')  
#     return render(request, 'login.html')
