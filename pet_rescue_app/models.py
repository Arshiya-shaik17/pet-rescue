from django.db import models

class PetRequest(models.Model):

    REQUEST_TYPE_CHOICES = [
        ("Lost", "Lost"),
        ("Found", "Found"),
    ]

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Accepted", "Accepted"),
        ("Rejected", "Rejected"),
    ]

    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='pet_requests'
    )

    request_type = models.CharField(max_length=10, choices=REQUEST_TYPE_CHOICES)

    pet_type = models.CharField(max_length=50)  # Dog, Cat, etc
    breed = models.CharField(max_length=100)
    color = models.CharField(max_length=100)

    location = models.CharField(max_length=200)
    contact_info = models.CharField(max_length=100)

    image = models.ImageField(upload_to='pet_requests/', null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pet_type} - {self.request_type}"

class User(models.Model):

    ROLE_CHOICES = [
        ("User", "User"),
        ("Admin", "Admin"),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    phone = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=100)

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="User")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email