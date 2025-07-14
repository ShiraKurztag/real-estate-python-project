from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Seller(models.Model):
    id = models.AutoField(primary_key=True)
    user=models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id}: {self.user}"

class Broker(models.Model):
    id = models.AutoField(primary_key=True)
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    benefits=models.IntegerField()

    def __str__(self):
        return f"{self.id}: {self.user}, benefits: {self.benefits}"

class Apartment(models.Model):
    id = models.AutoField(primary_key=True)
    city=models.CharField(max_length=50)
    neighborhood=models.CharField(max_length=50)
    street=models.CharField(max_length=50)
    seller = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    floor=models.IntegerField()
    rooms=models.IntegerField()
    state=models.CharField(max_length=100)
    describe=models.CharField(max_length=200)
    price=models.IntegerField()
    brokerage = models.BooleanField(default=False)
    status=models.BooleanField(default=False)


    def __str__(self):
        return f"{self.id}: {self.city} price: {self.price}"

class Inquiries(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    apartment = models.ForeignKey(Apartment, on_delete=models.DO_NOTHING)
    date = models.DateField()

    def __str__(self):
        return f"{self.id}: {self.apartment}"


class Image(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    apartment = models.ForeignKey(Apartment, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.id}: {self.apartment} "






