# urls.py (Main)
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import (
    ServiceViewSet, MetricViewSet, MetricTypeViewSet,
    QualityRuleViewSet, IncidentViewSet, AuditLogViewSet
)

router = DefaultRouter()
router.register(r'services', ServiceViewSet, basename='service')
router.register(r'metrics', MetricViewSet, basename='metric')
router.register(r'metric-types', MetricTypeViewSet, basename='metric-type')
router.register(r'rules', QualityRuleViewSet, basename='rule')
router.register(r'incidents', IncidentViewSet, basename='incident')
router.register(r'audit-logs', AuditLogViewSet, basename='audit-log')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
