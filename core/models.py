from django.db import models
from django.db.models.signals import pre_save
from django.core.validators import MaxValueValidator, MinValueValidator

from eMall.utils import unique_slug_generator


class Store(models.Model):

    name = models.CharField(max_length=250, unique=True)
    image = models.ImageField(upload_to="stores-images", null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Category(models.Model):

    name = models.CharField(max_length=250, unique=True)
    image = models.ImageField(
        upload_to="categoies-images", null=True, blank=True)
    store = models.ForeignKey(to="Store", on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Product(models.Model):

    Gender_Choices = (
        ('male', 'male'),
        ('female', 'female'),
        ('kid', 'kid'),
    )

    name = models.CharField(max_length=250, unique=True)
    category = models.ForeignKey(to='Category', on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='Products-images', null=True, blank=True)
    gender = models.CharField(
        max_length=30, choices=Gender_Choices, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2,
                                validators=[MinValueValidator(0.01)], default=0.1)
    discount_price = models.DecimalField(max_digits=6, decimal_places=2,
                                         validators=[MinValueValidator(0.00)], default=0.0, blank=True, null=True)
    active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# function to create a slug using the function (unique_slug_generator) that exist in the module (utils.py)
def create_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(create_slug, sender=Store)
pre_save.connect(create_slug, sender=Category)
pre_save.connect(create_slug, sender=Product)




# class ProductImage(models.Model):
#     product = models.ForeignKey(
#         'Product', default=None, on_delete=models.CASCADE)
#     images = models.FileField(upload_to='Products-images')

    # def __str__(self):
    #     return self.product.name

