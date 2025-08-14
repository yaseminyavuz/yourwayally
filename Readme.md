Your Way Ally — Streamlit Chatbot (Tamamen Ücretsiz)
====================================================

Bu proje, tamamen ücretsiz API'ler ve yerel LLM (Ollama) kullanarak çalışan,
web tabanlı bir seyahat chatbot uygulamasıdır.

Özellikler
----------
- Yerel LLM: Ollama (llama3:8b-instruct varsayılan)
- Hava durumu bilgisi: Open-Meteo API (API anahtarı gerektirmez)
- Destinasyon arama: OpenTripMap API (ücretsiz plan)
- "Yakınımdakiler" özelliği: OpenTripMap /places/radius
- Basit ve profesyonel Streamlit arayüzü
- Rate-limit ve cache mekanizması
- Modüler yapı (`app.py`, `tools.py`, `utils.py`)

Proje Yapısı
------------
yourwayally-streamlit/
│
├── app.py                 # Ana Streamlit uygulaması
├── tools.py               # API araçları (hava, yerler, geocode vb.)
├── utils.py               # Ortak yardımcı fonksiyonlar
├── requirements.txt       # Python bağımlılık listesi
├── README.txt              # Bu dosya
└── .streamlit/
    └── secrets.toml        # API anahtarları ve ayarlar

Gereksinimler
-------------
- Python 3.10+
- pip (Python paket yöneticisi)
- Ollama (https://ollama.com)
- OpenTripMap ücretsiz API anahtarı (https://opentripmap.io)

Kurulum
-------
1. Depoyu bilgisayarına al (veya yeni klasör oluştur).
2. Terminal / PowerShell'de proje kök dizinine git:
   cd "C:\Users\<KullanıcıAdı>\PycharmProjects\yourwayally-streamlit"

3. Sanal ortam oluştur ve aktif et:
   python -m venv .venv
   .venv\Scripts\activate      (Windows)
   source .venv/bin/activate   (Mac/Linux)

4. Bağımlılıkları yükle:
   pip install -r requirements.txt

5. .streamlit/secrets.toml dosyasını oluştur:
   mkdir .streamlit
   notepad .streamlit\secrets.toml
   İçerik:
   --------------------------------
   OLLAMA_BASE_URL = "http://localhost:11434"
   OLLAMA_MODEL = "llama3:8b-instruct"
   OPENTRIPMAP_API_KEY = "senin_otm_anahtarın"
   --------------------------------

6. Ollama’yı kur ve modeli indir:
   ollama pull llama3:8b-instruct

Çalıştırma
----------
streamlit run app.py

Kullanım
--------
- Sohbet kutusuna sorularını yaz.
- "yakın" veya "gezilecek" gibi kelimeler geçtiğinde OpenTripMap'ten öneriler gelir.
- "38.42, 27.14" gibi koordinatlar yazarsan hava durumu bilgisi eklenir.
- Lat/lon veya şehir adı ile "yakınımdakiler" özelliğini kullanabilirsin.

İpuçları
--------
- API limitine takılmamak için `utils.py` içindeki RateLimiter değerini artırabilirsin.
- Daha spesifik arama yapmak için OpenTripMap "kinds" parametresini kullanabilirsin.
- Nominatim geocode özelliği ile şehir adlarını otomatik lat/lon’a çevirebilirsin.

Lisans
------
Bu proje açık kaynaklıdır. API sağlayıcıların ücretsiz kullanım politikalarına
uymak kaydıyla ticari olmayan projelerde kullanılabilir.
