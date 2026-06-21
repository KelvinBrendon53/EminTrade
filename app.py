import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

# --- MİDAS TASARIM (Mobile First) ---
st.set_page_config(page_title="EminTrade", layout="centered")

st.markdown("""
    <style>
    /* Midas Renk Paleti ve Fontlar */
    .stApp { background-color: #000000; color: #FFFFFF; font-family: sans-serif; }
    h1 { font-size: 24px !important; margin-bottom: 0px !important; }
    .stMetric { background-color: #121212; padding: 15px; border-radius: 12px; border: 1px solid #222; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #007AFF; color: white; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# Başlık
st.title("EminTrade")
st.caption("Piyasa Gözlemcisi")

# Hisse Girişi
ticker = st.text_input("", "THYAO.IS").upper()

@st.cache_data(ttl=60)
def get_data(symbol):
    return yf.download(symbol, period="1mo", interval="1d")

data = get_data(ticker)

if not data.empty:
    son_fiyat = float(data['Close'].iloc[-1].item())
    degisim = ((son_fiyat - float(data['Close'].iloc[-2].item())) / float(data['Close'].iloc[-2].item())) * 100
    
    # Midas Tarzı Üst Panel
    st.write(f"## {son_fiyat:.2f} TL")
    st.write(f":{'green' if degisim >= 0 else 'red'}[%{degisim:.2f}]")
    
    # Grafik (Minimalist)
    fig = go.Figure(data=[go.Scatter(x=data.index, y=data['Close'], line=dict(color='#007AFF', width=2))])
    fig.update_layout(
        template="plotly_dark",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        margin=dict(l=0, r=0, t=0, b=0),
        height=250
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Midas Kartları
    c1, c2 = st.columns(2)
    c1.metric("En Yüksek", f"{float(data['High'].max().item()):.2f}")
    c2.metric("En Düşük", f"{float(data['Low'].min().item()):.2f}")
    
    st.button("Alış Yap")
    st.button("Satış Yap")

else:
    st.error("Hisse bulunamadı.")
