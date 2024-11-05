from django.db import models

# Create your models here.
class Formateur(models.Model):
    GENDER = (
        ('Monsieur', 'Mr'),
        ('Madam', 'Mm'),
    )
    names = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    genr = models.CharField(max_length=10, null=True, choices=GENDER)
    e_mail = models.CharField(max_length=150)
    
    # Database de student 
class Student(models.Model):
    GENRE = (
        ('Male', 'M'),
        ('Femme', 'F'),
    )
    nom = models.CharField(max_length=150)
    prenom = models.CharField(max_length=150)
    naissance = models.DateField( auto_now=False, auto_now_add=False)
    genre = models.CharField(max_length=6, null=True, choices=GENRE)
    email = models.CharField(max_length=150)
    formateur = models.ForeignKey(Formateur, on_delete=models.CASCADE)
       
# Database de formations de student

class Formation(models.Model):
    TYPE = (
        ('Elevage', 'Elevage'),
        ('Agricole', 'Agricole'),
        ('Transformation Produit', 'T-Produit'),
        ('Couper coutume', 'C-Coutume'),
    )
    
    DURE = (
        ('1 Mois', '1'),
        ('2 Mois', '2'),
        ('3 Mois', '3'),
    )
    
    PRIX = (
        ('50000', '1 mois'),
        ('100000', '2 mois'),
        ('150000', '3 mois'),
    )
    
    
    type = models.CharField(max_length=24, null=True, choices=TYPE)
    dure = models.CharField(max_length=25)
    prix = models.FloatField(default=0.0)
    # formateur = models.ForeignKey(Formateur, on_delete=models.CASCADE)
    def __str__(self):
        return self.type
    



class Inscrie(models.Model):
    dates = models.DateField(auto_now=False, auto_now_add=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    formation = models.ForeignKey(Formation, on_delete=models.CASCADE)
    def __str__(self):
        return self.dates
    