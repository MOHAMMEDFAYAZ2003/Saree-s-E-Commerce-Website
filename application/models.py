from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import pre_save
from django.dispatch import receiver

# Base Product Model
class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return f"{self.name} - ₹{self.price}"

# Cart Model with Generic Foreign Key
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Generic Foreign Key to support multiple product models
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  
    object_id = models.PositiveIntegerField()
    product = GenericForeignKey('content_type', 'object_id')

    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        try:
            return self.quantity * self.product.price
        except AttributeError:
            return 0  # Handles cases where product or price doesn't exist

    def __str__(self):
        return f"{self.quantity} x {self.product} (₹{self.total_price()})"

# Saree Model
class Saree(models.Model):
    product_id = models.AutoField(primary_key=True)  # Added for proper referencing
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="saree_images/")
    color = models.CharField(max_length=255, default="Unknown")
    saree_model = models.CharField(max_length=255)
    about_item = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.title} - ₹{self.price}"

# Featured Saree Model
class FeaturedSaree(models.Model):
    product_id = models.AutoField(primary_key=True)  # Added for proper referencing
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="featured_sarees/")
    color = models.CharField(max_length=255, default="Unknown")
    saree_model = models.CharField(max_length=255, default="Generic Model")
    about_item = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.title} - ₹{self.price}"

# Automatically set initial product_id for new entries
@receiver(pre_save, sender=Saree)
def set_saree_product_id(sender, instance, **kwargs):
    if instance.product_id is None:  # Only set if it's a new object
        last_id = Saree.objects.order_by('-product_id').first()
        instance.product_id = last_id.product_id + 1 if last_id else 1000

@receiver(pre_save, sender=FeaturedSaree)
def set_featured_saree_product_id(sender, instance, **kwargs):
    if instance.product_id is None:
        last_id = FeaturedSaree.objects.order_by('-product_id').first()
        instance.product_id = last_id.product_id + 1 if last_id else 2000

# Silk Saree Model
class SilkSaree(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='silk_sarees/')

    def __str__(self):
        return self.title

# Cotton Saree Model
class CottonSaree(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='cotton_sarees/')

    def __str__(self):
        return self.title

# Trending Sarees Model
class TrendingSarees(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='trending_sarees/')

    def __str__(self):
        return self.title
