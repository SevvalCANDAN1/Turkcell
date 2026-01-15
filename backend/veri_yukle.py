import os
import django
from django.utils import timezone
from django.db import transaction

# --- AYARLAR ---
# Buraya uygulama adınızı yazın (klasör adı)
APP_NAME = 'api' 

# Modelleri dinamik olarak import ediyoruz
from django.apps import apps
Service = apps.get_model(APP_NAME, 'Service')
MetricType = apps.get_model(APP_NAME, 'MetricType')
Metric = apps.get_model(APP_NAME, 'Metric')
QualityRule = apps.get_model(APP_NAME, 'QualityRule')
Incident = apps.get_model(APP_NAME, 'Incident')

def run():
    print("Veri ekleme işlemi başlıyor...")
    
    with transaction.atomic():
        # --- 0. METRIC TYPE ---
        print("- Metrik Tipleri oluşturuluyor...")
        mt_latency, _ = MetricType.objects.get_or_create(name='LATENCY_MS', defaults={'unit': 'ms'})
        mt_packet, _ = MetricType.objects.get_or_create(name='PACKET_LOSS', defaults={'unit': '%'})
        mt_buffer, _ = MetricType.objects.get_or_create(name='BUFFER_RATIO', defaults={'unit': '%'})
        mt_error, _ = MetricType.objects.get_or_create(name='ERROR_RATE', defaults={'unit': '%'})

        mt_map = {
            'LATENCY_MS': mt_latency,
            'PACKET_LOSS': mt_packet,
            'BUFFER_RATIO': mt_buffer,
            'ERROR_RATE': mt_error
        }

        # --- 1. SERVICES ---
        print("- Servisler oluşturuluyor...")
        service_map = {}
        
        # get_or_create kullanarak tekrar çalıştırıldığında hata vermesini engelliyoruz
        s1, _ = Service.objects.get_or_create(name='Superonline', defaults={'description': 'Fiber Internet'})
        service_map['S1'] = s1
        
        s2, _ = Service.objects.get_or_create(name='TV+', defaults={'description': 'IPTV Service'})
        service_map['S2'] = s2
        
        s3, _ = Service.objects.get_or_create(name='Paycell', defaults={'description': 'Payment System'})
        service_map['S3'] = s3

        # --- 2. QUALITY RULES ---
        print("- Kalite Kuralları oluşturuluyor...")
        rule_map = {}

        qr1, _ = QualityRule.objects.get_or_create(
            metric_type=mt_map['LATENCY_MS'], 
            operator='>', 
            defaults={'threshold': 150.0, 'priority': 1, 'is_active': True}
        )
        rule_map['QR-01'] = qr1

        qr2, _ = QualityRule.objects.get_or_create(
            metric_type=mt_map['PACKET_LOSS'], 
            operator='>', 
            defaults={'threshold': 1.5, 'priority': 2, 'is_active': True}
        )
        rule_map['QR-02'] = qr2

        qr3, _ = QualityRule.objects.get_or_create(
            metric_type=mt_map['BUFFER_RATIO'], 
            operator='>', 
            defaults={'threshold': 6.0, 'priority': 2, 'is_active': True}
        )
        rule_map['QR-03'] = qr3

        # --- 3. METRICS ---
        print("- Metrikler giriliyor...")
        metric_map = {}

        m1 = Metric.objects.create(service=service_map['S1'], metric_type=mt_map['LATENCY_MS'], value=180.0)
        metric_map['M1'] = m1
        
        Metric.objects.create(service=service_map['S1'], metric_type=mt_map['PACKET_LOSS'], value=2.1)
        
        m3 = Metric.objects.create(service=service_map['S2'], metric_type=mt_map['BUFFER_RATIO'], value=7.5)
        metric_map['M3'] = m3
        
        Metric.objects.create(service=service_map['S3'], metric_type=mt_map['ERROR_RATE'], value=1.9)

        # --- 4. INCIDENTS ---
        print("- Olaylar (Incidents) oluşturuluyor...")
        
        Incident.objects.create(
            service=service_map['S1'],
            rule=rule_map['QR-01'],
            metric=metric_map['M1'],
            priority=1,
            status='OPEN'
        )

        Incident.objects.create(
            service=service_map['S2'],
            rule=rule_map['QR-03'],
            metric=metric_map['M3'],
            priority=2,
            status='OPEN'
        )

    print("\n✅ İŞLEM BAŞARIYLA TAMAMLANDI!")