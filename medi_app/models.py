from django.db import models

STATUS_CHOICES = [
    ("Pending", "Pending"),
    ("Approved", "Approved"),
    ("Shipped", "Shipped"),
    ("Returned", "Returned"),
    ("Appeal", "Appeal"),
]

class ProductImage(models.Model):
    pid = models.BigIntegerField(unique=True)  # Product ID from smart contract
    owner = models.CharField(max_length=42)  # Owner's public address
    image = models.ImageField(upload_to="product_images/")

class RentalRequest(models.Model):
    pid = models.BigIntegerField()
    owner = models.CharField(max_length=42)
    renter = models.CharField(max_length=42)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

class SubRentalRequest(models.Model):
    pid = models.BigIntegerField()
    owner = models.CharField(max_length=42)
    renter = models.CharField(max_length=42)  # Main renter
    sub_renter = models.CharField(max_length=42)  # Sub-renter
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)
