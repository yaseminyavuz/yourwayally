import streamlit as st
import pandas as pd
import requests
import json
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import time

# Sayfa konfigürasyonu
st.set_page_config(
    page_title="Your Way Ally",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    /* Ana tema */
    .main > div {
        padding: 0;
    }

    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(to bottom, #4338ca, #7c3aed);
    }

    /* Header styling */
    .header-container {
        background: linear-gradient(to right, #3b82f6, #8b5cf6);
        padding: 1rem 2rem;
        border-radius: 0.75rem;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }

    .header-title {
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0;
        background: linear-gradient(to right, #fbbf24, #f59e0b, #ef4444);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .header-subtitle {
        font-size: 0.9rem;
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
    }

    .destination-card:hover {
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
        transform: translateY(-2px);
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
    }

    .rating {
        color: #f59e0b;
        font-weight: bold;
    }

    /* Weather card */
    .weather-card {
        background: linear-gradient(to right, #06b6d4, #3b82f6);
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
        background: linear-gradient(to right, #10b981, #059669);
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
        background: linear-gradient(to right, #f97316, #ea580c);
        color: white;
        padding: 1.5rem;
        border-radius: 1rem;
        margin-bottom: 1rem;
    }

    /* Packing list */
    .packing-item {
        background: #f3f4f6;
        padding: 0.75rem;
        border-radius: 0.5rem;
        margin-bottom: 0.5rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .essential {
        background: #fef2f2;
        border-left: 4px solid #ef4444;
    }

    .optional {
        background: #eff6ff;
        border-left: 4px solid #3b82f6;
    }

    /* Sidebar logo */
    .sidebar-logo {
        text-align: center;
        padding: 1rem;
        background: linear-gradient(to right, #4338ca, #7c3aed);
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

    /* Stats grid */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 1rem 0;
    }

    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 0.75rem;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
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

    /* Fix for text visibility */
    .element-container .stMarkdown {
        color: inherit;
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
        'description': 'Büyüleyici kayalar, sıcak hava balonları ve underground şehirler',
        'rating': 4.8,
        'difficulty': 'Kolay',
        'season': 'Tüm mevsimler',
        'tags': ['Doğa', 'Macera', 'Fotoğraf'],
        'coordinates': [38.6431, 34.8311],
        'highlights': ['🎈 Balon Turu', '🏛️ Göreme Açık Hava Müzesi', '🌄 Güneş Doğumu'],
        'best_time': 'Nisan-Kasım',
        'icon': '🎈'
    },
    {
        'id': 2,
        'name': 'Pamukkale',
        'country': 'Türkiye',
        'description': 'Beyaz travertenler ve antik Hierapolis kalıntıları',
        'rating': 4.7,
        'difficulty': 'Kolay',
        'season': 'İlkbahar/Sonbahar',
        'tags': ['Doğa', 'Termal', 'Tarih'],
        'coordinates': [37.9206, 29.1206],
        'highlights': ['♨️ Termal Havuzlar', '🏛️ Hierapolis Antik Kenti', '📸 Beyaz Travertenler'],
        'best_time': 'Mart-Mayıs, Eylül-Kasım',
        'icon': '♨️'
    },
    {
        'id': 3,
        'name': 'Olympos',
        'country': 'Türkiye',
        'description': 'Antik kalıntılar, cennet koyu ve doğal güzellikler',
        'rating': 4.6,
        'difficulty': 'Orta',
        'season': 'İlkbahar/Yaz',
        'tags': ['Plaj', 'Tarih', 'Trekking'],
        'coordinates': [36.4186, 30.4686],
        'highlights': ['🏖️ Olympos Plajı', '🏛️ Antik Kalıntılar', '🔥 Yanartaş (Chimaera)'],
        'best_time': 'Mayıs-Ekim',
        'icon': '🏖️'
    }
]

community_tips = [
    {
        'destination': 'Kapadokya',
        'tip': 'Balon turu için en iyi zaman gün doğumu. Rezervasyon mutlaka önceden yapın!',
        'author': 'Mehmet K.',
        'rating': 5
    },
    {
        'destination': 'Pamukkale',
        'tip': 'Ayakkabılarınızı çıkarmanız gerekiyor. Havlu getirmeyi unutmayın.',
        'author': 'Ayşe T.',
        'rating': 4
    }
]

# Sidebar - Logo ve Navigasyon
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div style="display: flex; align-items: center; justify-content: center; gap: 0.5rem;">
            <div style="width: 2.5rem; height: 2.5rem; background: linear-gradient(to bottom right, #fbbf24, #f59e0b); border-radius: 0.75rem; display: flex; align-items: center; justify-content: center;">
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
        st.markdown("### 🔐 Giriş Yap")
        with st.form("login_form"):
            username = st.text_input("Kullanıcı Adı")
            password = st.text_input("Şifre", type="password")
            login_button = st.form_submit_button("Giriş Yap", use_container_width=True)

            if login_button and username and password:
                st.session_state.authenticated = True
                st.session_state.user_name = username
                st.success("Başarıyla giriş yaptınız!")
                st.rerun()
    else:
        st.success(f"Hoş geldin, {st.session_state.get('user_name', 'Kullanıcı')}! 👋")
        if st.button("Çıkış Yap", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()

    st.markdown("---")

    # Navigation
    page = st.selectbox(
        "📍 Navigasyon",
        ["🔍 Keşfet", "🌤️ Hava Durumu", "💰 Bütçe", "🎒 Çanta", "🤝 Topluluk", "👤 Profil"]
    )


# Helper function for destination cards
def render_destination_card(dest):
    """Destinasyon kartını render eden yardımcı fonksiyon"""

    # Card container
    with st.container():
        # Card header
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"### {dest['icon']} {dest['name']}")
            st.caption(f"📍 {dest['country']}")
        with col2:
            st.markdown(f"**⭐ {dest['rating']}**")

        # Description
        st.write(dest['description'])

        # Highlights
        st.markdown("**Öne Çıkanlar:**")
        highlight_cols = st.columns(len(dest['highlights']))
        for i, highlight in enumerate(dest['highlights']):
            with highlight_cols[i]:
                st.info(highlight)

        # Tags
        tag_text = " • ".join(dest['tags'])
        st.markdown(f"🏷️ **Etiketler:** {tag_text}")

        # Info row
        col1, col2 = st.columns(2)
        with col1:
            st.metric("🎯 Zorluk", dest['difficulty'])
        with col2:
            st.metric("🗓️ Sezon", dest['season'])

        # Select button
        if st.button(f"📋 {dest['name']} Seç", key=f"select_{dest['id']}", use_container_width=True):
            st.session_state.selected_destination = dest
            st.success(f"✅ {dest['name']} seçildi!")
            st.rerun()

        st.markdown("---")


# Ana içerik
if page == "🔍 Keşfet":
    st.markdown("""
    <div class="header-container">
        <h1 class="header-title">Yeni keşifler seni bekliyor! 🌟</h1>
        <p class="header-subtitle">AI destekli öneriler ile unutulmaz seyahatler planlayın</p>
    </div>
    """, unsafe_allow_html=True)

    # Arama
    col1, col2 = st.columns([4, 1])
    with col1:
        search_query = st.text_input("🔍 Nereye gitmek istiyorsun?", placeholder="Destinasyon ara...")
    with col2:
        st.write("")
        st.write("")
        search_button = st.button("Ara", use_container_width=True)

    # Destinasyon kartları
    st.markdown("### 🏞️ Önerilen Destinasyonlar")

    # Filter based on search
    filtered_destinations = destinations_data
    if search_query:
        filtered_destinations = [d for d in destinations_data
                                 if search_query.lower() in d['name'].lower()
                                 or search_query.lower() in d['description'].lower()]

    for dest in filtered_destinations:
        render_destination_card(dest)

    # Seçili destinasyon detayları
    if st.session_state.selected_destination:
        dest = st.session_state.selected_destination
        st.markdown(f"## 🎯 {dest['name']} - Detay Bilgileri")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.info(f"📍 **Konum**\n\nKoordinatlar: {dest['coordinates'][0]}, {dest['coordinates'][1]}")
        with col2:
            stars = "⭐" * int(dest['rating'])
            st.success(f"⭐ **Değerlendirme**\n\n{stars} ({dest['rating']})")
        with col3:
            st.warning(f"🗓️ **En İyi Zaman**\n\n{dest['best_time']}")

elif page == "🌤️ Hava Durumu":
    st.markdown("""
    <div class="header-container">
        <h1 class="header-title">🌤️ Hava Durumu Bilgisi</h1>
        <p class="header-subtitle">Seçilen destinasyon için güncel hava durumu</p>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.selected_destination:
        dest = st.session_state.selected_destination

        # Mock weather data
        weather_data = {
            'temperature': 22,
            'condition': 'Güneşli',
            'humidity': 65,
            'wind_speed': 12,
            'visibility': 8
        }

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"### 🌤️ {dest['name']} - Güncel Durum")

            # Weather display
            temp_col, cond_col = st.columns(2)
            with temp_col:
                st.metric("🌡️ Sıcaklık", f"{weather_data['temperature']}°C")
            with cond_col:
                st.metric("☀️ Durum", weather_data['condition'])

            # Weather details
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("💧 Nem", f"{weather_data['humidity']}%")
            with col_b:
                st.metric("💨 Rüzgar", f"{weather_data['wind_speed']} km/h")
            with col_c:
                st.metric("👁️ Görüş", f"{weather_data['visibility']} km")

        with col2:
            st.markdown("### 📅 7 Günlük Tahmin")
            forecast_data = []
            for i in range(7):
                date = datetime.now() + timedelta(days=i)
                forecast_data.append({
                    'Gün': date.strftime('%A')[:3],
                    'Tarih': date.strftime('%d/%m'),
                    'Sıcaklık': 22 + (i % 3) - 1,
                    'Durum': ['☀️', '⛅', '🌧️'][i % 3]
                })

            forecast_df = pd.DataFrame(forecast_data)
            st.dataframe(forecast_df, use_container_width=True, hide_index=True)

            # Weather chart
            fig = px.line(forecast_df, x='Gün', y='Sıcaklık',
                          title='Sıcaklık Trendi',
                          markers=True)
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning("🎯 Hava durumu bilgisi için önce Keşfet sekmesinden bir destinasyon seçin.")

elif page == "💰 Bütçe":
    st.markdown("""
    <div class="header-container">
        <h1 class="header-title">💰 Seyahat Maliyeti</h1>
        <p class="header-subtitle">AI destekli maliyet hesaplama ve bütçe planlama</p>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.selected_destination:
        dest = st.session_state.selected_destination

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"### 💵 {dest['name']} - Tahmini Maliyet")

            # Budget calculation form
            duration = st.slider("🗓️ Seyahat Süresi (gün)", 1, 14, 3)
            travel_style = st.selectbox("🎭 Seyahat Tarzı",
                                        ["💰 Bütçe Dostu", "🏨 Konforlu", "✨ Lüks"])

            # Mock cost calculation
            base_costs = {
                'Ulaşım': 400,
                'Konaklama': 150 * duration,
                'Yemek': 80 * duration,
                'Aktiviteler': 200 * duration
            }

            # Adjust based on travel style
            multiplier = {"💰 Bütçe Dostu": 0.7, "🏨 Konforlu": 1.0, "✨ Lüks": 1.8}[travel_style]
            adjusted_costs = {k: int(v * multiplier) for k, v in base_costs.items()}
            total_cost = sum(adjusted_costs.values())

            # Total cost display
            st.success(f"### 💰 Toplam Maliyet: ₺{total_cost:,}")
            st.caption(f"{duration} günlük seyahat")

            # Cost breakdown
            st.markdown("### 📊 Maliyet Dağılımı")
            for category, amount in adjusted_costs.items():
                st.metric(category, f"₺{amount:,}")

            # Budget pie chart
            fig = px.pie(values=list(adjusted_costs.values()),
                         names=list(adjusted_costs.keys()),
                         title="Maliyet Dağılımı")
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("### 🎛️ Bütçe Ayarları")

            user_budget = st.slider("💰 Toplam Bütçe", 500, 10000,
                                    st.session_state.user_preferences['budget'], step=100)
            st.session_state.user_preferences['budget'] = user_budget

            # Budget comparison
            if total_cost <= user_budget:
                st.success(f"✅ Bu seyahat bütçenize uygun!\n\n**Kalan: ₺{user_budget - total_cost:,}**")
            else:
                st.error(f"⚠️ Bütçe aşımı!\n\n**Fazla: ₺{total_cost - user_budget:,}**")

            # Savings tips
            st.markdown("### 💡 Tasarruf İpuçları")
            st.info("🌟 Erken rezervasyon ile %20-30 tasarruf sağlayabilirsiniz!")
            st.info("📅 Esnek tarihlerde seyahat etmek maliyetleri düşürür")
            st.info("🏠 Yerel konaklama seçeneklerini değerlendirin")

    else:
        st.warning("🎯 Maliyet hesaplaması için önce Keşfet sekmesinden bir destinasyon seçin.")

elif page == "🎒 Çanta":
    st.markdown("""
    <div class="header-container">
        <h1 class="header-title">🎒 Akıllı Çanta Listesi</h1>
        <p class="header-subtitle">Hava durumu ve aktivitelere göre AI destekli paket önerisi</p>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.selected_destination:
        dest = st.session_state.selected_destination

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"### 🎯 {dest['name']} için Öneriler")

            # Mock packing list based on destination
            packing_lists = {
                'Kapadokya': {
                    'Belgeler': [('Pasaport/Kimlik', True), ('Seyahat sigortası', False)],
                    'Kıyafet': [('Sıcak mont', True), ('Rahat ayakkabı', True), ('Şapka', False)],
                    'Elektronik': [('Telefon şarj cihazı', True), ('Kamera', False)],
                    'Sağlık': [('İlk yardım çantası', True), ('Güneş kremi', True)]
                },
                'Pamukkale': {
                    'Belgeler': [('Pasaport/Kimlik', True), ('Otel rezervasyonu', False)],
                    'Kıyafet': [('Havlu', True), ('Çıkarılabilir ayakkabı', True), ('Mayo', False)],
                    'Elektronik': [('Telefon şarj cihazı', True), ('Su geçirmez kamera', False)],
                    'Sağlık': [('İlk yardım çantası', True), ('Termal suya uygun krem', False)]
                },
                'Olympos': {
                    'Belgeler': [('Pasaport/Kimlik', True), ('Seyahat sigortası', False)],
                    'Kıyafet': [('Mayo', True), ('Yürüyüş ayakkabısı', True), ('Plaj havlusu', True)],
                    'Elektronik': [('Telefon şarj cihazı', True), ('Su geçirmez çanta', False)],
                    'Sağlık': [('Güneş kremi', True), ('Su matarası', True), ('Böcek spreyi', False)]
                }
            }

            current_list = packing_lists.get(dest['name'], packing_lists['Kapadokya'])

            for category, items in current_list.items():
                st.markdown(f"#### {category}")
                for item, essential in items:
                    if essential:
                        st.error(f"🔴 **{item}** - Zorunlu")
                    else:
                        st.info(f"🔵 **{item}** - İsteğe bağlı")

            st.success("🌟 **AI Önerisi:** Bu liste hava durumu tahminleri ve seçilen aktivitelere göre oluşturuldu!")

        with col2:
            st.markdown("### 📋 Çanta Kontrol Listesi")

            # Last minute checks
            st.markdown("#### ⚠️ Son Dakika Kontrolleri")
            checks = [
                "Pasaport geçerlilik tarihi (6 ay önceden)",
                "Seyahat sigortası aktif mi?",
                "Telefon operatörü roaming paketleri",
                "Banka kartı yurtdışı aktivasyonu"
            ]

            for check in checks:
                st.checkbox(check, key=f"check_{check[:20]}")

            # Packing tips
            st.markdown("#### 💡 Paketleme İpuçları")
            tips = [
                "Ağır eşyaları valiz altına yerleştirin",
                "Sıvıları içecek şişelerinde taşıyın",
                "Kırılabilir eşyaları kıyafetler arasına sarın",
                "Acil durum çantası hazırlayın"
            ]

            for tip in tips:
                st.info(f"💡 {tip}")

            # Weather-based recommendations
            st.markdown("#### 🌤️ Hava Durumu Önerisi")
            weather_rec = {
                'Kapadokya': '🧥 Sıcak kıyafetler ve eldiven gerekebilir!',
                'Pamukkale': '☀️ Güneş kremi ve bol su alın!',
                'Olympos': '🏖️ Plaj eşyaları ve yüzme kıyafetleri!'
            }

            recommendation = weather_rec.get(dest['name'], '☀️ Güneş kremi ve bol su alın!')
            st.success(recommendation)

    else:
        st.warning("🎯 Çanta listesi oluşturmak için önce Keşfet sekmesinden bir destinasyon seçin.")

elif page == "🤝 Topluluk":
    st.markdown("""
    <div class="header-container">
        <h1 class="header-title">🤝 Topluluk Deneyimleri</h1>
        <p class="header-subtitle">Gerçek seyahatçılardan öneriler ve ipuçları</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 💬 En Son İpuçları")

        for tip in community_tips:
            with st.container():
                st.markdown(f"**🏔️ {tip['destination']}**")
                st.write(tip['tip'])
                col_a, col_b = st.columns(2)
                with col_a:
                    st.caption(f"👤 {tip['author']}")
                with col_b:
                    st.caption(f"{'⭐' * tip['rating']} ({tip['rating']})")
                st.markdown("---")

        # Popular destinations stats
        st.markdown("### 🏆 Popüler Destinasyonlar")

        popular_stats = [
            {'name': 'Kapadokya', 'posts': 156, 'rating': 4.8},
            {'name': 'Pamukkale', 'posts': 89, 'rating': 4.7},
            {'name': 'Antalya', 'posts': 234, 'rating': 4.6}
        ]

        for stat in popular_stats:
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("📍 Yer", stat['name'])
            with col_b:
                st.metric("📝 Deneyim", stat['posts'])
            with col_c:
                st.metric("⭐ Puan", stat['rating'])
            st.markdown("---")

    with col2:
        st.markdown("### ✍️ Deneyiminizi Paylaşın")

        with st.form("tip_form"):
            destination_name = st.selectbox(
                "Destinasyon",
                ["Kapadokya", "Pamukkale", "Olympos", "Diğer"],
                help="Hangi yeri ziyaret ettiniz?"
            )

            if destination_name == "Diğer":
                destination_name = st.text_input("Destinasyon adını yazın")

            tip_text = st.text_area(
                "İpucunuz",
                placeholder="Diğer seyahatçılara öneriniz...",
                help="Deneyiminizi ve önerilerinizi paylaşın"
            )

            rating = st.select_slider(
                "Değerlendirme",
                options=[1, 2, 3, 4, 5],
                value=5,
                format_func=lambda x: "⭐" * x
            )

            author_name = st.text_input("Adınız", placeholder="İsteğe bağlı")

            submitted = st.form_submit_button("📤 Paylaş", use_container_width=True)

            if submitted:
                if destination_name and tip_text:
                    st.success("✅ İpucunuz başarıyla paylaşıldı!")
                    # Here you would normally save to database
                    new_tip = {
                        'destination': destination_name,
                        'tip': tip_text,
                        'author': author_name or "Anonim",
                        'rating': rating
                    }
                    st.balloons()
                else:
                    st.error("❌ Lütfen destinasyon ve ipucu alanlarını doldurun.")

elif page == "👤 Profil":
    st.markdown("""
    <div class="header-container">
        <h1 class="header-title">👤 Profil & Tercihler</h1>
        <p class="header-subtitle">Kişiselleştirilmiş seyahat deneyimi için ayarlarınız</p>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.authenticated:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 🎯 Seyahat Tercihleri")

            # Interest selection
            st.markdown("#### İlgi Alanlarınız")
            interests = [
                "🏔️ Doğa", "🏛️ Tarih", "🧭 Macera", "👥 Kültür",
                "🍽️ Gastronomi", "📷 Fotoğraf", "🏖️ Plaj", "🌆 Şehir"
            ]

            selected_interests = []

            # Create interest checkboxes in columns
            interest_cols = st.columns(2)
            for i, interest in enumerate(interests):
                with interest_cols[i % 2]:
                    if st.checkbox(interest, key=f"interest_{i}"):
                        selected_interests.append(interest)

            st.session_state.user_preferences['interests'] = selected_interests

            # Budget preference
            st.markdown("#### Tercih Edilen Bütçe Aralığı")
            budget_style = st.selectbox(
                "Seyahat Tarzı",
                ["💰 Bütçe Dostu (₺500-2000)", "🏨 Konforlu (₺2000-5000)", "✨ Lüks (₺5000+)"]
            )
            st.session_state.user_preferences['travel_style'] = budget_style

            # AI Recommendations info
            st.success("""
            🤖 **AI Önerileri:**

            Tercihlerinize göre size özel destinasyon önerileri oluşturuyoruz. 
            Seçimleriniz ne kadar detaylı olursa, önerilerimiz o kadar kişisel olur!
            """)

        with col2:
            st.markdown("### 📊 Seyahat İstatistikleri")

            # Statistics display
            stats_data = [
                ("12", "Ziyaret Edilen Yer"),
                ("5", "Paylaşılan İpucu"),
                ("₺15K", "Toplam Tasarruf"),
                ("4.8", "Ortalama Puan")
            ]

            for stat_value, stat_label in stats_data:
                st.metric(stat_label, stat_value)

            # Achievements
            st.markdown("#### 🏅 Rozet ve Başarılar")
            achievements = ["🌟 Keşifçi", "📝 İpucu Ustası", "💡 Topluluk Lideri"]

            for achievement in achievements:
                st.success(achievement)

            # Recent plans
            st.markdown("#### 🗺️ Son Planlar")
            recent_plans = [
                "Kapadokya - 3 gün",
                "Pamukkale - 2 gün",
                "Antalya - 5 gün"
            ]

            for plan in recent_plans:
                col_plan, col_status = st.columns([3, 1])
                with col_plan:
                    st.write(plan)
                with col_status:
                    st.success("✅")

    else:
        st.warning("🔐 Profil bilgilerinizi görmek için giriş yapmanız gerekiyor.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6b7280; font-size: 0.8rem; padding: 2rem 0;">
    <strong>Your Way Ally</strong> - AI Destekli Seyahat Asistanı<br>
    Made with ❤️ using Streamlit | © 2024 All Rights Reserved
</div>
""", unsafe_allow_html=True)

# Sidebar footer
with st.sidebar:
    st.markdown("---")
    st.markdown("### 📈 Sistem Durumu")

    status_items = [
        ("🟢 API Servisleri", "Aktif"),
        ("🟢 AI Sistemi", "Çalışıyor"),
        ("🟢 Veritabanı", "Bağlı"),
        ("🟢 Önbellek", "Güncellendi")
    ]

    for item, status in status_items:
        st.write(f"**{item}**: {status}")

    st.markdown("---")
    st.info("💡 **İpucu:** Daha iyi öneriler için profilinizi tamamlayın!")

# JavaScript for enhanced interactions (optional)
st.markdown("""
<script>
// Add some interactivity if needed
document.addEventListener('DOMContentLoaded', function() {
    console.log('Your Way Ally loaded successfully!');
});
</script>
""", unsafe_allow_html=True)
