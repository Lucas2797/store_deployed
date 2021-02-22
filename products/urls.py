from django.urls import path
from . import views


urlpatterns = [
    #FRONT#
    path('home/', views.amp_home, name='home_product'),
    path('list/', views.list_view, name='list_product'),
    path('list/kids/', views.kids_list_view, name='kids_list_product'),
    path('list/adult/', views.adult_list_view, name='adult_list_product'),
    path('detail/<int:id>', views.detail_view, name='detail_product'),
    path('contact/', views.contact_view, name='contact'),
    path('chat/', views.chat_view, name='chat'),
    path('company/', views.company_view, name='company'),
    path('suport/', views.suport_view, name='suport'),
    #test#
    path('test/', views.test_view, name='test_view'),
    #BACK#
    path('admin', views.admin_view, name='admin_product'),
    path('admin/product', views.all_products, name='all_products'),
    path('admin/add_product', views.add_product, name='add_product'),
    path('admin/add_modelo', views.add_modelo, name='add_modelo'),
    path('admin/add_storage/<int:id>', views.add_storage, name='add_storage'),
    path('admin/update_product/<int:id>', views.update_product, name='update_product'),
    path('admin/delete_product/<int:id>', views.delete_product, name='delete_product'),
    path('admin/delete_image/<int:id>', views.delete_image, name='delete_image'),
    path('admin/add_banner/', views.add_banner, name='add_banner')

]
