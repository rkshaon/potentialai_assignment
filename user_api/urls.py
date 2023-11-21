from django.urls import path

from user_api.views import UserViewSet



urlpatterns = [
    path('registration', UserViewSet.as_view({
        'post': 'register',
    })),
]