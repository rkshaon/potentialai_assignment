from django.urls import path

from shop_api.views import ShopViewSet



urlpatterns = [
    path('shop-register', ShopViewSet.as_view({
        'post': 'create',
    })),
]