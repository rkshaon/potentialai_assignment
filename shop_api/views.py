from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from shop_api.models import Shop

from shop_api.serializers import ShopSerializer



class ShopViewSet(viewsets.ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer


    def create(self, request, *args, **kwargs):
        if not request.user.is_vendor:
            return Response({'error': 'Only vendors can create shops.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
