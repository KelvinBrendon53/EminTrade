import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

# --- SAYFA YAPILANDIRMASI ---
st.set_page_config(page_title="EminTrade Terminal", layout="wide")

# --- BAŞLIK VE SIDEBAR ---
st.title("🧭 EminTrade Terminal")
st.sidebar.info("**EminTrade Terminal**\n\nKurucu: **Gaviria Emin Bey**\n\n*Piyasaların puslu havasında rotanızı belirleyin.*")

# --- HİSSE SEÇİMİ ---
ticker = st.sidebar.text_input("Hisse Kodu (Örn: THYAO.IS, AAPL)", "THYAO.IS")
period = st.sidebar.selectbox("Analiz Periyodu", ["1mo", "3mo", "6mo", "1y", "2y"])

# --- VERİ İŞLEME ---
@st.cache_data # Hızlandırmak için önbellekleme
def veri_cek(sembol, periyot):
    return yf.download(sembol, period=periyot, interval="1d")

data = veri_cek(ticker, period)

if not data.empty:
    st.write(f"### {ticker} Teknik Analiz Grafiği")
    
    # Mum Grafiği (Candlestick)
    fig = go.Figure(data=[go.Candlestick(x=data.index,
                    open=data['Open'],
                    high=data['High'],
                    low=data['Low'],
                    close=data['Close'])])
    
    fig.update_layout(title=f"{ticker} Piyasa Hareketleri", xaxis_title="Tarih", yaxis_title="Fiyat")
    st.plotly_chart(fig, use_container_width=True)

    # --- İSTATİSTİKSEL ÖZET ---
    st.subheader("📊 Temel İstatistikler")
    col1, col2, col3 = st.columns(3)
    
    son_fiyat = data['Close'].iloc[-1]
    onceki_fiyat = data['Close'].iloc[-2]
    degisim = ((son_fiyat - onceki_fiyat) / onceki_fiyat) * 100
    
    col1.metric("Son Fiyat", f"{son_fiyat:.2f}")
    col2.metric("Günlük Değişim", f"{degisim:.2f}%", delta=f"{degisim:.2f}%")
    col3.metric("İşlem Hacmi", f"{data['Volume'].iloc[-1]:,.0f}")
else:
    st.error("Veri alınamadı! Lütfen geçerli bir hisse kodu girin (BIST hisseleri için .IS takısını unutmayın).")

st.divider()
st.caption("EminTrade Terminal - Gelişmiş Finansal Analiz Platformu © 2026 | Gaviria Emin Bey")