from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/' , include('core.urls')),
    path('pro/' , include('products.urls')),
    path('ord/' , include('orders.urls'))
]
