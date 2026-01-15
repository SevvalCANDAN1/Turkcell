import React, { useState, useEffect } from "react";
import axios from "axios";
import "./Paycell.css";

function PaycellDashboard({ onBack }) {
  const [service, setService] = useState(null);
  const [incidents, setIncidents] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // 1. Tüm servisleri çek ve Paycell'i bul
        const serviceRes = await axios.get("http://localhost:8000/api/services/");
        const allServices = serviceRes.data.results || serviceRes.data;
        const paycellData = allServices.find(s => s.name === "Paycell");

        if (paycellData) {
          setService(paycellData);

          // 2. Olayları (Incidents) çek ve Paycell'e ait olanları filtrele
          const incidentsRes = await axios.get("http://localhost:8000/api/incidents/");
          const allIncidents = incidentsRes.data.results || incidentsRes.data;
          
          // ID eşleşmesine göre filtrele
          const paycellIncidents = allIncidents.filter(
            inc => inc.service === paycellData.id || inc.service.id === paycellData.id
          );
          
          setIncidents(paycellIncidents);
        }
        setLoading(false);
      } catch (error) {
        console.error("Paycell verisi çekilemedi:", error);
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  // Tarih formatlayıcı
  const formatDate = (dateString) => {
    if (!dateString) return "-";
    const date = new Date(dateString);
    return date.toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' }) + " " + date.toLocaleDateString('tr-TR');
  };

  // Eğer veri henüz gelmediyse yükleniyor göster (Tasarımı bozmadan basitçe)
  if (loading) return <div className="pay-dashboard-wrapper" style={{color:'white', padding:'20px'}}>Yükleniyor...</div>;
  if (!service) return <div className="pay-dashboard-wrapper" style={{color:'white', padding:'20px'}}>Paycell servisi veritabanında bulunamadı!</div>;

  // --- GERÇEK VERİTABANI VERİLERİ ---
  // Eski "Cüzdan Bakiyesi" yerine veritabanındaki gerçek istatistikleri koyuyoruz.
  const stats = [
    { 
      label: "Servis Durumu", 
      value: service.open_incident_count > 0 ? "Sorun Var" : "Aktif", 
      icon: service.open_incident_count > 0 ? "⚠️" : "✅" 
    },
    { 
      label: "Aktif Olaylar", 
      value: `${service.open_incident_count} Adet`, 
      icon: "🔥" 
    },
    { 
      label: "Toplam Kayıt", 
      value: `${service.incident_count} Olay`, 
      icon: "📋" 
    },
    { 
      label: "Son Güncelleme", 
      value: new Date(service.updated_at).toLocaleDateString('tr-TR'), 
      icon: "📅" 
    }
  ];

  return (
    <div className="pay-dashboard-wrapper">
      {/* Üst Navigasyon */}
      <nav className="pay-nav">
        <div className="pay-brand-group">
          <span className="pay-brand">PAYCELL</span>
          <span className="pay-status-badge">
             {service.open_incident_count > 0 ? "KESİNTİ VAR" : "SİSTEM ONLİNE"}
          </span>
        </div>
        <button className="pay-back-button" onClick={onBack}>Portal Ana Menü</button>
      </nav>

      <div className="pay-container">
        <header className="pay-header">
          <h1>Servis Sağlık Durumu</h1>
          <p>Rapor Zamanı: {new Date().toLocaleDateString('tr-TR')} | İstanbul, TR</p>
        </header>

        {/* İstatistik Kartları (Artık DB'den geliyor) */}
        <div className="pay-grid">
          {stats.map((stat, index) => (
            <div key={index} className="pay-card">
              <span className="pay-card-icon">{stat.icon}</span>
              <div className="pay-card-data">
                <label>{stat.label}</label>
                <strong>{stat.value}</strong>
              </div>
            </div>
          ))}
        </div>

        {/* Alt Panel: Son Olaylar (Eski Transaction Listesi Yerine) */}
        <div className="pay-main-grid">
          <div className="pay-transactions-section">
            <h3>Son Sistem Olayları (Incidents)</h3>
            
            <div className="pay-transaction-list">
              {incidents.length === 0 ? (
                 <div className="tx-item">
                    <div className="tx-info"><strong>Henüz kayıtlı bir olay yok.</strong></div>
                 </div>
              ) : (
                incidents.map((inc) => (
                  <div key={inc.id} className="tx-item">
                    <div className="tx-info">
                      <strong>{inc.description}</strong>
                      <span>{formatDate(inc.created_at)}</span>
                    </div>
                    {/* Priority (Öncelik) değerine göre renk verelim */}
                    <div className={`tx-amount`} style={{ 
                        color: inc.priority === 'CRITICAL' || inc.priority === 'HIGH' ? '#ff4d4f' : '#52c41a',
                        fontWeight: 'bold'
                    }}>
                      {inc.priority}
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
          
          <div className="pay-actions">
            <h3>Hızlı İşlemler</h3>
            <button className="pay-action-btn primary">Rapor Oluştur</button>
            <button className="pay-action-btn">Ekibe Bildir</button>
            <button className="pay-action-btn">Logları İncele</button>
            <div className="pay-info-box">
              <small>Sistem logları her 5 dakikada bir veritabanına işlenmektedir.</small>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default PaycellDashboard;