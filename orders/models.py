import uuid
from django.db import models

# ! Fixing the migration problem if there is unknown error
# ? https://chat.openai.com/c/a2bedf2d-801d-4814-8298-9dd7fb0973c3
"""
TLDR;
Delete the migrations file, drop the tables, and do this
python manage.py flush
python manage.py makemigrations your_app_name
python manage.py migrate
"""

# Create your models here.
class Order(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set when the object is first created
    updated_at = models.DateTimeField(auto_now=True)      # Automatically set when the object is saved
    
    """
        ! if you want to combine first name & last name
        @property
        def name(self):
            return self.first_name + ' ' + self.last_name
    """
class OrderItem(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    product_title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    quantity = models.IntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set when the object is first created
    updated_at = models.DateTimeField(auto_now=True)    
    
    
    