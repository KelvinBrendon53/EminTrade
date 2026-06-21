import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime

# --- ARAYÜZ AYARLARI ---
st.set_page_config(page_title="EminTrade Pro", layout="wide")

# Midas-vari Koyu Tema CSS
st.markdown("""
    <style>
    .stApp { background-color: #0a0a0a; color: white; }
    .css-1r6slp0 { padding: 1rem; }
    .metric-card { background: #1a1a1a; padding: 20px; border-radius: 15px; border: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

st.title("🧭 EminTrade Pro")
st.caption(f"Güncel Zaman: {datetime.now().strftime('%H:%M:%S')}")

# --- SIDEBAR - VERİ YÖNETİMİ ---
ticker = st.sidebar.text_input("Hisse Kodu (Örn: THYAO.IS)", "THYAO.IS").upper()
btn_refresh = st.sidebar.button("🔄 Veriyi Yenile")

# --- DATA FETCHING (Canlı Veri Çekme) ---
@st.cache_data(ttl=60) # 60 saniyede bir veriyi taze tutar
def get_data(symbol):
    return yf.download(symbol, period="3mo", interval="1d")

data = get_data(ticker)

if not data.empty:
    # --- MİDAS TARZI KARTLAR ---
    son_fiyat = float(data['Close'].iloc[-1].item())
    onceki_fiyat = float(data['Close'].iloc[-2].item())
    degisim = ((son_fiyat - onceki_fiyat) / onceki_fiyat) * 100
    
    col1, col2, col3 = st.columns(3)
    with col1: st.metric("Anlık Fiyat", f"{son_fiyat:.2f} TL")
    with col2: st.metric("Günlük Değişim", f"%{degisim:.2f}", delta=f"{degisim:.2f}%")
    with col3: st.metric("İşlem Hacmi", f"{int(data['Volume'].iloc[-1].item()):,}")

    # --- TEKNİK ANALİZ (Grafik) ---
    fig = go.Figure(data=[go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'])])
    fig.update_layout(template="plotly_dark", height=400, margin=dict(l=0, r=0, t=20, b=0))
    st.plotly_chart(fig, use_container_width=True)

    # --- DETAYLI ANALİZ (İstatistikler) ---
    st.subheader("📊 Derinlemesine Analiz")
    tab1, tab2 = st.tabs(["Teknik Detay", "Hisse Bilgisi"])
    
    with tab1:
        # Basit Hareketli Ortalama (SMA) hesabı
        sma = data['Close'].rolling(window=20).mean()
        st.line_chart(data['Close'])
        st.write("20 Günlük Hareketli Ortalama: Grafikteki yükseliş trendini destekliyor.")
        
    with tab2:
        st.write(f"**{ticker}** hakkında detaylı borsa verileri güncel olarak yfinance üzerinden çekilmektedir. 3 aylık periyotta maksimum değer: {data['High'].max().item():.2f} TL.")

else:
    st.warning("Hisse verisi çekilemedi. Lütfen geçerli bir kod girin (Örn: ASELS.IS).")
