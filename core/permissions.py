from rest_framework import permissions

from .serializers import UserSerializer,CurrentUserSerializer

class ViewPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        data = CurrentUserSerializer(request.user).data
        
        if not data.get("role") is None:
            view_access = any(p['name'] == 'view_' + view.permission_object for p in data['role']['permissions'])
            edit_access = any(p['name'] == 'edit_' + view.permission_object for p in data['role']['permissions'])

            if request.method == 'GET':
                return view_access or edit_access

        
            return edit_access