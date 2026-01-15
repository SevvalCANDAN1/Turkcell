from rest_framework import serializers
from .models import Service, Metric, MetricType, QualityRule, Incident, AuditLog


class ServiceSerializer(serializers.ModelSerializer):
    incident_count = serializers.SerializerMethodField()
    open_incident_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Service
        fields = ['id', 'name', 'description', 'incident_count', 'open_incident_count', 'created_at']
    
    def get_incident_count(self, obj):
        return obj.incidents.count()
    
    def get_open_incident_count(self, obj):
        return obj.incidents.filter(status='OPEN').count()


class MetricTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetricType
        fields = ['name', 'unit']


class MetricSerializer(serializers.ModelSerializer):
    metric_type_name = serializers.CharField(source='metric_type.name', read_only=True)
    service_name = serializers.CharField(source='service.name', read_only=True)
    
    class Meta:
        model = Metric
        fields = ['id', 'service', 'service_name', 'metric_type', 'metric_type_name', 'value', 'timestamp']
    
    def create(self, validated_data):
        metric = super().create(validated_data)
        from .rule_engine import check_rules
        check_rules(metric)
        return metric


class QualityRuleSerializer(serializers.ModelSerializer):
    metric_type_name = serializers.CharField(source='metric_type.name', read_only=True)
    trigger_count = serializers.SerializerMethodField()
    
    class Meta:
        model = QualityRule
        fields = ['id', 'metric_type', 'metric_type_name', 'threshold', 'operator', 'priority', 'is_active', 'trigger_count', 'created_at', 'updated_at']
    
    def get_trigger_count(self, obj):
        return obj.incidents.count()


class IncidentSerializer(serializers.ModelSerializer):
    service_name = serializers.CharField(source='service.name', read_only=True)
    rule_details = QualityRuleSerializer(source='rule', read_only=True)
    metric_value = serializers.FloatField(source='metric.value', read_only=True)
    
    class Meta:
        model = Incident
        fields = ['id', 'service', 'service_name', 'rule', 'rule_details', 'metric_value', 'status', 'priority', 'created_at', 'updated_at', 'closed_at']


class AuditLogSerializer(serializers.ModelSerializer):
    service_name = serializers.CharField(source='service.name', read_only=True, allow_null=True)
    
    class Meta:
        model = AuditLog
        fields = ['id', 'action_type', 'service', 'service_name', 'details', 'timestamp']