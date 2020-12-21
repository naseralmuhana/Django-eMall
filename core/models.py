from django.db import models
from django.db.models.signals import pre_save
from django.core.validators import MaxValueValidator, MinValueValidator

from multiselectfield import MultiSelectField
from eMall.utils import unique_slug_generator

Gender_Choices = (
    ('male', 'male'),
    ('female', 'female'),
    ('kid', 'kid'),
)

Size_Choices = (
    ('XS', 'XS'),
    ('S', 'S'),
    ('M', 'M'),
    ('L', 'L'),
    ('XL', 'XL'),
)

Color_Choices = (
    ('#FFFFFF', 'White', ),
    ('#C0C0C0', 'Sliver',),
    ('#808080', 'Gray', ),
    ('#000000', 'Black', ),
    ('#FF0000', 'Red',),
    ('#FFFF00', 'Yellow', ),
    ('#008000', 'Green', ),
    ('#0000FF', 'Blue', ),
    ('#800080', 'Purple', ),
)


class Store(models.Model):

    name = models.CharField(max_length=250, unique=True)
    image = models.ImageField(upload_to="Stores-Images", null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Category(models.Model):

    name = models.CharField(max_length=250, unique=True)
    image = models.ImageField(
        upload_to="Categoies-Images", null=True, blank=True)
    store = models.ForeignKey(to="Store", on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Product(models.Model):

    name = models.CharField(max_length=250, unique=True)
    category = models.ForeignKey(to='Category', on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='Products-Images', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.1,
                                validators=[MinValueValidator(0.01)])
    discount_price = models.DecimalField(max_digits=6, decimal_places=2, default=0.0,
                                         validators=[MinValueValidator(0.00)], blank=True, null=True)
    gender = MultiSelectField(choices=Gender_Choices, null=True, blank=True)
    size = MultiSelectField(choices=Size_Choices, null=True, blank=True)
    color = MultiSelectField(choices=Color_Choices, null=True, blank=True)
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
