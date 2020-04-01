from django.db import models
from django.contrib.auth.models import User

from django.urls import reverse
from django.utils import timezone
from datetime import date

# Create your models here.
class Dun(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    code_name = models.CharField('DUN Code', max_length=3, null=True)
    name = models.CharField('DUN', max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.code_name} {self.name}"

class Applicant(models.Model):
    dun = models.ForeignKey(Dun, null=True, blank=True, on_delete=models.CASCADE)
    SALUTATION = (
        ('MR', 'Mr'),
        ('MRS', 'Mrs'),
        ('MS', 'Ms'),
    )
    salutation = models.CharField('Title',max_length=10, choices=SALUTATION, null=True)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    dob = models.DateField(default=date.today)
    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    gender = models.CharField(choices=GENDER, null=True, max_length=20)
    nric = models.CharField('NRIC No.', max_length=12, null=True)
    email = models.CharField(max_length=50, null=True)
    phone = models.CharField(max_length=20, null=True)
    alt_phone = models.CharField(max_length=20, null=True, blank=True)
    job_title = models.CharField(max_length=100, null=True)
    salary = models.FloatField(null=True)
    MARITAL = (
        ('Single', 'Single'),
        ('Married', 'Married'),
        ('Divorced', 'Divorced'),
        ('Complicated', 'Complicated'),
    )
    marital_status = models.CharField(choices=MARITAL, null=True, max_length=20)
    address1 = models.CharField('Address line 1', max_length=200, null=True)
    address2 = models.CharField('Address line 2', max_length=200, null=True)
    postal_code = models.CharField('Postcode', max_length=5, null=True)
    city = models.CharField('City', max_length=50, null=True)
    STATE = (
        ('JOHOR', 'Johor'),
        ('KEDAH', 'Kedah'),
        ('KELANTAN', 'Kelantan'),
        ('MELAKA', 'Melaka'),
        ('NEGERI SEMBILAN', 'Negeri Sembilan'),
        ('PAHANG', 'Pahang'),
        ('PULAU PINANG', 'Pulau Pinang'),
        ('PERAK', 'Perak'),
        ('PERLIS', 'Perlis'),
        ('SABAH', 'Sabah'),
        ('SARAWAK', 'Sarawak'),
        ('SELANGOR', 'Selangor'),
        ('TERENGGANU', 'Terengganu'),
        ('W.P. KUALA LUMPUR', 'Kuala Lumpur'),
        ('W.P. LABUAN', 'Labuan'),
        ('W.P. PUTRAJAYA', 'Putrajaya'),
    )
    state = models.CharField(choices=STATE, null=True, max_length=30)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def get_absolute_url(self):
        return reverse('update-application', kwargs={'pk': self.pk})

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class FamilyMember(models.Model):
    RELATION = (
        ('Spouse', 'Spouse'),
        ('Children', 'Children'),
    )
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    relationship = models.CharField(max_length=100, null=True, choices=RELATION)
    family_name = models.CharField(max_length=100, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.family_name

class Product(models.Model):
    name = models.CharField(max_length=100, null=True)
    price = models.FloatField(null=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )
    applicant = models.ForeignKey(Applicant, null=True, on_delete= models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete= models.SET_NULL)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.applicant.first_name} {self.applicant.last_name}"
    
