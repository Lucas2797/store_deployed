from django.db import models
from django.db.models import Q
from django.utils import timezone

class ProdutoManager(models.Manager):
    def price_low(self, preco):
        return self.filter(preco__lt=preco)

    def get_by_modelo(self, tipo):
        big = tipo.upper()
        return self.filter(model__modelo=big)

    def size_gte(self, size, modelo, preco, sexo):
        lista = []
        query = self.filter(model__publico='Crianca', model__modelo__icontains=modelo, preco__lte=preco, model__sexo__icontains=sexo, storage__quantidade__gt=0)
        for p in query:
            for e in p.storage.all():
                t = int(e.tamanho)
                if t >= int(size):
                    if p in lista:
                        pass
                    else:
                        lista.append(p) 
        return lista

    def size_gte2(self, size, modelo, preco, sexo):
        lista = []
        query = self.filter(model__publico='Adulto', model__modelo__icontains=modelo, preco__lte=preco, model__sexo__icontains=sexo, storage__quantidade__gt=0)
        for p in query:
            for e in p.storage.all():
                t = int(e.tamanho)
                if t >= int(size):
                    if p in lista:
                        pass
                    else:
                        lista.append(p) 
        return lista


class EstoqueManager(models.Manager):
    def size_lte(self, size):
        return self.filter(product__model__publico='Crianca', tamanho__lte=size)

    def is_new(self):
        return self.filter(updated_time__gte=(timezone.now() - timezone.timedelta(days=15)))


        # d1 = timezone.now() - self.updated_time
        # if d1.days <= 15:
        #     return True