from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    full_name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    company = models.CharField(max_length=255, blank=True, null=True)
    role = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return self.username


class ProductManagementEnrollment(models.Model):
    full_name = models.CharField(max_length=255)
    email_address = models.EmailField()
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.email_address})"

BUDGET_RANGE_CHOICES = [
    ("less_than_1000", "Less than $1,000"),
    ("1000_5000", "$1,000 - $5,000"),
    ("5000_10000", "$5,000 - $10,000"),
    ("10000_25000", "$10,000 - $25,000"),
    ("25000_50000", "$25,000 - $50,000"),
    ("50000_100000", "$50,000 - $100,000"),
    ("more_than_100000", "More than $100,000"),
]

SERVICE_CHOICES = [
    "Product Design",
    "Web/Mobile App Development",
    "Product Strategy",
    "MVP Development",
    "Other"
]

class ProjectBuilding(models.Model):
    full_name = models.CharField(max_length=255)
    email_address = models.EmailField()
    company = models.CharField(max_length=255, blank=True, null=True)
    budget_range = models.CharField(max_length=50, choices=BUDGET_RANGE_CHOICES, blank=True, null=True)
    service = models.CharField(max_length=50, choices=SERVICE_CHOICES, blank=True, null=True)
    project_description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.email_address})"
