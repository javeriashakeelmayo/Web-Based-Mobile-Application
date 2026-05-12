from django.db import models
import uuid

class Category(models.Model):
    name = models.CharField(max_length=100)  

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image_url = models.URLField(blank=True) 

    def __str__(self):
        return self.name

class Booking(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    date = models.DateField()
    time_slot = models.TimeField()
    guests = models.IntegerField()
    reference_id = models.CharField(max_length=10, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.reference_id:
            import uuid
            self.reference_id = uuid.uuid4().hex[:8].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.reference_id}"

class Lead(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    whatsapp = models.CharField(max_length=20)
    interest = models.TextField()
    def __str__(self):
        return self.name