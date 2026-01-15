import React, { useState, useEffect } from "react";
import axios from "axios";
import "./TVPlus.css"; // CSS dosyanın import edildiğinden emin ol

function TVPlusDashboard({ onBack }) {
  const [service, setService] = useState(null);
  const [metrics, setMetrics] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // 1. Backend'den Servis Listesini Çek
        const serviceRes = await axios.get("http://localhost:8000/api/services/");
        const allServices = serviceRes.data.results || serviceRes.data;
        
        // "TV+" veya "TVPlus" ismine sahip servisi bul
        const tvData = allServices.find(s => s.name === "TV+" || s.name === "TVPlus");

        if (tvData) {
          setService(tvData);

          // 2. Metrikleri Çek
          const metricsRes = await axios.get("http://localhost:8000/api/metrics/");
          const allMetrics = metricsRes.data.results || metricsRes.data;
          
          // Sadece TV+'a ait metrikleri filtrele ve tarihe göre (Yeniden Eskiye) sırala
          const tvMetrics = allMetrics
            .filter(m => m.service === tvData.id || m.service.id === tvData.id)
            .sort((a, b) => new Date(b.created_at) - new Date(a.created_at));

          setMetrics(tvMetrics);
        }
        setLoading(false);
      } catch (error) {
        console.error("TV+ verisi çekilemedi:", error);
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  // Yükleme Ekranı
  if (loading) return <div style={{background:'#001a3d', color:'white', height:'100vh', display:'flex', justifyContent:'center', alignItems:'center'}}>Yükleniyor...</div>;
  
  // Servis Bulunamadı Ekranı
  if (!service) return (
    <div style={{background:'#001a3d', color:'white', height:'100vh', display:'flex', flexDirection:'column', justifyContent:'center', alignItems:'center'}}>
      <h2>TV+ Servisi Bulunamadı!</h2>
      <button onClick={onBack} style={{marginTop:'20px', padding:'10px', cursor:'pointer'}}>Geri Dön</button>
    </div>
  );

  // --- HESAPLAMALAR ---
  // Backend'den gelen metrik tiplerine göre en güncel değeri buluyoruz.
  // Eğer o tipte veri yoksa 0 veya "-" gösteriyoruz.
  const getValue = (type) => {
    const metric = metrics.find(m => m.metric_type === type);
    return metric ? metric.value : 0;
  };

  // TV+ Özel Verileri (Backend'e Bağlı)
  const stats = [
    { 
      label: "BUFFER ORANI", 
      value: getValue('BUFFER_RATE'), 
      unit: "%", // Birim eklendi
      icon: "📺" 
    },
    { 
      label: "PAKET KAYBI", 
      value: getValue('PACKET_LOSS'), 
      unit: "%",
      icon: "💾" 
    },
    { 
      label: "GECİKME", 
      value: getValue('LATENCY_MS'), 
      unit: "ms",
      icon: "📱" 
    },
    { 
      label: "HATA ORANI", 
      value: getValue('ERROR_RATE'), 
      unit: "%", // Hata oranı genelde yüzde olur veya adet ise incident count alabiliriz
      icon: "🎟️" 
    }
  ];

  return (
    <div className="tvp-dashboard-wrapper">
      {/* Üst Navigasyon */}
      <nav className="tvp-nav">
        <div className="tvp-brand-group">
          <span className="tvp-brand">TV+</span>
          {/* Status Badge: Sorun varsa Kırmızı, yoksa Yeşil/Mavi */}
          <span className="tvp-status-badge" style={{ backgroundColor: service.open_incident_count > 0 ? '#ff4d4f' : '#00b894' }}>
            {service.open_incident_count > 0 ? 'BAKIM MODU' : '4K ULTRA HD'}
          </span>
        </div>
        <button className="tvp-back-button" onClick={onBack}>Portal Ana Menü</button>
      </nav>

      {/* İçerik Alanı - Class isimlerini senin verdiğin gibi korudum */}
      <main className="so-main-content">
        <div className="so-content-center">
          <header className="so-welcome">
            {/* Başlık Dinamikleşti */}
            <h1>TV+ Performans Paneli</h1>
            <p>
                Durum: {service.open_incident_count > 0 ? "⚠️ Servis İnceleniyor" : "✅ Yayın Stabil"} | 
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
                    {/* Değer ve Birimi Yan Yana Getirdik */}
                    {item.value} <span className="so-unit" style={{fontSize:'0.6em', color:'#aaa'}}>{item.unit}</span>
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

export default TVPlusDashboard;