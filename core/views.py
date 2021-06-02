from rest_framework import exceptions, viewsets, status, generics, mixins
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from .serializers import *
from .models import User, Permission, Role
from .authentication import generate_access_token, JWTAuthentication



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
    if data["password"] != data["password_confirm"]:
        raise exceptions.APIException('Passwords do not match!')
    serializer = UserSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
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
        data = UserSerializer(request.user).data
        # if data['role'] is not None:
        # data['permissions'] = data['role']['permissions']
        return Response({
            'data': data
        })



class RoleViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated ]
    permission_object = 'roles'
    serializer_class = RoleSerializer
    queryset = Role.objects.all()

class UserGenericAPIView(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated ]
    permission_object = 'roles'
    serializer_class = UserSerializer
    queryset = User.objects.all()
    
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



