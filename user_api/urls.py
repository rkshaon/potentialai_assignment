from django.urls import path

from user_api.views import UserViewSet
from user_api.views import UserListView



urlpatterns = [
    path('registration', UserViewSet.as_view({
        'post': 'register',
    })),
    path('', UserListView.as_view({
        'get': 'list',
    })),
]