import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import numpy as np

# --- MİDAS TASARIM (Pro Versiyon) ---
st.set_page_config(page_title="EminTrade Pro", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #FFFFFF; }
    .metric-card { background: #121212; padding: 15px; border-radius: 12px; border: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

st.title("EminTrade ⚡")
ticker = st.text_input("", "THYAO.IS").upper()

@st.cache_data(ttl=60)
def get_data(symbol):
    return yf.download(symbol, period="3mo", interval="1d")

data = get_data(ticker)

if not data.empty:
    son_fiyat = float(data['Close'].iloc[-1].item())
    
    # 1. MODÜL: KAR/ZARAR SİMÜLATÖRÜ
    with st.expander("💰 Portföy Hesaplayıcı"):
        yatirilan = st.number_input("Yatırılan Tutar (TL)", value=10000)
        adet = yatirilan / float(data['Close'].iloc[0].item())
        guncel_deger = adet * son_fiyat
        st.write(f"Tahmini Güncel Değer: **{guncel_deger:.2f} TL**")
        st.write(f"Toplam Getiri: **{guncel_deger - yatirilan:.2f} TL**")

    # 2. MODÜL: TEKNİK GÖSTERGE (RSI MANTIĞI)
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    # Görselleştirme
    st.write(f"## {son_fiyat:.2f} TL")
    fig = go.Figure(data=[go.Scatter(x=data.index, y=data['Close'], line=dict(color='#007AFF', width=2))])
    fig.update_layout(template="plotly_dark", height=250, margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(fig, use_container_width=True)

    # 3. MODÜL: PİYASA PSIKOLOJISI (Haber)
    st.subheader("📰 Güncel Piyasa Psikolojisi")
    if rsi.iloc[-1] > 70:
        st.warning("⚠️ Aşırı Alım Bölgesi: Kar satışı gelebilir, dikkatli ol!")
    elif rsi.iloc[-1] < 30:
        st.success("✅ Aşırı Satım Bölgesi: Alım fırsatı olabilir.")
    else:
        st.info("📊 Piyasa Nötr: Bekle ve gör stratejisi.")

else:
    st.error("Hisse bulunamadı.")
