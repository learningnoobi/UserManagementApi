from django.urls import path
from .views import (
   register,users,
   login,logout,
   AuthenticatedUser,RoleViewSet,
   UserGenericAPIView,PermissionApiView,
   ProfileUpdateView,ProfilePasswordAPIView
   )
from rest_framework import routers

#for viewsets
router = routers.DefaultRouter()
router.register(r'roles', RoleViewSet)
router.register(r'users', UserGenericAPIView)

#normal routes
urlpatterns = [
   path('' , users),
   path('register/' , register),
   path('login/' , login),
   path('logout/' , logout),
   path('permissions/' , PermissionApiView.as_view()),
   path('currentuser/' , AuthenticatedUser.as_view()),
   path('updateprofile/' , ProfileUpdateView.as_view()),
   path('updatepassword/' , ProfilePasswordAPIView.as_view()),

]

#combining viewsets routers and normal urlpatterns
urlpatterns += router.urls