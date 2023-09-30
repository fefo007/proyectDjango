from django.db import models
from django.contrib.auth.models import User

class Messages(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    addressee = models.EmailField(max_length=50,blank=False)
    subject = models.CharField(max_length=100,blank=False)
    message = models.CharField(max_length=800,blank=False)
    def __str__(self):
        return f'{self.client}'

class Order(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    travel = models.CharField(max_length=25,blank=False)
    wayToPay = models.CharField(max_length=25,blank=False)
    price = models.IntegerField(blank=False)
    departure = models.DateField(blank=False)
    arrival = models.DateField(blank=False)

    def __str__(self):
        return f'{self.client} - {self.travel} - ${self.price}'

class Travel(models.Model):
    name = models.CharField(max_length=25,blank=False)
    country = models.CharField(max_length=25,blank=False)
    cities = models.CharField(max_length=250,blank=False)
    image = models.ImageField(upload_to='travels',blank=False)
    screen1 = models.ImageField(upload_to='travels',blank=False)
    screen2 = models.ImageField(upload_to='travels',blank=False)
    screen3 = models.ImageField(upload_to='travels',blank=False)
    price = models.IntegerField(blank=False)
    duration = models.CharField(max_length=25,blank=False)
    description = models.CharField(max_length=500,blank=False)

    def __str__(self):
        return f'{self.name} - ${self.price}'

class Avatar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='avatares',blank=True,null=True)

    def __str__(self):
        return f'{self.user}'

class Tours(models.Model):
    name = models.CharField(max_length=50,blank=False)
    image = models.ImageField(upload_to='tours',blank=False)
    price = models.IntegerField(blank=True,null=True)
    text = models.CharField(max_length=800,blank=False)
    def __str__(self):
        return f'{self.name}'
