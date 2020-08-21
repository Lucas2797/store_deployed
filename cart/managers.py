from django.db import models


class ItemManager(models.Manager):
    def order_items(self, order):
        return self.objects.filter(order=order)



class PedidoManager(models.Manager):
    def cart_total(self, pedido):
        return self.objects.all()