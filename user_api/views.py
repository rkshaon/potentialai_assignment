from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action

from django.contrib.auth.models import Group
from user_api.models import User

from user_api.serializers import UserSerializer



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    
    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response({
            'id': user.id, 
            'username': user.username, 
            'email': user.email, 
            'is_vendor': user.is_vendor
            }, status=status.HTTP_201_CREATED, headers=headers)
    

    def perform_create(self, serializer):
        user = serializer.save()
        password = self.request.data.get('password')
        user.set_password(password)

        # Assign user to groups based on the role
        if self.request.data.get('is_vendor'):
            vendor_group = Group.objects.get(name='Vendor')
            user.groups.add(vendor_group)
        else:
            customer_group = Group.objects.get(name='Customer')
            user.groups.add(customer_group)

        user.save()
        return user


class UserListView(GenericViewSet, ListModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer