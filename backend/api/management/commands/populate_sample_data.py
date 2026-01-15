# management/commands/populate_sample_data.py
# Place this in: api/management/commands/populate_sample_data.py

import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from api.models import Service, MetricType, Metric, QualityRule, AuditLog

class Command(BaseCommand):
    help = 'Populate database with sample data for testing'

    def handle(self, *args, **options):
        # Create services
        services_data = ['Superonline', 'TV+', 'Paycell', 'Mobil']
        services = []
        for name in services_data:
            service, _ = Service.objects.get_or_create(
                name=name,
                defaults={'description': f'{name} Service'}
            )
            services.append(service)
            self.stdout.write(f'✓ Service created: {name}')

        # Create metric types
        metric_types_data = [
            ('LATENCY_MS', 'ms'),
            ('PACKET_LOSS', '%'),
            ('ERROR_RATE', '%'),
            ('BUFFER_RATE', '%'),
        ]
        metric_types = []
        for name, unit in metric_types_data:
            mt, _ = MetricType.objects.get_or_create(
                name=name,
                defaults={'unit': unit}
            )
            metric_types.append(mt)
            self.stdout.write(f'✓ MetricType created: {name}')

        # Create quality rules
        rules_config = [
            ('LATENCY_MS', '>', 150, 1),      # Critical: Latency > 150ms
            ('PACKET_LOSS', '>', 2, 2),       # High: Packet loss > 2%
            ('ERROR_RATE', '>', 5, 2),        # High: Error rate > 5%
            ('BUFFER_RATE', '>', 10, 3),      # Medium: Buffer rate > 10%
        ]
        
        for metric_name, operator, threshold, priority in rules_config:
            metric_type = MetricType.objects.get(name=metric_name)
            rule, _ = QualityRule.objects.get_or_create(
                metric_type=metric_type,
                threshold=threshold,
                operator=operator,
                defaults={'priority': priority, 'is_active': True}
            )
            self.stdout.write(f'✓ Rule created: {metric_name} {operator} {threshold}')

        # Generate sample metrics
        self.stdout.write('\nGenerating sample metrics...')
        for _ in range(20):
            service = random.choice(services)
            metric_type = random.choice(metric_types)
            
            # Generate realistic values
            if metric_type.name == 'LATENCY_MS':
                value = random.uniform(50, 200)
            elif metric_type.name == 'PACKET_LOSS':
                value = random.uniform(0, 5)
            elif metric_type.name == 'ERROR_RATE':
                value = random.uniform(0, 10)
            else:  # BUFFER_RATE
                value = random.uniform(0, 15)
            
            metric = Metric.objects.create(
                service=service,
                metric_type=metric_type,
                value=value
            )
            self.stdout.write(f'  Metric: {service.name} - {metric_type.name}: {value:.2f}')

        self.stdout.write(self.style.SUCCESS('\n✓ Sample data population completed!'))


