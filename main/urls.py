from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.HomeView.as_view(), name= 'home'),
    path('waad/<slug>/', views.ItemDetailView.as_view(), name = 'item_detail'),
    path('category/', views.ItemListView.as_view(), name = 'item_list'),
    path('cart_summry/', views.CartView.as_view(), name = 'cart_summry'),
    path('contact/', views.ClientMessageVeiw.as_view(), name = 'contact'),
    path('confirmation/', views.ConfirmatonView.as_view(), name = 'confirmation'),


    path('add_item/<slug>/', views.add_item_to_cart, name = 'add_item'),
    path('remove_single_item/<slug>/', views.remove_single_item_from_cart, name = 'remove_single_item'),
    path('remove_item/<slug>/', views.remove_item_from_cart, name = 'remove_item'),

    path('checkout/', views.CheckoutView.as_view(), name= 'checkout'),
    path('payment/<payment_option>/', views.PaymentView.as_view(), name= 'payment'),
    path('request_refund', views.RefundView.as_view(), name= 'request_refund'),
    path('add_coupon/', views.CouponView.as_view(), name= 'add_coupon'),


]
