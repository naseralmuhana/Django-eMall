from django.db import models
from django.contrib.auth.models import AbstractUser
import core

Cities = (
    ('Amman', 'Amman', ),
    ('Irbid', 'Irbid', ),
    ('Ajloun', 'Ajloun',),
    ('Jerash', 'Jerash', ),
    ('Mafraq', 'Mafraq', ),
    ('Balqa', 'Balqa',),
    ('Zarqa', 'Zarqa', ),
    ('Madaba', 'Madaba', ),
    ('Karak', 'Karak', ),
    ('Tafilah', 'Tafilah', ),
    ("Ma'an", "Ma'an", ),
    ('Aqaba', 'Aqaba', ),
)


class UserRegistration(AbstractUser):
    image = models.ImageField(
        upload_to='User-Profile-Images', null=True, blank=True)
    phone_number = models.CharField(verbose_name=(
        "Phone Number"), max_length=10, blank=True, null=True)
    city = models.CharField(
        choices=Cities, max_length=100, blank=True, null=True)
    address = models.CharField(verbose_name=(
        "Address"), max_length=256, blank=True, null=True)
    zip_code = models.CharField(verbose_name=(
        "Zip Code"), max_length=5, blank=True, null=True)

    class Meta:
        ordering = ["username"]


class OwnerProfile(models.Model):
    user = models.ForeignKey(UserRegistration, on_delete=models.CASCADE)
    store = models.ForeignKey('core.Store', on_delete=models.CASCADE)

    def __str__(self):
        return self.store.name + ' - ' + self.user.username
        
    class Meta:
        ordering = ["store"]
