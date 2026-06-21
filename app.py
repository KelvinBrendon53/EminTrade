# --- İSTATİSTİKSEL ÖZET ---
    st.subheader("📊 Temel İstatistikler")
    col1, col2, col3 = st.columns(3)
    
    # Veriyi float (sayı) formatına zorluyoruz
    son_fiyat = float(data['Close'].iloc[-1].item())
    onceki_fiyat = float(data['Close'].iloc[-2].item())
    degisim = ((son_fiyat - onceki_fiyat) / onceki_fiyat) * 100
    hacim = int(data['Volume'].iloc[-1].item())
    
    col1.metric("Son Fiyat", f"{son_fiyat:.2f}")
    col2.metric("Günlük Değişim", f"{degisim:.2f}%", delta=f"{degisim:.2f}%")
    col3.metric("İşlem Hacmi", f"{hacim:,}")
