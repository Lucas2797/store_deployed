from django.db import models
from django.template.defaultfilters import slugify
from .managers import ProdutoManager, EstoqueManager
from phonenumber_field.modelfields import PhoneNumberField
from django.core.exceptions import ValidationError
from django.utils import timezone


class Modelo(models.Model):

    CAMISA = 'CAMISA'
    REGATA = 'REGATA'
    VESTIDO = 'VESTIDO'
    MACACAO = 'MACACAO'
    CALSA = 'CALSA'
    SHORT = 'SHORT'
    INTIMA = 'INTIMA'
    tipo_choices = [
        (CAMISA, 'CAMISA'),
        (REGATA, 'REGATA'),
        (VESTIDO, 'VESTIDO'),
        (MACACAO, 'MACACAO'),
        (CALSA, 'CALSA'),
        (SHORT, 'SHORT'),
        (INTIMA, 'INTIMA'),
    ]


    Masculino = 'MASCULINO'
    Feminino = 'FEMININO'

    sexo_choice = [
        (Masculino, 'MASCULINO'),
        (Feminino, 'FEMININO')
    ]

    Crianca = 'Crianca'
    Adulto = 'Adulto'

    publico_choice = [
        (Crianca, 'Crianca'),
        (Adulto, 'Adulto')
    ]


    modelo = models.CharField(max_length=7, choices=tipo_choices)
    publico = models.CharField(choices=publico_choice, max_length=7)
    sexo = models.CharField(choices=sexo_choice, max_length=9)

    def __str__(self):
            return '%s-%s-%s' % (self.modelo, self.publico, self.sexo)

    def clean(self):
        mod = Modelo.objects.filter(modelo = self.modelo, publico=self.publico, sexo=self.sexo)
        if mod.exists():
            raise ValidationError('Modelo Já Existe')


class Produto (models.Model):
    model = models.ForeignKey(Modelo, on_delete=models.CASCADE, related_name='mod')
    nome = models.CharField(max_length=200)
    preco = models.DecimalField(max_digits=5, decimal_places=2)
    created_time = models.DateTimeField(auto_now=True)
    updated_time = models.DateTimeField(auto_now_add=True)
    activate = models.BooleanField(default=True)

    objects = ProdutoManager()

    def __str__(self):
        return '%s - %s' % (self.nome, self.model)
    
    def get_storage_total(self):
        total = 0
        e1 = self.storage.all()
        for e in e1:
            total += e.quantidade
        return total


    def all_buyed(self):
        total = 0
        for e in self.storage.all():
            total += e.quantidade
        for i in self.product_items.filter(is_ordered=True):
            total += i.quantity
        return total

    def all_selled(self):
        total = 0
        for i in self.product_items.filter(is_ordered=True):
            total += i.quantity
        return total

    def sell_percent(self):
        try:
            total = (self.all_selled() * 100)/ self.all_buyed()
            return total
        except ZeroDivisionError:
            return 'sem Vendidos'

class Estoque(models.Model):

    tamanhos = [
        ('Adulto', (
                ('P', 'P'),
                ('M', 'M'),
                ('G', 'G'),
                ('GG', 'GG'),
            )
        ),
        ('Infantil', (
                ('1', 1),
                ('2', 2),
                ('3', 3),
                ('4', 4),
                ('5', 5),
                ('6', 6),
                ('7', 7),
                ('8', 8),
                ('9', 9),
                ('10', 10),
                ('11', 11),
                ('12', 12),
            )
        ),
        ('Calsa', (
                ('36', 36),
                ('38', 38),
                ('40', 40),
                ('42', 42),
                ('44', 44),
                ('46', 46),
                ('48', 48),
                ('50', 50),
            )
        ),
        ('unknown', 'Unknown'),
    ]

    product = models.ForeignKey(Produto, on_delete=models.SET_NULL, null=True, related_name='storage')
    tamanho = models.CharField(max_length=100, choices=tamanhos)
    quantidade = models.PositiveIntegerField(default=0)
    created_time = models.DateTimeField(auto_now=True)
    updated_time = models.DateTimeField(auto_now_add=True)
    objects = EstoqueManager()


    def __str__(self):
        return '%s - %s - %s' % (self.product,self.tamanho, self.quantidade)

    def clean(self):
        stor = Estoque.objects.filter(product=self.product, tamanho=self.tamanho)
        if stor.exists():
            raise ValidationError('Estoque já existente')
        list1 = ['36', '38', '40', '42', '44', '46', '48', '50']
        list2 = ['P', 'M', 'G', 'GG']
        list3 = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
        if self.product.model.modelo == 'CALSA' and self.product.model.publico == 'Adulto' and self.tamanho not in list1:
            raise ValidationError('por favor selecione um tamanho para Calsa')
        if self.product.model.modelo != 'CALSA'  and self.product.model.publico == 'Adulto' and self.tamanho not in list2:
            raise ValidationError('por favor selecione um tamanho para Adultos')
        if self.product.model.publico == 'Crianca' and self.tamanho not in list3:
            raise ValidationError('por favor selecione um tamanho para Crianca')
        
        

def get_image_filename(instance, filename):
    nome = instance.product.nome
    slug = slugify(nome)
    return "produto_imagens/%s-%s" % (slug, filename)


class Imagem (models.Model):
    product = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=get_image_filename)


class Contact (models.Model):
    nome = models.CharField(max_length=100)
    phone = PhoneNumberField()
    email = models.EmailField()
    mensagem = models.TextField(max_length=600, default='Mensagem')

class Banner(models.Model):
    Inicial = 'Inicial'
    Mini = 'Mini'
    Adjacentes = 'Adjacentes'
    Promocao = 'Promocao'
    tipos_banner = [
        (Inicial, 'Inicial'),
        (Mini, 'Mini'),
        (Promocao, 'Promocao'),
        (Adjacentes, 'Adjacentes'),
    ]
    
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=10, choices=tipos_banner)

    def __str__(self):
        return '%s %s' % (self.nome, self.tipo)


def get_banner_image_filename(instance, filename):
    nome = instance.bannering.nome
    slug = slugify(nome)
    return "banner_imagens/%s-%s" % (slug, filename)

class BannerImages(models.Model):
    bannering = models.ForeignKey(Banner, on_delete=models.CASCADE, related_name='banner_image')
    imagem = models.ImageField(upload_to=get_banner_image_filename)
    link = models.URLField(max_length=200, default='products/home')

    def __str__(self):
        return '%s %s' % (self.bannering, self.imagem)