from django.db import models

from goods.models import Products
from users.models import User

class CartQueryset(models.QuerySet):
    
    def total_price(self):
        return sum(cart.products_price() for cart in self)
    
    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0

class Cart(models.Model):

    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True, verbose_name= 'Пользователь' )
    product = models.ForeignKey(to=Products, on_delete=models.CASCADE, verbose_name= 'Товар')
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name='Количество')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    session_key = models.CharField(max_length=32, blank=True, null=True)

    objects = CartQueryset().as_manager()

    class Meta:
        db_table = 'cart_model'
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
    
    def products_price(self):
        return round(self.product.sell_price() * self.quantity,2)
    
    def __str__(self):
        return f'Корзина {self.user.username} | Товар {self.product.name} | Количество {self.quantity}'
 