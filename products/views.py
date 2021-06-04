from django.core.files.storage import default_storage
from django.shortcuts import render
from rest_framework import generics, mixins,viewsets
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView 

from mainproject.pagination import CustomPagination
from products.models import Product
from products.serializers import ProductSerializer
from core.authentication import JWTAuthentication



class ProductGenericAPIView(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated ]
    pagination_class = CustomPagination
    permission_object = 'roles'
    serializer_class = ProductSerializer
    queryset = Product.objects.all()



class FileUploadView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser,)

    def post(self, request):
        file = request.FILES['image']
        file_name = default_storage.save(file.name, file)
        url = default_storage.url(file_name)

        return Response({
            'url': 'http://127.0.0.1:8000/pro' + url
        })
