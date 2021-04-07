from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=20,null=True)
    phone = models.CharField(max_length=20,null=True)
    emali = models.CharField(max_length=20,null=True)
    profile_pic = models.ImageField(null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.name

class Teg(models.Model):
    name = models.CharField(max_length=20,null=True)

    def __str__(self):
        return self.name

class Product(models.Model):

    CATEGORY = (
        ('Indoor', 'Indoor'),
        ('Outdoor','Outdoor')
    )

    name = models.CharField(max_length=20,null=True)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=20,null=True,choices=CATEGORY)
    discription = models.CharField(max_length=20,null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True)
    tag = models.ManyToManyField(Teg)

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS = (
        ('Pending','Pending'),
        ('Out For Delivery','Out For Delevery'),
        ('Delivered','Delivered'),

    )
    customer = models.ForeignKey(Customer,null=True,on_delete=models.SET_NULL)
    product = models.ForeignKey(Product,null=True,on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True,null=True)
    status = models.CharField(max_length=20,null=True,choices=STATUS)
    note = models.CharField(max_length=20,null=True, blank=True)

    def __str__(self):
        return self.product.name
