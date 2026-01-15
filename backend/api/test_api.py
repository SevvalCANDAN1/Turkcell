# test_api.py - Manual API testing script
"""import requests
import json
from datetime import datetime

BASE_URL = 'http://localhost:8000/api'

def test_api():
    print("=" * 60)
    print("TURKCELL SERVICE QUALITY MONITOR - API TEST")
    print("=" * 60)
    
    # Test 1: Get all services
    print("\n[TEST 1] GET /services/")
    response = requests.get(f'{BASE_URL}/services/')
    services = response.json()
    print(f"✓ Services: {len(services)} found")
    if services:
        print(f"  Example: {services[0]['name']}")
    
    # Test 2: Get all rules
    print("\n[TEST 2] GET /rules/")
    response = requests.get(f'{BASE_URL}/rules/')
    rules = response.json()
    print(f"✓ Rules: {len(rules.get('results', rules))} found")
    
    # Test 3: Create a metric (will trigger rule engine)
    if services:
        print("\n[TEST 3] POST /metrics/ - Create metric")
        service_id = services[0]['id']
        metric_data = {
            'service': service_id,
            'metric_type': 'LATENCY_MS',
            'value': 180  # This should trigger rule if threshold is 150
        }
        response = requests.post(f'{BASE_URL}/metrics/', json=metric_data)
        if response.status_code == 201:
            print("✓ Metric created successfully")
            print(f"  Value: {response.json()['value']}")
        else:
            print(f"✗ Error: {response.status_code}")
    
    # Test 4: Get incidents
    print("\n[TEST 4] GET /incidents/")
    response = requests.get(f'{BASE_URL}/incidents/')
    incidents = response.json()
    incident_list = incidents.get('results', incidents)
    print(f"✓ Incidents: {len(incident_list)} found")
    if incident_list:
        incident = incident_list[0]
        print(f"  Service: {incident['service_name']}")
        print(f"  Status: {incident['status']}")
        print(f"  Priority: {incident['priority']}")
    
    # Test 5: Create quality rule
    print("\n[TEST 5] POST /rules/ - Create new rule")
    rule_data = {
        'metric_type': 'PACKET_LOSS',
        'threshold': 1.5,
        'operator': '>',
        'priority': 1,
        'is_active': True
    }
    response = requests.post(f'{BASE_URL}/rules/', json=rule_data)
    if response.status_code == 201:
        print("✓ Rule created successfully")
        rule = response.json()
        print(f"  Condition: {rule['metric_type_name']} {rule['operator']} {rule['threshold']}")
    else:
        print(f"✗ Error: {response.status_code}")
    
    # Test 6: Get audit logs
    print("\n[TEST 6] GET /audit-logs/")
    response = requests.get(f'{BASE_URL}/audit-logs/?limit=10')
    audit_logs = response.json()
    log_list = audit_logs.get('results', audit_logs)
    print(f"✓ Audit logs: {len(log_list)} found")
    for log in log_list[:3]:
        print(f"  {log['action_type']} at {log['timestamp']}")
    
    print("\n" + "=" * 60)
    print("API TESTS COMPLETED")
    print("=" * 60)

if __name__ == '__main__':
    test_api()"""
import requests
import json

# API adresimiz (Services)
url = "http://localhost:8000/api/services/"

try:
    print(f"📡 İstek gönderiliyor: {url}")
    
    # İsteği yapıyoruz (GET request)
    response = requests.get(url)
    
    # Durum kodunu kontrol et (200 OK ise başarılıdır)
    if response.status_code == 200:
        data = response.json() # Gelen cevabı JSON formatına çevir
        
        print("\n✅ BAŞARILI! İşte veritabanındaki servisler:\n")
        
        # Gelen veriyi (results kısmını) ekrana güzelce yazdıralım
        # DRF yapısında veriler genellikle 'results' anahtarı içinde gelir
        services = data.get('results', data) 
        
        for service in services:
            print(f"🔹 Servis: {service['name']}")
            print(f"   Açıklama: {service['description']}")
            print("-" * 30)
            
    else:
        print(f"❌ Hata oluştu! Kod: {response.status_code}")

except Exception as e:
    print(f"❌ Bir şeyler ters gitti: {e}")