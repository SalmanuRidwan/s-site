from django.conf import settings
from django.db import models
from django.urls import reverse


CATEGORY_CHOICES = (
    ('S', 'Shirt'),
    ('SW', 'Sport wear'),
    ('OW', 'Outwear'),
)

LABLE_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger'),
)

class Shoe(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    label = models.CharField(choices=LABLE_CHOICES, max_length=1)
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField(blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('main:product', kwargs={
            'slug': self.slug
        })
        
    def get_add_to_cart_url(self):
        return reverse('main:add-to-cart', kwargs={
            'slug': self.slug
        })
        
    def get_remove_from_cart_url(self):
        return reverse('main:remove-from-cart', kwargs={
            'slug': self.slug
        })
    
class OrderShoe(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    ordered = models.BooleanField(default=False)
    shoe = models.ForeignKey(
        Shoe,
        on_delete=models.CASCADE,
    )
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.shoe.title}"
    
    def get_total_item_price(self):
        return self.quantity * self.shoe.price 
    
    def get_total_discount_item_price(self):
        return self.quantity * self.shoe.discount_price
    
    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()
    
    def get_final_price(self):
        if self.shoe.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()

class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    shoes = models.ManyToManyField(OrderShoe)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    
    def get_total(self):
        total = 0
        for order_item in self.shoes.all():
            total += order_item.get_final_price()
        return total
    