from django.core.files.storage import default_storage
from django.shortcuts import render
from rest_framework import generics, mixins,viewsets
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView 
from django.db.models import Q
from mainproject.pagination import CustomPagination
from products.models import Product
from products.serializers import ProductSerializer
from core.authentication import JWTAuthentication

from core.models import User
from orders.models import Order
import cloudinary.uploader

class ProductGenericAPIView(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated ]
    pagination_class = CustomPagination
    permission_object = 'roles'
    serializer_class = ProductSerializer
    # queryset = Product.objects.all()

    def get_queryset(self,*args,**kwargs):
        queryset = Product.objects.all()
        query = self.request.query_params.dict()
        keyword = query.get("keyword",'')
        if keyword:
            queryset =  queryset.filter(
                Q(title__icontains=keyword) |
                 Q(description__icontains=keyword )|
                  Q(price__icontains=keyword )
                )
        return queryset.order_by("-id")

class TotalCount(APIView):
    def get(self,request,*args, **kwargs):
        total_products = Product.objects.all().count()
        total_users = User.objects.all().count()
        total_orders = Order.objects.all().count()
        return Response({
            'total_products':total_products,
            'total_users':total_users,
            'total_orders':total_orders,
        })



class FileUploadView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser,)

    def post(self, request):
        file= request.data.get('image')
        upload_data = cloudinary.uploader.upload(file)
        # url = default_storage.url(file_name)

        return Response({
            'status': 'success',
            'data': upload_data,
        })


