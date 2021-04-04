from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from core.views import (
    CustomerViewSet,
    ProfessionViewSet,
    DataSheetViewSet,
    DocumentViewSet,
)

router = routers.DefaultRouter()
router.register(r'customers', CustomerViewSet, basename='customers')
router.register(r'professions', ProfessionViewSet, basename='professions')
router.register(r'datasheets', DataSheetViewSet, basename='datasheets')
router.register(r'documents', DocumentViewSet, basename='documents')

urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-token-auth/', obtain_auth_token),
    path('api-auth/', include('rest_framework.urls')),
]
