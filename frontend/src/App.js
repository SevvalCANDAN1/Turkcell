import { useState } from "react";
import "./login.css";
import Portal from "./Portal"; 

// --- BACKEND BAĞLANTILI DASHBOARDLARI İÇE AKTARIYORUZ ---
import SuperonlineDashboard from "./SuperonlineDashboard"; 
import TVPlusDashboard from "./TVPlusDashboard";
import PaycellDashboard from "./PaycellDashboard";

// Giriş Bilgileri (Mock Data)
import { validUsers } from "./authData";

function App() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState(""); // Hata mesajı için
  
  const [step, setStep] = useState("main-login"); 
  const [selectedService, setSelectedService] = useState(null);

  const handleSubmit = (e) => {
    e.preventDefault();
    setError("");

    // KONTROL: Girilen bilgiler "main" (admin) kullanıcısı ile eşleşiyor mu?
    if (email === validUsers.main.email && password === validUsers.main.pass) {
       setStep("portal");
    } else {
       setError("E-posta veya şifre hatalı!");
    }
  };

  const handleLogout = () => {
    setStep("main-login");
    setEmail("");
    setPassword("");
    setSelectedService(null);
    setError("");
  };

  // --- ADIM 3: DOĞRUDAN DASHBOARD EKRANLARI ---
  if (step === "service-dashboard") {
    
    // Debug: Hangi ismin geldiğini konsola yazdırır
    console.log("Seçilen Servis:", selectedService);

    // 1. Superonline Kontrolü
    if (selectedService === "Superonline") {
      return <SuperonlineDashboard onBack={() => setStep("portal")} />;
    }

    // 2. TV+ Kontrolü (HATA DÜZELTİLDİ: "TV+" veya "TVPlus" hepsini kabul et)
    if (selectedService === "TV+" || selectedService === "TVPlus" || selectedService === "TV Plus") {
      return <TVPlusDashboard onBack={() => setStep("portal")} />;
    }

    // 3. Paycell Kontrolü
    if (selectedService === "Paycell") {
       return <PaycellDashboard onBack={() => setStep("portal")} />;
    }
    
    // Eğer eşleşme olmazsa Hata Ekranı
    return (
      <div style={{backgroundColor: '#001a3d', minHeight: '100vh', color: 'white', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', fontFamily: 'Inter'}}>
        <h1>'{selectedService}' Dashboard Hazırlanıyor...</h1>
        <p style={{marginTop:'10px', color:'#ccc'}}>Servis ismi kod ile eşleşmedi.</p>
        <button onClick={() => setStep("portal")} style={{padding: '10px 20px', cursor: 'pointer', borderRadius: '10px', border: 'none', marginTop: '20px'}}>Geri Dön</button>
      </div>
    );
  }

  // --- ADIM 2: PORTAL EKRANI (Backend'den Servisleri Çeker) ---
  if (step === "portal") {
    return (
      <Portal 
        onSelectService={(serviceName) => {
          setSelectedService(serviceName);
          setStep("service-dashboard");
        }} 
        onLogout={handleLogout}
      />
    );
  }

  // --- ADIM 1: ANA LOGIN EKRANI ---
  return (
    <div className="login-container">
      <div className="login-box" style={{ textAlign: 'center' }}>
        <div className="logo-wrapper" style={{ display: 'flex', justifyContent: 'center', marginBottom: '25px', width: '100%' }}>
          {/* Turkcell Logosu */}
          <svg width="220" height="60" viewBox="0 0 220 60" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="30" cy="30" r="18" fill="#FFC600" />
            <text x="60" y="40" fontFamily="'Inter', sans-serif" fontSize="32" fontWeight="800" fill="#005baa" letterSpacing="-1">
              TURKCELL
            </text>
          </svg>
        </div>

        <h2 style={{ marginBottom: '10px' }}>Hoş Geldiniz</h2>
        <p style={{ marginBottom: '30px', color: '#64748b' }}>Bilgilerinizle giriş yaparak devam edin.</p>

        {error && <p style={{color: 'red', marginBottom: '15px'}}>{error}</p>}

        <form onSubmit={handleSubmit} style={{ textAlign: 'left' }}>
          <div className="input-group">
            <input
              type="email"
              placeholder="E-posta (admin@turkcell.com)"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              style={{ width: '100%', padding: '12px', marginBottom: '10px', borderRadius: '8px', border: '1px solid #ccc' }}
            />
          </div>

          <div className="input-group password-group" style={{ position: 'relative' }}>
            <input
              type={showPassword ? "text" : "password"}
              placeholder="Şifre (12345)"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              style={{ width: '100%', padding: '12px', marginBottom: '20px', borderRadius: '8px', border: '1px solid #ccc' }}
            />
            <button 
              type="button" 
              onClick={() => setShowPassword(!showPassword)}
              style={{ position: 'absolute', right: '10px', top: '12px', background: 'none', border: 'none', cursor: 'pointer' }}
            >
              {showPassword ? "👁️" : "🙈"}
            </button>
          </div>

          <button type="submit" className="login-btn" style={{ width: '100%', padding: '12px', backgroundColor: '#005baa', color: 'white', border: 'none', borderRadius: '8px', cursor: 'pointer', fontWeight: 'bold' }}>
            Giriş Yap
          </button>
        </form>

        <div className="footer-links" style={{ marginTop: '25px', fontSize: '14px' }}>
          <span style={{ color: '#666' }}>Henüz üye değil misiniz? </span>
          <a href="#" style={{ fontWeight: 'bold', color: '#005baa', textDecoration: 'none' }}>Hemen Katıl</a>
        </div>
      </div>
    </div>
  );
}

export default App;