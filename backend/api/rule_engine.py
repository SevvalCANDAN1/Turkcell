from .models import QualityRule, Incident, AuditLog
from django.utils import timezone
import json

class RuleEngine:
    """Quality rule evaluation engine"""
    
    @staticmethod
    def check_rules(metric):
        """
        Check if the given metric violates any quality rules.
        If a rule is violated, create an incident.
        """
        rules = QualityRule.objects.filter(
            metric_type=metric.metric_type,
            is_active=True
        )
        
        violations = []
        
        for rule in rules:
            if rule.check_violation(metric.value):
                incident = RuleEngine.create_incident(metric, rule)
                violations.append(incident)
                RuleEngine.send_notification(incident)
                
                # Log the action
                AuditLog.objects.create(
                    action_type='RULE_TRIGGERED',
                    service=metric.service,
                    incident=incident,
                    details={
                        'rule_id': str(rule.id),
                        'metric_value': metric.value,
                        'threshold': rule.threshold,
                        'operator': rule.operator,
                    }
                )
        
        # Log metric receipt
        AuditLog.objects.create(
            action_type='METRIC_RECEIVED',
            service=metric.service,
            details={
                'metric_type': metric.metric_type.name,
                'value': metric.value,
                'violations_count': len(violations),
            }
        )
        
        return violations
    
    @staticmethod
    def create_incident(metric, rule):
        """Create an incident from a rule violation"""
        incident = Incident.objects.create(
            service=metric.service,
            rule=rule,
            metric=metric,
            status='OPEN',
            priority=rule.priority
        )
        return incident
    
    @staticmethod
    def send_notification(incident):
        """Send notification to ops team (mock)"""
        notification_data = {
            'target': 'OPS_TEAM',
            'message': f"{incident.service.name} - {incident.rule.metric_type.name} threshold exceeded.",
            'priority': incident.priority,
            'incident_id': str(incident.id),
            'service': incident.service.name,
            'metric_type': incident.rule.metric_type.name,
            'timestamp': timezone.now().isoformat(),
        }
        
        # Mock implementation - in real world, integrate with BiP/SMS/email
        print(f"[NOTIFICATION] {json.dumps(notification_data, indent=2)}")
        
        # Log notification
        AuditLog.objects.create(
            action_type='NOTIFICATION_SENT',
            service=incident.service,
            incident=incident,
            details=notification_data
        )

# Convenience function to be called from serializers
def check_rules(metric):
    return RuleEngine.check_rules(metric)