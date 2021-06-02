from django.urls import path
from .views import (
   register,users,
   login,logout,
   AuthenticatedUser,RoleViewSet,
   UserGenericAPIView
   )
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'roles', RoleViewSet)
router.register(r'users', UserGenericAPIView)
urlpatterns = [
   path('' , users),
   path('register/' , register),
   path('login/' , login),
   path('logout/' , logout),
   path('currentuser/' , AuthenticatedUser.as_view()),

]
urlpatterns += router.urls