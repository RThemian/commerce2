from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    WATCHES = 'Watches'
    NATURE_PHOTOGRAPHY = 'Nature Photography'
    CLOTHES = 'Clothes'
    
    DEFAULT_CATEGORIES = [
        (WATCHES, 'Watches'),
        (NATURE_PHOTOGRAPHY, 'Nature Photography'),
        (CLOTHES, 'Clothes'),
    ]
    name = models.CharField(max_length=255, choices=DEFAULT_CATEGORIES, default=NATURE_PHOTOGRAPHY)
    # give default category: watches, nature_photos, clothes 
    

    # give categories: watches, phones, laptops, shoes, clothes, etc.

    class Meta:
        ordering = ('name',) # ordering by name
        verbose_name_plural = 'Categories' # plural name
    
    def __str__(self):
        return self.name
    
class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True) # blank=True, null=True 
    price = models.FloatField( blank=True, null=True)
    image = models.ImageField(upload_to='items_images', blank=True, null=True)
    is_sold = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.name
    
class Photo(models.Model):
   url = models.CharField(max_length=200)
   product = models.ForeignKey(Product, on_delete=models.CASCADE)

   def __str__(self):
      return f"Photo for product_id: {self.product.id} @{self.url}"