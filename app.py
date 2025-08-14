import streamlit as st
import pandas as pd
import requests
import json
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
import time
import random

# Sayfa konfigürasyonu
st.set_page_config(
    page_title="Your Way Ally",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Temiz ve çalışan CSS
st.markdown("""
<style>
    /* Ana tema */
    .main > div {
        padding: 0;
    }

    /* Header styling */
    .header-container {
        background: linear-gradient(135deg, #3b82f6, #8b5cf6, #ec4899);
        padding: 2rem;
        border-radius: 1rem;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        animation: fadeInDown 1s ease-out;
    }

    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-30px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .header-title {
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0;
        background: linear-gradient(45deg, #fbbf24, #f59e0b, #ef4444);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .header-subtitle {
        font-size: 1rem;
        opacity: 0.9;
        margin-top: 0.5rem;
    }

    /* Card styling */
    .destination-card {
        background: white;
        padding: 1.5rem;
        border-radius: 1rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
        border: 1px solid #e5e7eb;
        transition: all 0.3s ease;
        animation: slideInUp 0.6s ease-out;
    }

    @keyframes slideInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .destination-card:hover {
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
        transform: translateY(-5px);
    }

    .card-title {
        font-size: 1.25rem;
        font-weight: bold;
        color: #1f2937;
        margin-bottom: 0.5rem;
    }

    .card-description {
        color: #6b7280;
        font-size: 0.9rem;
        margin-bottom: 1rem;
    }

    .tag {
        display: inline-block;
        background: #dbeafe;
        color: #1e40af;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        margin: 0.125rem;
        transition: all 0.3s ease;
    }

    .tag:hover {
        background: #3b82f6;
        color: white;
        transform: scale(1.05);
    }

    .rating {
        color: #f59e0b;
        font-weight: bold;
    }

    /* Weather card */
    .weather-card {
        background: linear-gradient(135deg, #06b6d4, #3b82f6);
        color: white;
        padding: 2rem;
        border-radius: 1rem;
        text-align: center;
        margin-bottom: 1rem;
    }

    .weather-temp {
        font-size: 3rem;
        font-weight: bold;
        margin: 0;
    }

    .weather-condition {
        font-size: 1.1rem;
        opacity: 0.9;
    }

    /* Budget card */
    .budget-card {
        background: linear-gradient(135deg, #10b981, #059669);
        color: white;
        padding: 2rem;
        border-radius: 1rem;
        text-align: center;
        margin-bottom: 1rem;
    }

    .budget-amount {
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0;
    }

    /* Community card */
    .community-card {
        background: linear-gradient(135deg, #f97316, #ea580c);
        color: white;
        padding: 1.5rem;
        border-radius: 1rem;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }

    .community-card:hover {
        transform: translateX(5px);
    }

    /* Success/Warning alerts */
    .success-alert {
        background: #d1fae5;
        border: 1px solid #10b981;
        color: #065f46;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }

    .warning-alert {
        background: #fef3c7;
        border: 1px solid #f59e0b;
        color: #92400e;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }

    /* Sidebar logo */
    .sidebar-logo {
        text-align: center;
        padding: 1rem;
        background: linear-gradient(135deg, #4338ca, #7c3aed);
        margin: -1rem -1rem 2rem -1rem;
        color: white;
    }

    .logo-title {
        font-size: 1.5rem;
        font-weight: bold;
        margin: 0;
    }

    .logo-subtitle {
        font-size: 0.8rem;
        opacity: 0.8;
        margin-top: 0.25rem;
    }

    /* Stats card */
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 0.75rem;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }

    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.15);
    }

    .stat-number {
        font-size: 2rem;
        font-weight: bold;
        color: #1f2937;
    }

    .stat-label {
        color: #6b7280;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }

    /* Button hover effects */
    .stButton > button {
        transition: all 0.3s ease !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2) !important;
    }

    /* Responsive */
    @media (max-width: 768px) {
        .header-title {
            font-size: 2rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Session state initialization
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'selected_destination' not in st.session_state:
    st.session_state.selected_destination = None
if 'user_preferences' not in st.session_state:
    st.session_state.user_preferences = {
        'budget': 1000,
        'interests': [],
        'travel_style': 'comfort'
    }

# Mock data
destinations_data = [
    {
        'id': 1,
        'name': 'Kapadokya',
        'country': 'Türkiye',
        'description': 'Büyüleyici peri bacaları, sıcak hava balonları ve yeraltı şehirleri ile dolu mistik deneyim',
        'rating': 4.8,
        'difficulty': 'Kolay',
        'season': 'Tüm mevsimler',
        'tags': ['🌄 Doğa', '🎈 Macera', '📸 Fotoğraf', '🏛️ Tarih'],
        'coordinates': [38.6431, 34.8311],
        'highlights': ['🎈 Balon Turu', '🏛️ Göreme Açık Hava Müzesi', '🌄 Güneş Doğumu', '🏠 Peri Bacaları'],
        'best_time': 'Nisan-Kasım',
        'icon': '🎈',
        'price_range': '₺800-2500',
        'duration': '2-4 gün'
    },
    {
        'id': 2,
        'name': 'Pamukkale',
        'country': 'Türkiye',
        'description': 'Bembeyaz travertenler ve antik Hierapolis kalıntıları ile doğa ve tarihin buluştuğu destinasyon',
        'rating': 4.7,
        'difficulty': 'Kolay',
        'season': 'İlkbahar/Sonbahar',
        'tags': ['♨️ Termal', '🏛️ Tarih', '📸 Fotoğraf', '🌿 Doğa'],
        'coordinates': [37.9206, 29.1206],
        'highlights': ['♨️ Termal Havuzlar', '🏛️ Hierapolis Antik Kenti', '📸 Beyaz Travertenler',
                       '🏊‍♀️ Kleopatra Havuzu'],
        'best_time': 'Mart-Mayıs, Eylül-Kasım',
        'icon': '♨️',
        'price_range': '₺600-1800',
        'duration': '1-2 gün'
    },
    {
        'id': 3,
        'name': 'Olympos',
        'country': 'Türkiye',
        'description': 'Antik kalıntılar, cennet koyu ve doğal güzellikler ile deniz, tarih ve doğanın mükemmel uyumu',
        'rating': 4.6,
        'difficulty': 'Orta',
        'season': 'İlkbahar/Yaz',
        'tags': ['🏖️ Plaj', '🏛️ Tarih', '🥾 Trekking', '🔥 Doğa'],
        'coordinates': [36.4186, 30.4686],
        'highlights': ['🏖️ Olympos Plajı', '🏛️ Antik Kalıntılar', '🔥 Yanartaş (Chimaera)', '🌲 Lycian Yolu'],
        'best_time': 'Mayıs-Ekim',
        'icon': '🏖️',
        'price_range': '₺900-2200',
        'duration': '2-3 gün'
    },
    {
        'id': 4,
        'name': 'Safranbolu',
        'country': 'Türkiye',
        'description': 'Osmanlı mimarisi ve safran kokularıyla tarihi bir zamanda yolculuk deneyimi',
        'rating': 4.5,
        'difficulty': 'Kolay',
        'season': 'Tüm mevsimler',
        'tags': ['🏘️ Tarih', '🌸 Kültür', '🍯 Gastronomi', '📸 Fotoğraf'],
        'coordinates': [41.2500, 32.6864],
        'highlights': ['🏘️ Tarihi Evler', '🌸 Safran Bahçeleri', '🍯 Yerel Lezzetler', '🛤️ Taş Sokaklar'],
        'best_time': 'Tüm mevsimler',
        'icon': '🌸',
        'price_range': '₺500-1500',
        'duration': '1-2 gün'
    }
]

community_tips = [
    {
        'destination': 'Kapadokya',
        'tip': 'Balon turu için en iyi zaman gün doğumu. Rezervasyon mutlaka önceden yapın! Hava durumu nedeniyle iptal olabilir.',
        'author': 'Mehmet K.',
        'rating': 5,
        'date': '2 gün önce',
        'helpful_count': 24
    },
    {
        'destination': 'Pamukkale',
        'tip': 'Ayakkabılarınızı çıkarmanız gerekiyor. Havlu getirmeyi unutmayın. Günbatımı en güzel fotoğraf zamanı.',
        'author': 'Ayşe T.',
        'rating': 4,
        'date': '1 hafta önce',
        'helpful_count': 18
    },
    {
        'destination': 'Olympos',
        'tip': 'Yanartaş için el feneri alın, gece ziyareti çok etkileyici! Ayrıca trekking ayakkabısı şart.',
        'author': 'Can S.',
        'rating': 5,
        'date': '3 gün önce',
        'helpful_count': 31
    }
]

# Sidebar
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div style="display: flex; align-items: center; justify-content: center; gap: 0.5rem;">
            <div style="width: 2.5rem; height: 2.5rem; background: linear-gradient(45deg, #fbbf24, #f59e0b); border-radius: 0.75rem; display: flex; align-items: center; justify-content: center;">
                🧭
            </div>
            <div>
                <div class="logo-title">Your Way Ally</div>
                <div class="logo-subtitle">✨ AI Travel Assistant</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Authentication
    if not st.session_state.authenticated:
        st.markdown("### 🔐 Güvenli Giriş")

        username = st.text_input("👤 Kullanıcı Adı", placeholder="Kullanıcı adınızı girin")
        password = st.text_input("🔒 Şifre", type="password", placeholder="Şifrenizi girin")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🚀 Giriş Yap", use_container_width=True, type="primary"):
                if username and password:
                    with st.spinner('Giriş yapılıyor...'):
                        time.sleep(1)
                    st.session_state.authenticated = True
                    st.session_state.user_name = username
                    st.success("🎉 Başarıyla giriş yaptınız!")
                    st.balloons()
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Lütfen tüm alanları doldurun!")

        with col2:
            if st.button("📝 Kayıt Ol", use_container_width=True):
                st.info("🔗 Kayıt sayfasına yönlendiriliyorsunuz...")
    else:
        st.success(f"👋 Hoş geldin, {st.session_state.get('user_name', 'Kullanıcı')}!")

        if st.button("🚪 Güvenli Çıkış", use_container_width=True):
            st.session_state.authenticated = False
            st.info("👋 Başarıyla çıkış yaptınız!")
            time.sleep(1)
            st.rerun()

    st.markdown("---")

    # Navigation
    pages = {
        "🔍 Keşfet": "Ana sayfa - Destinasyon keşfi",
        "🌤️ Hava Durumu": "Güncel hava koşulları",
        "💰 Bütçe Planlayıcı": "Akıllı maliyet hesaplama",
        "🎒 Akıllı Çanta": "AI destekli paket listesi",
        "🤝 Topluluk": "Deneyim paylaşımı",
        "👤 Profil & Ayarlar": "Kişisel tercihler"
    }

    selected_page = st.selectbox(
        "🧭 **Navigasyon Menüsü**",
        list(pages.keys()),
        help="Gezinmek istediğiniz bölümü seçin"
    )

    st.caption(f"ℹ️ {pages[selected_page]}")

# Main content
if selected_page == "🔍 Keşfet":
    st.markdown("""
    <div class="header-container">
        <h1 class="header-title">🌟 Yeni Keşifler Seni Bekliyor!</h1>
        <p class="header-subtitle">🤖 AI destekli öneriler ile unutulmaz seyahatler planlayın</p>
    </div>
    """, unsafe_allow_html=True)

    # Search section
    st.markdown("### 🔍 **Akıllı Destinasyon Arama**")

    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        search_query = st.text_input(
            "",
            placeholder="🌍 Hangi destinasyonu keşfetmek istiyorsun?",
            help="Arama terimlerinizi girin"
        )
    with col2:
        search_button = st.button("🔍 **Ara**", use_container_width=True, type="primary")
    with col3:
        filter_button = st.button("🎛️ **Filtrele**", use_container_width=True)

    if search_button and search_query:
        with st.spinner('🤖 AI en uygun destinasyonları buluyor...'):
            time.sleep(1.5)
        st.success(f"🎯 '{search_query}' için {len(destinations_data)} destinasyon bulundu!")

    st.markdown("---")

    # Destination cards
    st.markdown("### 🏞️ **AI Önerili Destinasyonlar**")

    for i, dest in enumerate(destinations_data):
        with st.container():
            # Streamlit bileşenleri ile kart oluştur
            with st.container():
                st.markdown(f"""
                <div class="destination-card">
                    <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 1rem;">
                        <div>
                            <div class="card-title">{dest['icon']} {dest['name']}</div>
                            <span style="color: #6b7280; font-size: 0.9rem;">📍 {dest['country']}</span>
                            <div style="margin-top: 0.25rem;">
                                <span style="background: #fef3c7; color: #92400e; padding: 0.125rem 0.5rem; border-radius: 1rem; font-size: 0.7rem; margin-right: 0.5rem;">
                                    💰 {dest['price_range']}
                                </span>
                                <span style="background: #e0f2fe; color: #0277bd; padding: 0.125rem 0.5rem; border-radius: 1rem; font-size: 0.7rem;">
                                    ⏱️ {dest['duration']}
                                </span>
                            </div>
                        </div>
                        <div style="display: flex; align-items: center; gap: 0.25rem;">
                            <span style="color: #f59e0b;">⭐</span>
                            <span class="rating">{dest['rating']}</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Açıklama
                st.markdown(f"**{dest['description']}**")
                
                # Öne çıkanlar
                st.markdown("**🌟 ÖNE ÇIKANLAR:**")
                for highlight in dest['highlights']:
                    st.markdown(f"• {highlight}")
                
                # Etiketler
                st.markdown("**🏷️ ETİKETLER:**")
                cols = st.columns(len(dest['tags']))
                for i, tag in enumerate(dest['tags']):
                    with cols[i]:
                        st.markdown(f"<span class='tag'>{tag}</span>", unsafe_allow_html=True)
                
                # Bilgi grid'i
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"**🎯 Zorluk:** {dest['difficulty']}")
                with col2:
                    st.markdown(f"**🗓️ Mevsim:** {dest['season']}")
                with col3:
                    st.markdown(f"**📅 En İyi Zaman:** {dest['best_time']}")

            # Buttons
            col_btn1, col_btn2, col_btn3 = st.columns(3)

            with col_btn1:
                if st.button(f"📋 **Detayları Gör**", key=f"select_{dest['id']}", use_container_width=True,
                             type="primary"):
                    with st.spinner(f'🔍 {dest["name"]} bilgileri yükleniyor...'):
                        time.sleep(1)
                    st.session_state.selected_destination = dest
                    st.success(f"✅ {dest['name']} seçildi!")
                    st.balloons()

            with col_btn2:
                if st.button(f"💰 **Bütçe Hesapla**", key=f"budget_{dest['id']}", use_container_width=True):
                    st.session_state.selected_destination = dest
                    st.info(f"💰 {dest['name']} için bütçe hesaplaması yapılıyor...")

            with col_btn3:
                if st.button(f"🎒 **Çanta Hazırla**", key=f"pack_{dest['id']}", use_container_width=True):
                    st.session_state.selected_destination = dest
                    st.info(f"🎒 {dest['name']} için çanta listesi hazırlanıyor...")

    # Selected destination info
    if st.session_state.selected_destination:
        dest = st.session_state.selected_destination
        st.markdown("---")

        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 2rem; border-radius: 1rem; margin: 1rem 0; text-align: center;">
            <h3 style="margin: 0; font-size: 1.5rem;">🎯 Seçili Destinasyon: {dest['name']}</h3>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Detaylı bilgiler için diğer sekmeleri ziyaret edin</p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"""
            <div style="background: #dbeafe; padding: 1rem; border-radius: 0.75rem; text-align: center;">
                <h4 style="color: #1e40af; margin: 0;">📍 Koordinatlar</h4>
                <p style="font-size: 0.8rem; margin: 0.5rem 0 0 0; color: #1e40af;">{dest['coordinates'][0]:.4f}°N<br>{dest['coordinates'][1]:.4f}°E</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div style="background: #dcfce7; padding: 1rem; border-radius: 0.75rem; text-align: center;">
                <h4 style="color: #166534; margin: 0;">⭐ Değerlendirme</h4>
                <p style="font-size: 0.8rem; margin: 0.5rem 0 0 0; color: #166534;">{"⭐" * int(dest['rating'])}<br>({dest['rating']}/5.0)</p>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div style="background: #faf5ff; padding: 1rem; border-radius: 0.75rem; text-align: center;">
                <h4 style="color: #7c2d12; margin: 0;">💰 Fiyat Aralığı</h4>
                <p style="font-size: 0.8rem; margin: 0.5rem 0 0 0; color: #7c2d12;">{dest['price_range']}<br>kişi başı</p>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
            <div style="background: #fef3c7; padding: 1rem; border-radius: 0.75rem; text-align: center;">
                <h4 style="color: #92400e; margin: 0;">⏱️ Süre</h4>
                <p style="font-size: 0.8rem; margin: 0.5rem 0 0 0; color: #92400e;">Önerilen:<br>{dest['duration']}</p>
            </div>
            """, unsafe_allow_html=True)

elif selected_page == "🌤️ Hava Durumu":
    st.markdown("""
    <div class="header-container">
        <h1 class="header-title">🌤️ Akıllı Hava Durumu</h1>
        <p class="header-subtitle">🤖 AI destekli hava tahminleri ve seyahat önerileri</p>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.selected_destination:
        dest = st.session_state.selected_destination

        # Mock weather data
        weather_conditions = [
            {'condition': 'Güneşli', 'icon': '☀️', 'temp_range': (18, 28)},
            {'condition': 'Parçalı Bulutlu', 'icon': '⛅', 'temp_range': (15, 25)},
            {'condition': 'Bulutlu', 'icon': '☁️', 'temp_range': (12, 22)}
        ]

        current_weather = random.choice(weather_conditions)
        current_temp = random.randint(*current_weather['temp_range'])

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"""
            <div class="weather-card">
                <div style="display: flex; justify-content: center; align-items: center; gap: 1rem; margin-bottom: 1rem;">
                    <div style="font-size: 4rem;">{current_weather['icon']}</div>
                    <div>
                        <h3 style="margin: 0;">{dest['name']}</h3>
                        <p style="margin: 0; opacity: 0.8;">Anlık Durum</p>
                    </div>
                </div>
                <div class="weather-temp">{current_temp}°C</div>
                <div class="weather-condition">{current_weather['condition']}</div>
                <div style="margin-top: 1rem; font-size: 0.9rem; opacity: 0.8;">
                    Son güncelleme: {datetime.now().strftime('%H:%M')}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Weather details
            st.markdown("### 📊 **Detaylı Hava Bilgileri**")

            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("💧 Nem", f"{random.randint(45, 85)}%")
                st.metric("👁️ Görüş", f"{random.randint(5, 15)} km")
