from django.db import models
from django.forms import ModelForm, Textarea
from django.db.models.signals import pre_save
from django.core.validators import MaxValueValidator, MinValueValidator

from multiselectfield import MultiSelectField
from eMall.utils import unique_slug_generator
from account import models as account_models

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

RATING = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
)


class StoreType(models.Model):
    name = models.CharField(max_length=250, unique=True)
    image = models.ImageField(
        upload_to="StoresType-Images", null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Store(models.Model):

    name = models.CharField(max_length=250, unique=True)
    storetype = models.ForeignKey(to='StoreType', verbose_name=(
        'Store Type'), on_delete=models.CASCADE)
    image = models.ImageField(upload_to="Stores-Images", null=True, blank=True)
    logo = models.ImageField(upload_to="Stores-logos", null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


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

    class Meta:
        ordering = ["name"]


class Brand(models.Model):
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Product(models.Model):

    name = models.CharField(max_length=900, unique=True)
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
    brand = models.ForeignKey(
        to='Brand', on_delete=models.CASCADE, null=True, blank=True)
    active = models.BooleanField(default=True)
    favourite = models.ManyToManyField(
        account_models.UserRegistration, related_name='favourite', blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def store_name(self):
        return self.category.store.name

    def discount_percentage(self):
        discount_precent = int(100 - (self.discount_price / self.price)*100)
        return discount_precent

    class Meta:
        ordering = ["name"]


# function to create a slug using the function (unique_slug_generator) that exist in the module (utils.py)
def create_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(create_slug, sender=StoreType)
pre_save.connect(create_slug, sender=Store)
pre_save.connect(create_slug, sender=Category)
pre_save.connect(create_slug, sender=Product)


class Comment(models.Model):

    product = models.ForeignKey(to="Product", on_delete=models.CASCADE)
    user = models.ForeignKey(
        account_models.UserRegistration, on_delete=models.CASCADE)
    review = models.TextField(max_length=1000)
    rating = models.IntegerField(choices=RATING, default=0)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name + ' - ' + self.user.username

    def username(self):
        return self.user.username
    
    class Meta:
        ordering = ['-create_at']


# class for the form of the comment section. we can write it in the forms.py or here.
class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['review', 'rating']
        widgets = {
            'review': Textarea(attrs={'class': 'input'}),
            'rating': Textarea(attrs={'class': 'input'}),
        }
