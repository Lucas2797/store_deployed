from django.contrib import admin
from .models import Produto, Imagem, Modelo, Contact, Banner, BannerImages, Contact, Estoque



class ModeloAdmin(admin.ModelAdmin):
    list_display = ('modelo', 'publico', 'sexo', 'id')

class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('model', 'nome', 'preco', 'id')

class ContactAdmin(admin.ModelAdmin):
    list_display = ('nome', 'phone', 'email')

class ImagensAdmin(admin.ModelAdmin):
    list_display = ('product', 'image', 'id')

class BannerAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo')

class BannerImagesAdmin(admin.ModelAdmin):
    list_display = ('bannering', 'imagem')

class ContactAdmin(admin.ModelAdmin):
    list_display = ('nome', 'phone', 'email', 'mensagem')


class EstoqueAdmin(admin.ModelAdmin):
    list_display = ('product', 'tamanho', 'quantidade')


admin.site.register(Modelo, ModeloAdmin),
admin.site.register(Produto, ProdutoAdmin),
admin.site.register(Imagem, ImagensAdmin),
admin.site.register(Banner, BannerAdmin),
admin.site.register(BannerImages, BannerImagesAdmin),
admin.site.register(Contact, ContactAdmin),
admin.site.register(Estoque, EstoqueAdmin)