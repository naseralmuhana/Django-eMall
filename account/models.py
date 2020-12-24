from django.db import models
from django.contrib.auth.models import AbstractUser


class UserRegistration(AbstractUser):
    is_customer = models.BooleanField(default=True, verbose_name=("Customer"))
    is_owner = models.BooleanField(default=False, verbose_name=("Store Owner"))
    phone_number = models.CharField(verbose_name=(
        "Phone Number"), max_length=10, blank=True, null=True)

    class Meta:
        ordering = ["username"]
    # def __str__(self):
    #     return f"{self.username}: {self.first_name} {self.last_name}"
