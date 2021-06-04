from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import ProductGenericAPIView,FileUploadView

from rest_framework import routers
router = routers.DefaultRouter()
router.register(r'products', ProductGenericAPIView)

urlpatterns = [
     path('upload/', FileUploadView.as_view())

    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += router.urls