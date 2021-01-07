from django.db import models
from django.forms import ModelForm, TextInput
from core.models import Product
from account.models import UserRegistration

STATUS = (
    ('In Progress', 'In Progress'),
    ('Canceled', 'Canceled'),
    ('Delayed', 'Delayed'),
    ('Delivered', 'Delivered'),
)


class ShopCart(models.Model):
    user_id = models.ForeignKey(
        UserRegistration, on_delete=models.SET_NULL, null=True)
    product_cart = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()
    create_at = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    Gender_Choiced = models.CharField(max_length=250, blank=True, null=True)
    color_Choiced = models.CharField(max_length=250, blank=True, null=True)
    size_Choiced = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return self.product_cart.name

    @property
    def price(self):
        return (self.product_cart.price)

    @property
    def amount(self):
        subtotal = 0
        if self.product_cart.discount_price:
            subtotal = self.product_cart.discount_price * self.quantity
        else:
            subtotal = self.price * self.quantity

        return subtotal


class Order(models.Model):

    user = models.ForeignKey(UserRegistration, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=80, blank=True)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=150)
    city = models.CharField(max_length=40)
    zip_code = models.CharField(max_length=8, blank=True)
    total = models.FloatField()
    note = models.TextField(null=True, default="", blank=True)
    status = models.CharField(
        choices=STATUS, default='In Progress', max_length=15)
    create_at = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username + ' - ' + str(self.total)


class OrderDetail(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(UserRegistration, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()
    total = models.FloatField()
    deliver_time = models.DateField()
    create_at = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    color_Choiced = models.CharField(max_length=250,blank=True, null=True)
    size_Choiced = models.CharField(max_length=250,blank=True, null=True)

    def __str__(self):
        return self.product.name

    @property
    def amount(self):
        if self.product.discount_price:
            return (self.product.discount_price * self.quantity)

        else:
            return (self.product.price * self.quantity)


class OrderForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['note'].required = False

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone',
                  'address', 'city', 'zip_code', 'note']
        widgets = {
            'first_name': TextInput(attrs={'class': 'input'}),
            'last_name': TextInput(attrs={'class': 'input'}),
            'email': TextInput(attrs={'class': 'input'}),
            'phone': TextInput(attrs={'class': 'input'}),
            'address': TextInput(attrs={'class': 'input'}),
            'city': TextInput(attrs={'class': 'input'}),
            'zip_code': TextInput(attrs={'class': 'input'}),
            'note': TextInput(attrs={'class': 'input'}),
        }


class ShopCartForm(ModelForm):
    class Meta:
        model = ShopCart
        fields = ['quantity', 'Gender_Choiced',
                  'color_Choiced', 'size_Choiced']
