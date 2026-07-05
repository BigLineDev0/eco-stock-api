from django.db import models

class Warehouse(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    capacity = models.PositiveIntegerField()
    
    def __str__(self):
        return self.name

class Product(models.Model):
    STATUS_CHOICES = [
        ('available', 'Disponible'),
        ('reserved', 'Réservé'),
        ('expired', 'Périmé'),
    ]
    
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    expiration_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='products')
    
    def __str__(self):
        return self.name
