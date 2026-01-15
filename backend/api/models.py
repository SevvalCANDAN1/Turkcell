from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
import uuid

class Service(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name

class MetricType(models.Model):
    METRIC_CHOICES = [
        ('LATENCY_MS', 'Latency (ms)'),
        ('PACKET_LOSS', 'Packet Loss (%)'),
        ('ERROR_RATE', 'Error Rate (%)'),
        ('BUFFER_RATE', 'Buffer Rate (%)'),
    ]
    
    name = models.CharField(max_length=50, choices=METRIC_CHOICES, unique=True)
    unit = models.CharField(max_length=20)
    
    def __str__(self):
        return self.name

class Metric(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='metrics')
    metric_type = models.ForeignKey(MetricType, on_delete=models.CASCADE)
    value = models.FloatField(validators=[MinValueValidator(0)])
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['service', '-timestamp']),
        ]
    
    def __str__(self):
        return f"{self.service.name} - {self.metric_type.name}: {self.value}"

class QualityRule(models.Model):
    OPERATOR_CHOICES = [
        ('>', 'Greater Than'),
        ('<', 'Less Than'),
        ('>=', 'Greater or Equal'),
        ('<=', 'Less or Equal'),
        ('==', 'Equal'),
    ]
    
    PRIORITY_CHOICES = [
        (1, 'Critical'),
        (2, 'High'),
        (3, 'Medium'),
        (4, 'Low'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    metric_type = models.ForeignKey(MetricType, on_delete=models.CASCADE)
    threshold = models.FloatField(validators=[MinValueValidator(0)])
    operator = models.CharField(max_length=2, choices=OPERATOR_CHOICES)
    priority = models.IntegerField(choices=PRIORITY_CHOICES)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['priority', '-created_at']
    
    def __str__(self):
        return f"{self.metric_type.name} {self.operator} {self.threshold}"
    
    def check_violation(self, value):
        """Check if metric value violates this rule"""
        if not self.is_active:
            return False
        
        if self.operator == '>':
            return value > self.threshold
        elif self.operator == '<':
            return value < self.threshold
        elif self.operator == '>=':
            return value >= self.threshold
        elif self.operator == '<=':
            return value <= self.threshold
        elif self.operator == '==':
            return value == self.threshold
        return False

class Incident(models.Model):
    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('IN_PROGRESS', 'In Progress'),
        ('CLOSED', 'Closed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='incidents')
    rule = models.ForeignKey(QualityRule, on_delete=models.CASCADE, related_name='incidents')
    metric = models.ForeignKey(Metric, on_delete=models.CASCADE, related_name='incident')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')
    priority = models.IntegerField(choices=QualityRule.PRIORITY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['service', '-created_at']),
            models.Index(fields=['status', '-created_at']),
        ]
    
    def __str__(self):
        return f"Incident {self.service.name} - {self.status}"

class AuditLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    action_type = models.CharField(max_length=50)  # METRIC_RECEIVED, RULE_TRIGGERED, INCIDENT_CREATED, etc.
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)
    incident = models.ForeignKey(Incident, on_delete=models.SET_NULL, null=True, blank=True)
    details = models.JSONField(default=dict)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp']),
        ]