import streamlit as st

# Midas'ın "App" görünümü için ayarlar
st.set_page_config(page_title="EminTrade", layout="centered")

# --- MİDAS TASARIM (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #FFFFFF; }
    .card { background-color: #121212; padding: 20px; border-radius: 15px; margin-bottom: 15px; }
    .stButton>button { border-radius: 20px; background-color: #333; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- UYGULAMA SEKMELERİ (Midas Gibi) ---
tab1, tab2, tab3 = st.tabs(["Yatırım", "Keşfet", "Listeler"])

with tab1:
    st.title("Yatırım")
    st.subheader("$0,00")
    st.caption("Günlük (%0,00)")
    
    # "1000126992.jpg" görselindeki gibi buton yapısı
    c1, c2, c3 = st.columns(3)
    c1.button("Aktar")
    c2.button("Çek")
    c3.button("Döviz Al/Sat")
    
    st.markdown('<div class="card">Yatırımda yeni rota: Avrupa<br>İlk durak Almanya borsası...</div>', unsafe_allow_html=True)

with tab2:
    st.title("Keşfet")
    # "1000126993.jpg" görselindeki gibi arama çubuğu
    st.text_input("", placeholder="Aramak için bir şey yaz")
    
    # Kategori Filtreleri
    st.write("ABD | BIST | Avrupa | Fonlar | Kripto")
    
    st.subheader("Günün öne çıkanları")
    # Liste öğeleri (Örnek)
    st.markdown("**TP2** - Tera Portföy | %60,30")
    st.markdown("**PHE** - Pusula Portföy | %224,18")

with tab3:
    st.title("Listeler")
    st.info("Opsiyon kontratlarını takip listesine ekleyebilirsin.")
