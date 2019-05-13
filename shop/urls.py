from django.urls import path
from .views import *


urlpatterns = [
    path('', MainPageView.as_view(), name='main_page'),
    path('catalog/', Catalog.as_view(), name='catalog'),
    path('category/<slug>/', CategoryListView.as_view(), name='category_view'),
    path('product/<slug>/', ProductDetailView.as_view(), name='product_view'),
    path('info/<slug>/', InfopageView.as_view(), name='infopage_view'),
    path('cart/', CartView.as_view(), name='cart_view'),
    path('json_cart/', get_json_cart, name='get_json_cart'),
]
