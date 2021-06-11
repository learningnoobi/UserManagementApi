from rest_framework import exceptions, viewsets, status, generics, mixins
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from .serializers import *
from .models import User, Permission, Role
from .authentication import generate_access_token, JWTAuthentication
from rest_framework.generics import ListAPIView
from mainproject.pagination import CustomPagination
from.permissions import ViewPermissions
from django.db.models import Q
@api_view(['GET'])
def users(request):
    user = User.objects.all()
    serializer = UserSerializer(user,many=True)
    return Response({
        "users":serializer.data
    })

@api_view(['POST'])
def register(request):
    data = request.data
    first_name = data['first_name']
    last_name = data['last_name']
    email = data['email']
    role= "Editor"
    if data['password'] != data['password_confirm']:
        raise exceptions.APIException('Passwords do not match!')
    if len(data['password']) < 6:
        raise exceptions.APIException('Passwords must be larger than 6 letters!')
    new_user = User(
        first_name=first_name,last_name=last_name,
        email=email,password= data['password'] ,
        role=Role.objects.get(name=role)
        )
    new_user.set_password(data['password'])
    new_user.save()
    serializer = UserSerializer(new_user)
    return Response(serializer.data)


@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = User.objects.filter(email=email).first()

    if user is None:
        raise exceptions.AuthenticationFailed('User not found!')

    if not user.check_password(password):
        raise exceptions.AuthenticationFailed('Incorrect Password!')

    response = Response()

    token = generate_access_token(user)
    response.set_cookie(key='jwt', value=token, httponly=True)
    response.data = {
        'jwt': token
    }

    return response


@api_view(['POST'])
def logout(_):
    response = Response()
    response.delete_cookie(key='jwt')
    response.data = {
        'message': 'Success'
    }
    return response



class AuthenticatedUser(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = CurrentUserSerializer(request.user).data
        return Response({
            'data': data
        })

        
class PermissionApiView(ListAPIView):
    serializer_class = PermissionSerializer
    queryset = Permission.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated ]


class RoleViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated & ViewPermissions]
    permission_object = 'roles'
    serializer_class = RoleSerializer
    queryset = Role.objects.all()

class UserGenericAPIView(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated & ViewPermissions]
    pagination_class = CustomPagination
    permission_object = 'roles'
    serializer_class = CurrentUserSerializer
    queryset = User.objects.all()
    
    def get_queryset(self,*args,**kwargs):
        queryset = User.objects.all()
        query = self.request.query_params.dict()
        keyword = query.get("keyword",None)
        if keyword:
            queryset =  queryset.filter(
                Q(first_name__icontains=keyword) |
                 Q(last_name__icontains=keyword) |
                 Q(email__icontains=keyword )
                 
                )
        return queryset

    @action(detail=True, methods=['get'])
    def roles(self,request,pk=None):
        email = self.get_object()
        user = User.objects.get(email=email)
        roles = user.role
        serializer = RoleSerializer(roles)
        return Response(serializer.data)

    def create(self,request,*args,**kwargs):
        data = request.data
        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']
        password = "182blink"
        role= data['role']
        new_user = User(
            first_name=first_name,last_name=last_name,
            email=email,password=password,
            role=Role.objects.get(id=role)
            )
        new_user.set_password(password)
        new_user.save()
        serializer = UserSerializer(new_user)
        return Response(serializer.data)
    
    def update(self,request,*args,**kwargs):
        data = request.data
        email = data['email']
        password = "182blink"
        role = data['role']
        pk = self.get_object()
        user = User.objects.get(email = pk)
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.email = email
        user.role = Role.objects.get(id=role)
        user.set_password(password)
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data)


class ProfileUpdateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated ]

    def put(self, request , pk=None):
        user = request.user
        serializer = UserSerializer(user, data=request.data , partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class ProfilePasswordAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, pk=None):
        user = request.user

        if len(request.data['password']) < 6:
            raise exceptions.ValidationError({'len':'Passwords must be larger than 6 letters !'})

        if not user.check_password(request.data['old_password']):
            raise exceptions.AuthenticationFailed({'old':'Incorrect Password!'})
        
        if request.data['password'] != request.data['password_confirm']:
            raise exceptions.ValidationError({'new':'Passwords do not match  !'})

        user.set_password(request.data['password'])
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data)