from django.db import models
from django.contrib.auth.models import User

STATUS_CHOICES = [
    ("Pending", "Pending"),
    ("Approved", "Approved"),
    ("Shipped", "Shipped"),
    ("Returned", "Returned"),
    ("Appeal", "Appeal"),
]

class ProductImage(models.Model):
    pid = models.BigIntegerField(unique=True)  # Product ID from smart contract
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_product_images')  # Owner's public address
    image = models.ImageField(upload_to="product_images/")

class RentalRequest(models.Model):
    pid = models.BigIntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_rentals')
    renter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rented_items')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

class SubRentalRequest(models.Model):
    pid = models.BigIntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_subrentals')
    renter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rented_subrentals') # Main renter
    sub_renter= models.ForeignKey(User, on_delete=models.CASCADE, related_name='sub_rented_items')   # Sub-renter
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

