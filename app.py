# 2. MODÜL: TEKNİK GÖSTERGE (RSI MANTIĞI) - HATA DÜZELTİLMİŞ HALİ
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi_series = 100 - (100 / (1 + rs))
    
    # .iloc[-1] değerini float'a zorluyoruz
    rsi_value = float(rsi_series.iloc[-1].item())
    
    # Görselleştirme
    st.write(f"## {son_fiyat:.2f} TL")
    fig = go.Figure(data=[go.Scatter(x=data.index, y=data['Close'], line=dict(color='#007AFF', width=2))])
    fig.update_layout(template="plotly_dark", height=250, margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(fig, use_container_width=True)

    # 3. MODÜL: PİYASA PSIKOLOJISI (Haber)
    st.subheader("📰 Güncel Piyasa Psikolojisi")
    if rsi_value > 70:
        st.warning("⚠️ Aşırı Alım Bölgesi: Kar satışı gelebilir, dikkatli ol!")
    elif rsi_value < 30:
        st.success("✅ Aşırı Satım Bölgesi: Alım fırsatı olabilir.")
    else:
        st.info(f"📊 Piyasa Nötr: RSI Değeri: {rsi_value:.2f} - Bekle ve gör.")
