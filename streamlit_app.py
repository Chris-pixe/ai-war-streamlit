# ai_war_app.py
import streamlit as st
import google.generativeai as genai
import os

# API Anahtarınızı buraya ekleyin veya ortam değişkeni olarak ayarlayın
# os.environ['GOOGLE_API_KEY'] = "YOUR_API_KEY"
# genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
# API anahtarınızı yapılandırdığınızdan emin olun
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except Exception as e:
    st.error("Lütfen Google API anahtarınızı Streamlit Secrets'a ekleyin!")


def savas_sonucunu_getir(fraksiyon, prompt):
    # Bu prototipte sadece Gemini modelini kullanacağız
    # Farklı fraksiyonlar için prompt'u özelleştirebiliriz
    model = genai.GenerativeModel('gemini-1.5-pro-latest')

    hazirlik_promptu = f"""
    Sen, AI DOMINION oyununda bir AI asistanısın. Oyuncu '{fraksiyon}' fraksiyonunu seçti.
    Görevi: Rakibin korku propagandasına karşı halkın desteğini kazanmak.
    Oyuncunun komutu şu: '{prompt}'
    Bu komuta dayanarak, seçilen fraksiyonun yeteneklerine uygun, yaratıcı ve etkili bir propaganda çıktısı üret.
    Çıktın doğrudan propaganda metni olsun.
    """

    response = model.generate_content(hazirlik_promptu)
    return response.text
st.title("AI DOMINION: The Prompt Wars")
st.caption("Bir AI Fraksiyonu seçin ve komut gücünüzü gösterin!")

# Fraksiyon Seçimi
fraksiyon = st.selectbox(
    "Fraksiyonunuzu Seçin:",
    ("Metin İmparatorlukları (Gemini)", "Görsel Sanatkarlar (DALL-E - Simülasyon)", "Dijital Mimarlar (Kodlama Görevi)")
)

# Görev Tanımı
st.subheader("Görev: Propaganda Üretimi")
st.write("Göreviniz, seçtiğiniz fraksiyonun gücünü kullanarak halkın desteğini kazanacak bir propaganda metni/fikri üretmektir. Rakibiniz belirsizlik ve korku yaymaya çalışıyor.")

# Kullanıcı Komut Alanı
user_prompt = st.text_area("Savaş Komutunuzu Buraya Girin:", height=150)

# Savaş Butonu
if st.button("SAVAŞI BAŞLAT!"):
    if user_prompt:
        with st.spinner("AI birlikleri hazırlanıyor... Sonuçlar hesaplanıyor..."):
            sonuc = savas_sonucunu_getir(fraksiyon, user_prompt)
            st.subheader("Savaş Sonucu:")
            st.markdown(sonuc)
    else:
        st.error("Savaşmak için bir komut girmelisiniz!")
