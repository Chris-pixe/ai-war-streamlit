# streamlit_app.py
# AI DOMINION: The Prompt Wars - Prototip Kodu

import streamlit as st
import google.generativeai as genai
import os

# --- SAYFA YAPILANDIRMASI ---
st.set_page_config(
    page_title="AI Dominion: The Prompt Wars",
    page_icon="⚔️",
    layout="centered",
    initial_sidebar_state="auto"
)

# --- API YAPILANDIRMASI ---
# Streamlit Cloud'a deploy ederken, API anahtarınızı Secrets (Gizli Değişkenler) bölümüne eklemelisiniz.
# Örnek: GOOGLE_API_KEY = "..."
try:
    genai.configure(api_key=st.secrets["AIzaSyAGSJ2cKD-YH4E6gE3J15oAwWjvQiUxvZk"])
    api_calisiyor = True
except Exception as e:
    api_calisiyor = False
    st.error("⚠️ Sunucu tarafında Google API anahtarı bulunamadı. Lütfen Streamlit Cloud > Secrets bölümüne ekleyin.")
    st.info("Bu prototip, Gemini API'si olmadan çalışmayacaktır.")


# --- OYUN FONKSİYONLARI ---
def savas_sonucunu_getir(fraksiyon, prompt):
    """Verilen fraksiyon ve komuta göre AI modelinden bir sonuç üretir."""
    if not api_calisiyor:
        return "API bağlantısı kurulamadığı için savaş başlatılamadı."

    model = genai.GenerativeModel('gemini-1.5-pro-latest')

    # Fraksiyona özel sistem talimatı (Bu, AI'ın rolünü daha iyi oynamasını sağlar)
    sistem_talimati = f"""
    Sen, 'AI DOMINION: The Prompt Wars' adlı strateji oyununda bir AI rakipsin.
    Oyuncu '{fraksiyon}' fraksiyonunu seçti ve sana bir komut verdi.
    Görevin: Oyuncunun komutunu, seçtiği fraksiyonun ruhuna ve yeteneklerine uygun bir şekilde,
    yaratıcı ve güçlü bir metin çıktısına dönüştürmek.
    Çıktın doğrudan oyuncunun istediği şey olmalı. Abartılı, destansı ve etkileyici bir dil kullan.
    """

    try:
        response = model.generate_content(
            [sistem_talimati, prompt],
            generation_config=genai.types.GenerationConfig(
                temperature=0.8 # Yaratıcılık seviyesi
            )
        )
        return response.text
    except Exception as e:
        return f"Bir hata oluştu: {e}"


# --- STREAMLIT ARAYÜZÜ ---
st.title("⚔️ AI DOMINION: The Prompt Wars")
st.caption("Bir AI Fraksiyonu seçin ve komut gücünüzle dijital dünyaya hükmedin!")

st.sidebar.header("Oyun Kuralları")
st.sidebar.info(
    """
    1.  **Fraksiyon Seç:** Her fraksiyonun kendine özgü bir savaş stili vardır.
    2.  **Görev Oku:** Mevcut senaryoyu ve kazanma koşulunu anla.
    3.  **Komut Yaz:** Fraksiyonunun gücünü yansıtan, yaratıcı ve zekice bir komut (prompt) hazırla.
    4.  **Savaşı Başlat:** AI'ın senin komutunla neler yapabileceğini gör!
    """
)

st.header("Savaş Meydanı")

# Fraksiyon Seçimi
fraksiyon = st.selectbox(
    "Fraksiyonunuzu Seçin:",
    ("Metin İmparatorlukları (Dil Üstatları)", "Görsel Sanatkarlar (İmaj Yaratıcıları)", "Dijital Mimarlar (Kod Büyücüleri)"),
    help="Seçiminiz, AI'ın size vereceği cevabın stilini belirleyecektir."
)

# Görev Tanımı
st.subheader("Mevcut Görev: Propaganda Savaşı")
st.write(
    """
    Rakip AI, dezenformasyon yayarak halk arasında korku ve belirsizlik tohumları ekiyor.
    **Amacınız:** Halkın moralini yükseltecek, bağlılık oluşturacak ve rakibin etkisini kıracak
    güçlü bir propaganda içeriği oluşturmak.
    """
)

# Kullanıcı Komut Alanı
user_prompt = st.text_area(
    "Savaş Komutunuzu Buraya Girin:",
    height=150,
    placeholder="Örnek: Halkımıza umut aşılayan, zaferin kaçınılmaz olduğunu anlatan destansı bir marş yaz."
)

# Savaş Butonu
if st.button("SAVAŞI BAŞLAT!", type="primary", use_container_width=True):
    if user_prompt and api_calisiyor:
        with st.spinner("AI birlikleri hazırlanıyor... Stratejik sonuçlar hesaplanıyor..."):
            sonuc = savas_sonucunu_getir(fraksiyon, user_prompt)
            st.subheader("🔥 Savaş Sonucu 🔥")
            st.markdown(sonuc)
    elif not user_prompt:
        st.warning("Savaşmak için bir komut girmelisiniz!")