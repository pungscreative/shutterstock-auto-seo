import streamlit as st
import pandas as pd
from PIL import Image
from google import genai

# Konfigurasi Halaman
st.set_page_config(page_title="Nyetok.Kuy Pro | AI SEO Metadata", page_icon="✨", layout="wide")

# CSS Styling - Gradasi Judul & Subteks serta Efek Kaca Transparan yang Seragam
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #c7d2fe 0%, #e9d5ff 35%, #fbcfe8 70%, #fed7aa 100%);
        background-attachment: fixed;
    }
    
    /* Efek Kaca Transparan yang Seragam untuk Judul & Kolom */
    .hero-container, .glass-box {
        background: rgba(255, 255, 255, 0.4);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.6);
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
    }
    
    .hero-container {
        text-align: center;
        padding: 30px;
        margin-bottom: 25px;
    }
    
    .glass-box {
        padding: 25px;
        height: 100%;
    }
    
    /* Font Tebal Gemuk dengan Gradasi untuk Judul & Subteks */
    .gradient-title, .gradient-heading {
        font-family: 'Fredoka', sans-serif;
        font-weight: 700;
        background: linear-gradient(135deg, #4338ca 0%, #7e22ce 50%, #be185d 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .gradient-title {
        font-size: 2.5rem;
        margin-bottom: 5px;
    }
    
    .gradient-heading {
        font-size: 1.25rem;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Header Utama
st.markdown("""
<div class="hero-container">
    <h1 class="gradient-title">✨ Nyetok.Kuy Pro</h1>
    <p style="color: #475569; font-weight: 500;">Sistem Otomatisasi Metadata Stok Foto Profesional & SEO Optimal</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown('<div class="glass-box">', unsafe_allow_html=True)
    st.markdown('<h3 class="gradient-heading">⚙️ Konfigurasi & Upload</h3>', unsafe_allow_html=True)
    
    # Ambil API Key dari secrets atau sediakan input manual jika gagal
    api_key = None
    try:
        if "GEMINI_API_KEY" in st.secrets:
            api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass
        
    if not api_key:
        api_key = st.text_input("🔑 Masukkan Gemini API Key", type="password")
    
    uploaded_file = st.file_uploader("Upload Foto Produk", type=["jpg", "jpeg", "png"])
    
    if uploaded_file:
        st.image(uploaded_file, caption="Pratinjau Foto", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="glass-box">', unsafe_allow_html=True)
    st.markdown('<h3 class="gradient-heading">📊 Hasil Pemrosesan AI</h3>', unsafe_allow_html=True)
    
    if uploaded_file and api_key:
        if st.button("🚀 Generate Metadata SEO", type="primary"):
            with st.spinner("✨ AI sedang meracik metadata terbaik..."):
                try:
                    client = genai.Client(api_key=api_key.strip())
                    img = Image.open(uploaded_file)
                    
                    prompt = """
                    Act as a professional Shutterstock contributor. 
                    Analyze the image and provide metadata in English format:
                    TITLE: [A concise, commercial search-friendly title]
                    KEYWORDS: [Provide EXACTLY 45 relevant comma-separated keywords.]
                    CATEGORY: [Pick one: Animals/Wildlife, Nature, Backgrounds, People, Technology, Food/Drink]
                    DESCRIPTION: [A detailed commercial description]
                    """
                    
                    response = client.models.generate_content(
                        model='gemini-3.5-flash',
                        contents=[prompt, img]
                    )
                    
                    st.success("🎉 Metadata berhasil disusun!")
                    st.text_area("Hasil Lengkap AI:", response.text, height=200)
                    
                except Exception as e:
                    st.error(f"Terjadi kesalahan pada sistem AI: {e}")
    else:
        st.info("💡 Silakan unggah foto dan pastikan API Key sudah tersedia untuk mengaktifkan tombol.")
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #475569; font-size: 0.85rem;'>© 2026 Nyetok.Kuy - All Rights Reserved | powered by Pungs Creative</p>", unsafe_allow_html=True)
