from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.permissions import AllowAny

from django.contrib.auth import authenticate, login

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


# permission_classes([AllowAny])
# @authentication_classes([])
# class UserLoginView(ObtainAuthToken):
#     def post(self, request, *args, **kwargs):
#         print(request.data)
#         serializer = self.serializer_class(data=request.data, context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({'token': token.key, 'user_id': user.id, 'username': user.username})

class UserLoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        print(username)
        print(password)

        user = authenticate(request, username=username, password=password)

        print(user)

        if user is not None:
            login(request, user)
            # You can customize the response data based on your needs
            return Response({'message': 'Login successful', 'user_id': user.id, 'username': user.username})
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class UserListView(GenericViewSet, ListModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer