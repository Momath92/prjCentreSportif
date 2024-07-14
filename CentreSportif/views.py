from django.shortcuts import render, redirect, get_object_or_404
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Moniteur, Activite, Inscription, Horaire, Client

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

        if not nom or len(nom) < 2:
            errors['nom'] = "Le nom doit contenir au moins 2 caractères"
        if not prenom or len(prenom) < 2:
            errors['prenom'] = "Le prénom doit contenir au moins 2 caractères"
        try:
            validate_email(email)
            if User.objects.filter(email=email).exists():
                errors['email'] = "Cet email est déjà utilisé"
        except ValidationError:
            errors['email'] = "L'email n'est pas dans le bon format"
        if not age or not age.isdigit() or int(age) < 0:
            errors['age'] = "L'âge doit être un nombre positif"
        if not choix_sport or len(choix_sport) < 2:
            errors['choix_sport'] = "Le choix de sport doit contenir au moins 2 caractères"
        if not password or len(password) < 8:
            errors['password'] = "Le mot de passe doit contenir au moins 8 caractères"
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

def inscription(request, activite_id):
    activite = get_object_or_404(Activite, id=activite_id)
    horaires = Horaire.objects.filter(activite=activite)

    if request.method == 'POST':
        client_id = request.POST.get('client_id')
        horaire_id = request.POST.get('horaire_id')
        client = get_object_or_404(Client, id=client_id)
        horaire = get_object_or_404(Horaire, id=horaire_id)
        Inscription.objects.create(
            client=client,
            activite=activite,
            horaire=horaire,
            statut_inscription='en cours'
        )
        messages.success(request, 'Inscription réussie')
        return redirect('accueil')

    return render(request, 'inscription.html', {'activite': activite, 'horaires': horaires})

@login_required
def moniteur_detail(request):
    moniteur = get_object_or_404(Moniteur, email=request.user.email)
    cours = Activite.objects.filter(moniteur=moniteur)
    inscriptions = Inscription.objects.filter(activite__in=cours)
    horaires = Horaire.objects.filter(activite__in=cours)

    context = {
        'moniteur': moniteur,
        'cours': cours,
        'inscriptions': inscriptions,
        'horaires': horaires
    }
    return render(request, 'moniteur_detail.html', context)


@login_required
def moniteur_detail(request):
    moniteur = get_object_or_404(Moniteur, user=request.user)
    cours = Activite.objects.filter(moniteur=moniteur)
    inscriptions = Inscription.objects.filter(activite__in=cours)
    horaires = Horaire.objects.filter(activite__in=cours)

    context = {
        'moniteur': moniteur,
        'cours': cours,
        'inscriptions': inscriptions,
        'horaires': horaires
    }
    return render(request, 'moniteur_detail.html', context)
