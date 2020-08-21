from django.shortcuts import render, redirect
from .models import Produto, Imagem, Modelo, Banner, BannerImages, Estoque
from .forms import ProdutoForm, ImagemForm, ModeloForm, BannerForm, BannerImagesForm, ContactForm, EstoqueForm, TestForm
from django.forms import modelformset_factory
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from cart.models import Pedido, Item
from accounts.decorators import allowed_users 
from django.db.models import Q
from cart.models import Item, Pedido
from django.http import HttpResponseRedirect
from django.forms import inlineformset_factory



#FRONT#
def amp_home(request):
    for b in Banner.objects.filter(tipo='Inicial'):
        filter1 = b.banner_image.all()
    filter2 = Banner.objects.filter(tipo='Mini')
    context = {
        'filter1': filter1,
        'filter2': filter2,
        }
    if request.user_agent.is_mobile:
        return render(request, 'amp/home.amp.html', context)
    elif request.user_agent.is_pc:
        return render (request, 'desktop/home.amp.html', context)
    else:
        return render (request, 'amp/home.amp.html', context)



def list_view(request):
    model_query = request.GET.get('model_query', '')
    price_query = request.GET.get('price_query', '')
    size_query_all = request.GET.get('size_query_all', '')
    size_query_calsa = request.GET.get('size_query_calsa', '')
    sex_query = request.GET.get('sex_query', '')

    if model_query or price_query or size_query_all:
        if model_query == 'CALSA':
            query = Produto.objects.filter(Q(model__modelo__icontains='CALSA'),
                Q(preco__lte=price_query),
                Q(storage__tamanho__gte=size_query_calsa),
                Q(model__sexo__icontains=sex_query),
                Q(storage__quantidade__gt=0)).distinct

        else:
            query = Produto.objects.filter(Q(model__modelo__icontains=model_query),
                Q(preco__lte=price_query),
                Q(storage__tamanho__gte=size_query_all),
                Q(model__sexo__icontains=sex_query),
                Q(storage__quantidade__gt=0)).distinct
    
    
    else:
        query = Produto.objects.filter(storage__quantidade__gt=0).distinct()

        context = {
            'query': query
        }
    if request.user_agent.is_mobile:
        return render(request, 'amp/AllList.amp.html', context)
    elif request.user_agent.is_pc:
        return render (request, 'desktop/AllList.amp.html', context)
    else:
        return render (request, 'amp/AllList.amp.html', context)

def kids_list_view(request):
    model_query = request.GET.get('model_query', '')
    price_query = request.GET.get('price_query', '')
    size_query = request.GET.get('size_query', '')
    sex_query = request.GET.get('sex_query', '')


    if model_query or price_query or size_query or sex_query:
        query = Produto.objects.size_gte(size=size_query, modelo=model_query, preco=price_query, sexo=sex_query)
    
    else:
        query = Produto.objects.filter(Q(model__publico='Crianca'), Q(storage__quantidade__gt=0)).distinct()
        context = {
            'query': query
        }
    if request.user_agent.is_mobile:
        return render(request, 'amp/KidsList.amp.html', context)
    elif request.user_agent.is_pc:
        return render (request, 'desktop/KidsList.amp.html', context)
    else:
        return render (request, 'amp/KidsList.amp.html', context)

def adult_list_view(request):
    model_query = request.GET.get('model_query', '')
    price_query = request.GET.get('price_query', '')
    size_query_all = request.GET.get('size_query_all', '')
    size_query_calsa = request.GET.get('size_query_calsa', '')
    sex_query = request.GET.get('sex_query', '')

    if model_query or price_query or size_query_all or sex_query:
        if 'CALSA' in model_query:
            size_query = size_query_calsa
            query = Produto.objects.size_gte2(size=size_query, modelo='CALSA', preco=price_query, sexo=sex_query)
        else:
            size_query = size_query_all
            query = Produto.objects.filter(model__publico__icontains='Adulto', storage__tamanho__icontains=size_query, model__modelo__icontains=model_query, preco__lte=price_query, model__sexo__icontains=sex_query).distinct()
        
    else:
        query = Produto.objects.filter(Q(model__publico='Adulto'), Q(storage__quantidade__gt=0)).distinct()

        context = {
            'query': query
        }
    if request.user_agent.is_mobile:
        return render(request, 'amp/AdultList.amp.html', context)
    elif request.user_agent.is_pc:
        return render (request, 'desktop/AdultList.amp.html', context)
    else:
        return render (request, 'amp/AdultList.amp.html', context)

def detail_view(request, id):
    prod = get_object_or_404(Produto, pk=id)
    query = Produto.objects.filter(model=prod.model)
    context = {
        'prod': prod,
        'query': query,
    }
    if request.user_agent.is_mobile:
        return render(request, 'amp/detail.amp.html', context)
    elif request.user_agent.is_pc:
        return render (request, 'desktop/detail.amp.html', context)
    else:
        return render (request, 'desktop/detail.amp.html', context)

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home_product')

    else:
        form = ContactForm()


    context = {'form': form}
    if request.user_agent.is_mobile:
        return render(request, 'amp/contact.amp.html', context)
    elif request.user_agent.is_pc:
        return render (request, 'desktop/contact.amp.html', context)
    else:
        return render (request, 'desktop/contact.amp.html', context)


def chat_view(request):
    if request.user_agent.is_mobile:
        return render(request, 'amp/chat.amp.html')
    elif request.user_agent.is_pc:
        return render (request, 'desktop/chat.amp.html')
    else:
        return render (request, 'desktop/chat.amp.html')



                     #BACK#

@allowed_users(allowed_ones=['Admin', 'Vendedor'])
def admin_view(request):
    query = Produto.objects.all()
    context = {
        'query': query,
    }
    if request.user_agent.is_mobile:
        return render(request, 'admin_amp/admin.amp.html', context)
    elif request.user_agent.is_pc:
        return render (request, 'admin/admin.amp.html', context)
    else:
        return render (request, 'admin_amp/admin.amp.html', context)

@allowed_users(allowed_ones=['Admin', 'Vendedor'])
def all_products(request):
    query = Produto.objects.all()
    context = {
        'query': query,
    }
    if request.user_agent.is_mobile:
        return render(request, 'admin_amp/all_products.amp.html', context)
    elif request.user_agent.is_pc:
        return render (request, 'admin/all_products.amp.html', context)
    else:
        return render (request, 'admin_amp/all_products.amp.html', context)


@login_required
@allowed_users(allowed_ones=['Admin', 'Vendedor'])
def add_modelo(request):
    if request.method == 'POST':
        form = ModeloForm(request.POST)
        if form.is_valid():
            form.save()
        
    else:
        form = ModeloForm()
   
    context = {
        'form': form,
    }
    if request.user_agent.is_mobile:
        return render(request, 'admin_amp/modelo_add.amp.html', context)
    elif request.user_agent.is_pc:
        return render (request, 'admin/modelo_add.amp.html', context)
    else:
        return render (request, 'admin_amp/modelo_add.amp.html', context)

@login_required
@allowed_users(allowed_ones=['Admin', 'Vendedor'])
def add_product(request):
    if request.method == 'POST':
        prod_form = ProdutoForm(request.POST)
        if prod_form.is_valid():
            prod = prod_form.save()
            return redirect(reverse('update_product', kwargs={'id': prod.id}))

    else:
        prod_form = ProdutoForm()

    context = {
        'prod_form': prod_form,
    }
    if request.user_agent.is_mobile:
        return render(request, 'admin_amp/produto_add.amp.html', context)
    elif request.user_agent.is_pc:
        return render (request, 'admin/produto_add.amp.html', context)
    else:
        return render (request, 'admin_amp/produto_add.amp.html', context)

def add_storage(request, id):
    prod = Produto.objects.get(id=id)
    query = Estoque.objects.all()
    if request.method == 'POST':
        storage_form = EstoqueForm(request.POST)
        if storage_form.is_valid():
            storage_form.save()

    else:
        storage_form = EstoqueForm(instance=prod)

    context = {
        'prod': prod,
        'query': query,
        'storage_form': storage_form
    }
    if request.user_agent.is_mobile:
        return render(request, 'admin_amp/storage_add.amp.html', context)
    elif request.user_agent.is_pc:
        return render (request, 'admin/storage_add.amp.html', context)
    else:
        return render (request, 'admin_amp/storage_add.amp.html', context)
    



@login_required
@allowed_users(allowed_ones=['Admin', 'Vendedor'])
def add_banner(request):
    BannerImageFormSet = modelformset_factory(BannerImages, fields=('imagem',), extra=4)
    if request.method == 'POST':
        form = BannerForm(request.POST)
        form2 = BannerImageFormSet(request.POST, request.FILES)
        if form.is_valid() and form2.is_valid():
            banner = form.save(commit=False)
            banner.save()
            for f in form2:
                try:
                    photo = BannerImages(banner=banner, imagem=f.cleaned_data['imagem'])
                    photo.save()

                except Exception as e:
                    break
            return redirect('/products/admin')
    else:
        form = BannerForm()
        form2 = BannerImageFormSet(queryset=Imagem.objects.none())
    context = {
        'form': form,
        'form2': form2,

    }
    if request.user_agent.is_mobile:
        return render(request, 'admin_amp/banner_add.amp.html', context)
    elif request.user_agent.is_pc:
        return render (request, 'admin/banner_add.amp.html', context)
    else:
        return render (request, 'admin_amp/banner_add.amp.html', context)
    

@allowed_users(allowed_ones=['Admin', 'Vendedor'])
def update_product(request, id):
    prod = Produto.objects.get(id=id)

    prod_form = ProdutoForm(instance=prod)
    img_form = ImagemForm()
    model_form = ModeloForm()
    storage_form = EstoqueForm(instance=prod)

    prod_query = Produto.objects.all()
    img_query = Imagem.objects.all()
    model_query = Modelo.objects.all()
    storage_query = Estoque.objects.all()

    t1 = 'no'
    t2 = request.POST
    if request.method == 'POST' and 'producting' in request.POST:
        print('PROD')
        prod_form = ProdutoForm(request.POST, instance=prod)
        t1 = 'product'
        t2 = request.POST
        if prod_form.is_valid():
            prod_form.save()

    elif request.method == 'POST' and 'img' in request.POST:
        print('IMG')
        img_form = ImagemForm(request.POST, request.FILES)
        t1 = 'img'
        t2 = request.POST
        if img_form.is_valid():
            img = img_form.save(commit=False)
            img.product = prod
            img.save()

    elif request.method == 'POST' and 'model' in request.POST:
        print('MODEL')
        model_form = ModeloForm(request.POST)
        t1 = 'model'
        t2 = request.POST
        if model_form.is_valid():
            model_form.save()

    elif request.method == 'POST' and 'storage' in request.POST:
        print('STORAGE')
        storage_form = EstoqueForm(request.POST)
        t1 = 'storage'
        t2 = request.POST
        if storage_form.is_valid():
            stg = storage_form.save(commit=False)
            stg.product = prod
            stg.save()


    else:
        prod_form = ProdutoForm(instance=prod)
        img_form = ImagemForm()
        model_form = ModeloForm()
        storage_form = EstoqueForm(instance=prod)

    context = {
        'prod': prod,
        'prod_query': prod_query,
        'img_query': img_query,
        'storage_query': storage_query,
        'model_query': model_query,
        'prod_form': prod_form,
        'img_form': img_form,
        'model_form': model_form,
        'storage_form': storage_form,
        't1': t1,
        't2': t2,
    }
    if request.user_agent.is_mobile:
        return render(request, 'admin_amp/update_product.amp.html', context)
    elif request.user_agent.is_pc:
        return render (request, 'admin/update_product.amp.html', context)
    else:
        return render (request, 'admin_amp/update_product.amp.html', context)

def update_image(request, id):
    img = Imagem.objects.get(id=id)
    img.image.url = request.GET.get('Image')
    img.save()


@allowed_users(allowed_ones=['Admin'])
def delete_product(request, id):
    prod = Produto.objects.get(id=id)
    prod.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@allowed_users(allowed_ones=['Admin'])
def delete_image(request, id):
    img = Imagem.objects.get(id=id)
    img.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
@allowed_users(allowed_ones=['Admin'])
def test_view(request):
    var = request.GET.get('var', '')
    print(var)

    context = {
        'var': var,
    }

    if request.user_agent.is_mobile:
        return render(request, 'amp/test.amp.html', context)
    elif request.user_agent.is_pc:
        return render (request, 'desktop/test.amp.html', context)
    else:
        return render (request, 'test.html', context)












#    prod = Produto.objects.get(id=id)

#     prod_form = ProdutoForm(instance=prod)
#     img_form = ImagemForm()
#     model_form = ModeloForm()
#     storage_form = EstoqueForm(instance=prod)

#     prod_query = Produto.objects.all()
#     img_query = Imagem.objects.all()
#     model_query = Modelo.objects.all()
#     storage_query = Estoque.objects.all()

#     t1 = 'no'
#     t2 = request.POST
#     if request.method == 'POST' and 'producting' in request.POST:
#         print('PROD')
#         prod_form = ProdutoForm(request.POST, instance=prod)
#         t1 = 'product'
#         t2 = request.POST
#         if prod_form.is_valid():
#             prod_form.save()

#     elif request.method == 'POST' and 'img' in request.POST:
#         print('IMG')
#         img_form = ImagemForm(request.POST, request.FILES)
#         t1 = 'img'
#         t2 = request.POST
#         if img_form.is_valid():
#             img = img_form.save(commit=False)
#             img.product = prod
#             img.save()

#     elif request.method == 'POST' and 'model' in request.POST:
#         print('MODEL')
#         model_form = ModeloForm(request.POST)
#         t1 = 'model'
#         t2 = request.POST
#         if model_form.is_valid():
#             model_form.save()

#     elif request.method == 'POST' and 'storage' in request.POST:
#         print('STORAGE')
#         storage_form = EstoqueForm(request.POST)
#         t1 = 'storage'
#         t2 = request.POST
#         if storage_form.is_valid():
#             stg = storage_form.save(commit=False)
#             stg.product = prod
#             stg.save()


#     else:
#         prod_form = ProdutoForm(instance=prod)
#         img_form = ImagemForm()
#         model_form = ModeloForm()
#         storage_form = EstoqueForm(instance=prod)

#     context = {
#         'prod': prod,
#         'prod_query': prod_query,
#         'img_query': img_query,
#         'storage_query': storage_query,
#         'model_query': model_query,
#         'prod_form': prod_form,
#         'img_form': img_form,
#         'model_form': model_form,
#         'storage_form': storage_form,
#         't1': t1,
#         't2': t2,
#     }
#     if request.user_agent.is_mobile:
#         return render(request, 'amp/test.amp.html', context)
#     elif request.user_agent.is_pc:
#         return render (request, 'desktop/test.amp.html', context)
#     else:
#         return render (request, 'test.html', context)



    # prod = Produto.objects.get(id=id)
    # ImgFormSet = inlineformset_factory(Produto, Imagem, fields=('image',))
    # if request.method == 'POST':
    #     prod_form = ProdutoForm(request.POST, instance=prod)
    #     img_form = ImgFormSet(request.POST, request.FILES, instance=prod)
    #     if prod_form.is_valid() and img_form.is_valid():
    #         prod_form.save()
    #         img_form.save()

    # else:
    #     prod_form = ProdutoForm(instance=prod)
    #     img_form = ImgFormSet(instance=prod)

    # context = {
    #    'prod_form': prod_form,
    #    'img_form': img_form,
    #    'prod': prod
    # }




    # model_create = request.GET.get('model_create')
    # if request.method == 'POST':
    #     model_form = ModeloForm(request.POST)
    #     if model_form.is_valid():
    #         model = model_form.save(commit=False)
    #         model.save()
    #         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    # ImagemFormSet = modelformset_factory(Imagem, fields=('image',), extra=4)
    # if request.method == 'POST':
    #     product_form = ProdutoForm(request.POST)
    #     formset = ImagemFormSet(request.POST or None, request.FILES)
    #     if product_form.is_valid() and formset.is_valid():
    #         product = product_form.save(commit=False)
    #         product.save()

    #         for f in formset:
    #             try:
    #                 photo = Imagem(product=product, image=f.cleaned_data['image'])
    #                 photo.save()

    #             except Exception as e:
    #                 break
    #         return redirect('/products/admin')
    # else:
    #     product_form = ProdutoForm()
    #     formset = ImagemFormSet(queryset=Imagem.objects.none())
    #     model_form = ModeloForm()
    # context = {
    #     'product_form': product_form,
    #     'formset': formset,
    #     'model_form': model_form
    # }
    # if request.user_agent.is_mobile:
    #     return render(request, 'amp/test.amp.html', context)
    # elif request.user_agent.is_pc:
    #     return render (request, 'desktop/test.amp.html', context)
    # else:
    #     return render (request, 'test.html', context)