import streamlit as st
import pandas as pd
from PIL import Image
from google import genai

# Konfigurasi Halaman
st.set_page_config(page_title="Nyetok.Kuy Pro | AI SEO Metadata", page_icon="✨", layout="wide")

# CSS Styling - Diperbarui agar lebih stabil
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
    
    html, body {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Memastikan background app terlihat */
    .stApp {
        background: linear-gradient(135deg, #c7d2fe 0%, #e9d5ff 35%, #fbcfe8 70%, #fed7aa 100%);
        background-attachment: fixed;
    }

    /* Hero Header dengan Efek Kaca */
    .hero-container {
        text-align: center;
        padding: 35px 20px;
        background: rgba(255, 255, 255, 0.3);
        backdrop-filter: blur(25px);
        border: 1px solid rgba(255, 255, 255, 0.5);
        border-radius: 24px;
        margin-bottom: 30px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.08);
        position: relative;
    }
    
    /* Font Gradasi */
    .gradient-title {
        font-family: 'Fredoka', sans-serif;
        font-weight: 700;
        font-size: 2.8rem;
        background: linear-gradient(135deg, #4338ca 0%, #7e22ce 50%, #be185d 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Memastikan konten di atas blob */
    .stApp > div {
        position: relative;
        z-index: 10;
    }
</style>
""", unsafe_allow_html=True)

# Layout Header Hero
st.markdown("""
<div class="hero-container">
    <div style="display: inline-block; background: rgba(255, 255, 255, 0.5); color: #6b21a8; padding: 4px 14px; border-radius: 20px; font-size: 0.75rem; font-weight: 700; margin-bottom: 10px;">✨ AI-POWERED PUNGS CREATIVE</div>
    <h1 class="gradient-title">Nyetok.Kuy Pro</h1>
    <p>Sistem Otomatisasi Metadata Stok Foto Profesional & SEO Optimal</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.subheader("⚙️ Konfigurasi & Upload")
    
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        api_key = None
        st.error("⚠️ API Key tidak terkonfigurasi di secrets.toml.")
    
    uploaded_file = st.file_uploader("Upload Foto Produk", type=["jpg", "jpeg", "png"])
    
    if uploaded_file:
        # Perubahan: menggunakan width='stretch' (Sesuai update Streamlit terbaru)
        st.image(uploaded_file, width='stretch', caption="Pratinjau Foto")

with col2:
    st.subheader("📊 Hasil Pemrosesan AI")
    
    if uploaded_file and api_key:
        if st.button("🚀 Generate Metadata SEO"):
            with st.spinner("✨ AI sedang meracik metadata..."):
                try:
                    client = genai.Client(api_key=api_key.strip())
                    img = Image.open(uploaded_file)
                    
                    prompt = "Act as a Shutterstock contributor. Provide TITLE, KEYWORDS (exactly 45), CATEGORY, and DESCRIPTION."
                    
                    response = client.models.generate_content(
                        model='gemini-3.5-flash',
                        contents=[prompt, img]
                    )
                    
                    # Logika tampilan dataframe
                    st.success("🎉 Berhasil!")
                    # Perubahan: menggunakan width='stretch'
                    st.dataframe(pd.DataFrame({"Result": [response.text]}), width='stretch')
                    
                except Exception as e:
                    st.error(f"Error: {e}")
    else:
        st.info("💡 Silakan unggah foto.")

# Footer
st.markdown('<div style="text-align: center; margin-top: 50px; color: #475569;">© 2026 Nyetok.Kuy | powered by Pungs Creative</div>', unsafe_allow_html=True)
