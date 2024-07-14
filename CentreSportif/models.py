from django.db import models
from django.contrib.auth.models import User
from datetime import date

class Moniteur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='moniteur', null=True, blank=True)
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.prenom} {self.nom}"

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nom_client = models.CharField(max_length=255)
    prenom_client = models.CharField(max_length=255)
    username = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=False, blank=True)
    age = models.IntegerField(null=True, blank=True)
    choix_sport = models.CharField(max_length=255, null=True, blank=True)
    role = models.CharField(max_length=255, null=True, blank=True)
    password = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return f"{self.prenom_client} {self.nom_client}"

class Activite(models.Model):
    nom_activite = models.CharField(max_length=255)
    prix = models.FloatField(null=True, blank=True)
    categories = models.CharField(max_length=255, null=True, blank=True)
    image = models.CharField(max_length=2800)
    moniteur = models.ForeignKey(Moniteur, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nom_activite

class Inscription(models.Model):
    STATUT_CHOICES = [
        ('en cours', 'En cours'),
        ('annulée', 'Annulée'),
        ('approuvée', 'Approuvée'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    activite = models.ForeignKey(Activite, on_delete=models.CASCADE)
    date_inscription = models.DateField(default=date.today)
    statut_inscription = models.CharField(max_length=10, choices=STATUT_CHOICES)
    horaire = models.ForeignKey('Horaire', on_delete=models.CASCADE)

    def __str__(self):
        return f"Inscription {self.id} - {self.client} - {self.activite}"

class Paiement(models.Model):
    inscription = models.ForeignKey(Inscription, on_delete=models.CASCADE)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date_paiement = models.DateField()
    mode_paiement = models.CharField(max_length=255)

    def __str__(self):
        return f"Paiement {self.id} - {self.montant} - {self.date_paiement}"

class Horaire(models.Model):
    activite = models.ForeignKey(Activite, on_delete=models.CASCADE)
    jour = models.CharField(max_length=10)
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()
    moniteur = models.ForeignKey(Moniteur, on_delete=models.CASCADE)

    def __str__(self):
        return f"Horaire {self.id} - {self.activite} - {self.jour} {self.heure_debut}-{self.heure_fin}"
