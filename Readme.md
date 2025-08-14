# Your Way Ally — Streamlit Seyahat Chatbotu

Tamamen ücretsiz API'ler ve yerel LLM kullanarak çalışan, akıllı seyahat asistanı uygulaması.

## ✨ Özellikler

- **🤖 Yerel LLM**: Ollama ile çalışır (llama3:8b-instruct varsayılan)
- **🌤️ Hava Durumu**: Open-Meteo API (API anahtarı gerektirmez)
- **📍 Destinasyon Keşfi**: OpenTripMap API ile gezilecek yerler
- **🎯 Yakınımdakiler**: Konum bazlı öneriler
- **💬 Akıllı Sohbet**: Doğal dil işleme ile seyahat planlaması
- **⚡ Hızlı ve Güvenli**: Rate-limit koruması ve önbellek sistemi

## 📁 Proje Yapısı

```
yourwayally-streamlit/
├── app.py                 # Ana Streamlit uygulaması
├── tools.py               # API araçları (hava, yerler, geocode)
├── utils.py               # Yardımcı fonksiyonlar ve RateLimiter
├── requirements.txt       # Python bağımlılıkları
├── README.md             # Bu dosya
└── .streamlit/
    └── secrets.toml       # Yapılandırma dosyası
```

## 🚀 Hızlı Başlangıç

### 1. Önkoşullar
- Python 3.10+
- [Ollama](https://ollama.com) kurulu olmalı
- [OpenTripMap](https://opentripmap.io) ücretsiz API anahtarı

### 2. Kurulum

```bash
# Projeyi indirin
git clone [repo-url] yourwayally-streamlit
cd yourwayally-streamlit

# Sanal ortam oluşturun
python -m venv .venv

# Sanal ortamı etkinleştirin
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate

# Bağımlılıkları yükleyin
pip install -r requirements.txt
```

### 3. Yapılandırma

`.streamlit/secrets.toml` dosyasını oluşturun:

```toml
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = "llama3:8b-instruct"
OPENTRIPMAP_API_KEY = "your_api_key_here"
```

### 4. Ollama Modelini İndirin

```bash
ollama pull llama3:8b-instruct
```

### 5. Uygulamayı Başlatın

```bash
streamlit run app.py
```

Uygulama `http://localhost:8501` adresinde açılacaktır.

## 💡 Kullanım Örnekleri

- **Seyahat Planlaması**: "İstanbul'da 3 günlük gezi planı yap"
- **Hava Durumu**: "İzmir'in hava durumu nasıl?"
- **Yakın Yerler**: "41.0082, 28.9784 yakınındaki müzeler"
- **Genel Sorular**: "Kapadokya'da ne yapabilirim?"

## ⚙️ Gelişmiş Ayarlar

### Rate Limiting Ayarları
`utils.py` dosyasındaki `RateLimiter` sınıfını kullanarak API çağrı limitlerini kontrol edebilirsiniz.

### OpenTripMap Kategori Filtreleri
Gezilecek yerleri kategorilere göre filtrelemek için `kinds` parametresini kullanabilirsiniz:
- `museums` - Müzeler
- `historic` - Tarihi yerler
- `natural` - Doğal yerler
- `architecture` - Mimari yapılar

## 🔧 Sorun Giderme

### Ollama Bağlantı Problemi
```bash
# Ollama servisinin çalıştığını kontrol edin
ollama serve
```

### API Anahtarı Hatası
OpenTripMap API anahtarınızın geçerli olduğundan ve `secrets.toml` dosyasında doğru yazıldığından emin olun.

### Port Çakışması
Eğer 8501 portu kullanımda ise:
```bash
streamlit run app.py --server.port 8502
```

## 🤝 Katkıda Bulunma

1. Bu repository'yi fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## 📄 Lisans

Bu proje açık kaynaklıdır ve MIT lisansı altında dağıtılmaktadır. API sağlayıcıların kullanım koşullarına uygun olarak kullanınız.

## 🆘 Destek

Sorularınız için:
- Issues sekmesinden yeni bir konu açın
- Dokümantasyonu kontrol edin
- Community forumlarından yardım alın

---

**Not**: Bu uygulama ücretsiz API'ler kullandığı için kullanım limitleri bulunmaktadır. Yoğun kullanım için ücretli planları değerlendirebilirsiniz.
