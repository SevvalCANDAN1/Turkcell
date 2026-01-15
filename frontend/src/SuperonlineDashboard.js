import React, { useState, useEffect } from "react";
import axios from "axios";
import "./Superonline.css"; 

function SuperonlineDashboard({ onBack }) {
  const [service, setService] = useState(null);
  const [metrics, setMetrics] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // 1. Servisleri Çek
        const serviceRes = await axios.get("http://localhost:8000/api/services/");
        const allServices = serviceRes.data.results || serviceRes.data;
        
        // "Superonline" servisini bul
        const soData = allServices.find(s => s.name === "Superonline");
        
        if (soData) {
          setService(soData);

          // 2. Metrikleri Çek
          const metricsRes = await axios.get("http://localhost:8000/api/metrics/");
          const allMetrics = metricsRes.data.results || metricsRes.data;
          
          // Superonline metriklerini filtrele ve tarihe göre sırala (Yeniden eskiye)
          const soMetrics = allMetrics
            .filter(m => m.service === soData.id || m.service.id === soData.id)
            .sort((a, b) => new Date(b.created_at) - new Date(a.created_at));

          setMetrics(soMetrics);
        }
        setLoading(false);
      } catch (error) {
        console.error("Superonline verisi hatası:", error);
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  // Yükleme Ekranı (Tasarımına uygun koyu renk)
  if (loading) return <div style={{background:'#001a3d', color:'white', height:'100vh', display:'flex', justifyContent:'center', alignItems:'center'}}>Veriler Yükleniyor...</div>;
  
  // Hata Ekranı
  if (!service) return (
    <div style={{background:'#001a3d', color:'white', height:'100vh', display:'flex', flexDirection:'column', justifyContent:'center', alignItems:'center'}}>
      <h2>Superonline Servisi Bulunamadı!</h2>
      <button onClick={onBack} style={{marginTop:'20px', padding:'10px', cursor:'pointer'}}>Geri Dön</button>
    </div>
  );

  // --- HESAPLAMALAR ---
  // Belirli bir metrik tipinin en güncel değerini getiren fonksiyon
  const getValue = (type, defaultValue = 0) => {
    const metric = metrics.find(m => m.metric_type === type);
    return metric ? metric.value : defaultValue;
  };

  // Dinamik Verilerle Stats Dizisi
  // Not: Veritabanında DOWNLOAD_SPEED veya ERROR_RATE yoksa varsayılan değerleri gösterir.
  const stats = [
    { 
      label: "BUFFER ORANI", // Bunu 'DOWNLOAD_SPEED' olarak eşleştirdim (Mbps olduğu için)
      value: getValue('DOWNLOAD_SPEED', 940.5), 
      unit: "Mbps", 
      icon: "🚀" 
    },
    { 
      label: "PAKET KAYBI", 
      value: getValue('PACKET_LOSS', 0.0), 
      unit: "%", 
      icon: "📤" 
    },
    { 
      label: "GECİKME", 
      value: getValue('LATENCY_MS', 4), 
      unit: "ms", 
      icon: "⚡" 
    },
    { 
      label: "HATA ORANI", 
      value: getValue('ERROR_RATE', 0.01), 
      unit: "%", 
      icon: "⚠️" 
    },
  ];

  return (
    <div className="so-wrapper">
      {/* ÜST NAVİGASYON */}
      <nav className="so-header-nav">
        <div className="so-nav-left">
          <span className="so-logo-text">SUPERONLINE</span>
          {/* Servis Durumunu Logo Yanına Küçük Bir Badge Olarak Ekleyebiliriz */}
          <span style={{ 
              marginLeft: '15px', 
              fontSize: '10px', 
              background: service.open_incident_count > 0 ? '#ff4d4f' : '#39ff14',
              color: service.open_incident_count > 0 ? 'white' : 'black',
              padding: '2px 8px',
              borderRadius: '10px',
              fontWeight: 'bold'
          }}>
            {service.open_incident_count > 0 ? 'BAKIMDA' : 'ONLINE'}
          </span>
        </div>
        
        <button className="so-back-portal-btn" onClick={onBack}>
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" style={{marginRight: '8px'}}>
            <path d="M19 12H5M12 19l-7-7 7-7"/>
          </svg>
          PORTALA DÖN
        </button>
      </nav>

      {/* ANA İÇERİK */}
      <main className="so-main-content">
        <div className="so-content-center">
          <header className="so-welcome">
            <h1>Superonline Paneli</h1>
            <p>
                Müşteri ID: 85024419 | Paket: Işık Hızı Fiber | 
                Son Güncelleme: {new Date().toLocaleTimeString('tr-TR')}
            </p>
          </header>

          <div className="so-stats-grid">
            {stats.map((item, index) => (
              <div key={index} className="so-stat-card">
                <div className="so-stat-icon">{item.icon}</div>
                <div className="so-stat-info">
                  <label>{item.label}</label>
                  <div className="so-stat-value">
                    {/* Veri ve Birim Ayrımı */}
                    {item.value} <span className="so-unit">{item.unit}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </main>
    </div>
  );
}

export default SuperonlineDashboard;