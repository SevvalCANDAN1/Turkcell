from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Count
from .models import Service, Metric, MetricType, QualityRule, Incident, AuditLog
from .serializers import (
    ServiceSerializer, MetricSerializer, MetricTypeSerializer,
    QualityRuleSerializer, IncidentSerializer, AuditLogSerializer
)


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.prefetch_related('incidents', 'metrics')
    serializer_class = ServiceSerializer
    
    @action(detail=True, methods=['get'])
    def latest_metrics(self, request, pk=None):
        service = self.get_object()
        latest_metrics = Metric.objects.filter(service=service).order_by('metric_type', '-timestamp').distinct('metric_type')
        serializer = MetricSerializer(latest_metrics, many=True)
        return Response(serializer.data)


class MetricViewSet(viewsets.ModelViewSet):
    queryset = Metric.objects.select_related('service', 'metric_type')
    serializer_class = MetricSerializer
    
    @action(detail=False, methods=['get'])
    def by_service(self, request):
        service_id = request.query_params.get('service_id')
        metric_type = request.query_params.get('metric_type')
        
        queryset = Metric.objects.select_related('service', 'metric_type')
        if service_id:
            queryset = queryset.filter(service_id=service_id)
        if metric_type:
            queryset = queryset.filter(metric_type__name=metric_type)
        
        serializer = MetricSerializer(queryset[:100], many=True)
        return Response(serializer.data)


class MetricTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MetricType.objects.all()
    serializer_class = MetricTypeSerializer


class QualityRuleViewSet(viewsets.ModelViewSet):
    queryset = QualityRule.objects.select_related('metric_type')
    serializer_class = QualityRuleSerializer
    
    @action(detail=False, methods=['get'])
    def most_triggered(self, request):
        rules = QualityRule.objects.annotate(
            incident_count=Count('incidents')
        ).order_by('-incident_count')[:10]
        serializer = QualityRuleSerializer(rules, many=True)
        return Response(serializer.data)


class IncidentViewSet(viewsets.ModelViewSet):
    queryset = Incident.objects.select_related('service', 'rule', 'metric')
    serializer_class = IncidentSerializer
    
    @action(detail=True, methods=['patch'])
    def close(self, request, pk=None):
        incident = self.get_object()
        incident.status = 'CLOSED'
        incident.closed_at = timezone.now()
        incident.save()
        
        AuditLog.objects.create(
            action_type='INCIDENT_CLOSED',
            incident=incident,
            service=incident.service,
            details={'closed_by': request.user.username if request.user else 'system'}
        )
        
        return Response(IncidentSerializer(incident).data)
    
    @action(detail=False, methods=['get'])
    def open_incidents(self, request):
        service_id = request.query_params.get('service_id')
        queryset = Incident.objects.filter(status='OPEN')
        if service_id:
            queryset = queryset.filter(service_id=service_id)
        
        serializer = IncidentSerializer(queryset, many=True)
        return Response(serializer.data)


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.select_related('service')
    serializer_class = AuditLogSerializer