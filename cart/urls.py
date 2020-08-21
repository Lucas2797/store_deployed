from django.urls import path
from . import views


urlpatterns = [
    #FRONT#
    path('add_to_cart/<int:id>', views.add_to_cart, name='add_to_cart'),
    path('order_summary/', views.order_details, name='order_summary'),
    path('success/', views.success, name='purchase_success'),
    path('item/delete/<int:id>', views.delete_from_cart, name='delete_item'),
    path('checkout/', views.checkout, name='checkout'),
    #BACK#
    path('all_orders/', views.all_orders, name='all_orders'),
    path('order/<int:id>', views.order_detail, name='order_detail'),
    path('order/delete/<int:id>', views.order_delete, name='order_delete')
]