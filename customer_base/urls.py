from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from core.views import CustomerViewSet, ProfessionViewSet

router = routers.DefaultRouter()
router.register(r'customers', CustomerViewSet, basename='customers')
router.register(r'professions', ProfessionViewSet, basename='professions')


urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
]

