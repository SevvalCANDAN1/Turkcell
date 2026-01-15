import React, { useState, useEffect } from "react";
import axios from "axios";
import "./Portal.css";

// Frontend tarafındaki Görsel Ayarlar (Logo ve Renk Temaları)
// Bu veriler veritabanında tutulmaz, o yüzden burada eşleştiriyoruz.
const serviceUIConfig = {
  "Superonline": {
    logo: '/img/superonline.png',
    themeClass: 'superonline-card',
    fallbackDesc: 'Işık hızında fiber internet deneyimi.'
  },
  "TV+": {
    logo: '/img/tv+.png',
    themeClass: 'tvplus-card',
    fallbackDesc: 'En sevdiğin filmler ve canlı yayınlar.'
  },
  "Paycell": {
    logo: '/img/paycell.jpg',
    themeClass: 'paycell-card',
    fallbackDesc: 'Harcadıkça kazandıran dijital cüzdan.'
  }
};

function Portal({ onSelectService, onLogout }) {
  const [services, setServices] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchServices = async () => {
      try {
        // Backend'den gerçek servis listesini çekiyoruz
        const response = await axios.get("http://localhost:8000/api/services/");
        const dbServices = response.data.results || response.data;
        
        // Veritabanından gelen veriyi, bizim UI config ile birleştiriyoruz
        // Sadece hem DB'de olan hem de Config'de tanımlı olanları listeliyoruz.
        const mergedServices = dbServices
          .filter(service => serviceUIConfig[service.name]) // Bilinmeyen servisleri gizle
          .map(service => ({
            ...service, // DB'deki id, name, description, incident_count buraya gelir
            ...serviceUIConfig[service.name] // Logo ve themeClass buradan gelir
          }));

        setServices(mergedServices);
        setLoading(false);
      } catch (error) {
        console.error("Servisler yüklenirken hata oluştu:", error);
        setLoading(false);
      }
    };

    fetchServices();
  }, []);

  return (
    <div className="portal-elite-wrapper">
      {/* Üst Header Alanı - Elit Metin Logo ve Çıkış Butonu */}
      <header className="portal-header-bar">
        <div className="turkcell-brand-box">
          <span className="turkcell-text-logo">TURKCELL</span>
        </div>
        <button className="elite-logout" onClick={onLogout}>
          Güvenli Çıkış
        </button>
      </header>

      <div className="portal-main-content">
        {/* Başlık Alanı */}
        <header className="hero-section">
          <h1>Dijital Dünyanı Yönet</h1>
          <p>Tüm servislerini tek noktadan kontrol et.</p>
        </header>

        {loading ? (
          <div style={{color:'white', textAlign:'center', marginTop:'50px'}}>Yükleniyor...</div>
        ) : (
          /* Yan Yana Duran Kartlar */
          <div className="service-card-grid">
            {services.map((service) => (
              <div 
                key={service.id} 
                className={`elite-service-card ${service.themeClass}`}
                onClick={() => onSelectService(service.name)} // İsim üzerinden Dashboard seçimi
              >
                <div className="card-top-accent"></div>
                
                <div className="card-inner">
                  <div className="service-logo-area">
                    <img src={service.logo} alt={service.name} className="brand-img" />
                  </div>
                  
                  <div className="service-text-area">
                    {/* Veritabanından gelen İsim */}
                    <h3>{service.name}</h3>
                    
                    {/* Veritabanından gelen Açıklama (Yoksa fallback kullanılır) */}
                    <p>{service.description || service.fallbackDesc}</p>
                    
                    {/* Küçük bir ekleme: Eğer sorun varsa burada belli etmeden metin rengiyle oynayabiliriz ama tasarımı bozmadım */}
                  </div>
                  
                  <div className="card-footer-btn">
                     {service.open_incident_count > 0 ? "⚠️ Sorunu İncele →" : "Hemen Yönet →"}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default Portal;