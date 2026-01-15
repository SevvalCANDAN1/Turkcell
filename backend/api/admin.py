from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Service, MetricType, Metric, QualityRule, Incident, AuditLog


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'incident_count', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'description')
    readonly_fields = ('id', 'created_at')
    
    def incident_count(self, obj):
        return obj.incidents.count()
    incident_count.short_description = 'Open Incidents'


@admin.register(MetricType)
class MetricTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit')
    search_fields = ('name',)


@admin.register(Metric)
class MetricAdmin(admin.ModelAdmin):
    list_display = ('service', 'metric_type', 'value', 'timestamp')
    list_filter = ('metric_type', 'service', 'timestamp')
    search_fields = ('service__name',)
    readonly_fields = ('id', 'timestamp')
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return self.readonly_fields + ('service', 'metric_type', 'value')
        return self.readonly_fields


@admin.register(QualityRule)
class QualityRuleAdmin(admin.ModelAdmin):
    list_display = ('metric_type', 'operator', 'threshold', 'priority', 'is_active', 'trigger_count')
    list_filter = ('is_active', 'priority', 'metric_type', 'created_at')
    search_fields = ('metric_type__name',)
    readonly_fields = ('id', 'created_at', 'updated_at')
    fieldsets = (
        ('Rule Details', {
            'fields': ('metric_type', 'threshold', 'operator', 'priority')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def trigger_count(self, obj):
        return obj.incidents.count()
    trigger_count.short_description = 'Times Triggered'


@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    list_display = ('service', 'rule', 'status', 'priority', 'created_at', 'closed_at')
    list_filter = ('status', 'priority', 'service', 'created_at')
    search_fields = ('service__name',)
    readonly_fields = ('id', 'created_at', 'updated_at', 'rule', 'metric')
    fieldsets = (
        ('Incident Details', {
            'fields': ('service', 'rule', 'metric', 'status', 'priority')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'closed_at')
        }),
        ('ID', {
            'fields': ('id',),
            'classes': ('collapse',)
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return self.readonly_fields + ('service',)
        return self.readonly_fields


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('action_type', 'service', 'timestamp')
    list_filter = ('action_type', 'service', 'timestamp')
    search_fields = ('action_type', 'service__name')
    readonly_fields = ('id', 'timestamp', 'action_type', 'service', 'incident', 'details')
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False